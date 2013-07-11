from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django import forms
from django.forms import CharField, Form, PasswordInput
from PIL import Image

from account.models import UserProfile,EmailChange

class RegisterForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField(label=_("E-mail"))
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password (Confirm)"),
                                widget=forms.PasswordInput)

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if len(first_name) > 30:
            raise forms.ValidationError(_('Ensure this value has at most 30 characters'))
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        if len(last_name) > 30:
            raise forms.ValidationError(_('Ensure this value has at most 30 characters'))
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if len(email) > 75:
            raise forms.ValidationError(_('Email address too long. '
                                           'Please enter maximum 75 characters.'))
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(_('Email addresses already exists.'))
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_('The passwords are not the same'))
        
        return password2

    def save(self, profile_callback=None):
        username = User.objects.make_random_password() * 3
        user = User.objects.create(username=username,
                                   password=self.cleaned_data["password1"],
                                   email=self.cleaned_data["email"],
                                   first_name=self.cleaned_data["first_name"],
                                   last_name=self.cleaned_data["last_name"],
                                   is_active=True)
        user.set_password(self.cleaned_data["password1"])
        user.save()

        p = user.get_profile()
        p.activation_key = User.objects.make_random_password()
        p.is_approved = False
        p.save()
        return user


class LoginForm(forms.Form):
    username = forms.RegexField(
                        regex=r'^[\w.@+-]+$',
                        max_length=100,
                        label=_("Username"),
                        error_messages={'invalid': _("Username can contain any "
                                                     "letters or numbers, "
                                                     "without spaces")})

    password = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(email=username)
        
        if user.exists():
            user = user[0]
        else:
            raise forms.ValidationError(_("Invalid email/password"))

        if not user.is_active:
            disabled_msg = 'Disabled account. Please contact blog admin'
            raise forms.ValidationError(_(disabled_msg))
        elif not user.get_profile().is_approved:
            deactive_msg = 'Not activated account! Please activate your account'
            raise forms.ValidationError(_(deactive_msg))
        return username

class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if len(first_name) > 30:
            raise forms.ValidationError(_('Ensure this value has at most 30 characters'))
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        if len(last_name) > 30:
            raise forms.ValidationError(_('Ensure this value has at most 30 characters'))
        return last_name

    class Meta:
        model = User
        fields = ('first_name', 'last_name')
        
class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # magic 
        self.user = kwargs['instance'].user
        user_kwargs = kwargs.copy()
        user_kwargs['instance'] = self.user
        self.uf = UserForm(*args, **user_kwargs)
        # magic end 

        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields.update(self.uf.fields)
        self.initial.update(self.uf.initial)
         
        # define fields order if needed
        self.fields.keyOrder = (
            'first_name',
            'last_name',
        
            'gender',
            'image',
        )

    def save(self, *args, **kwargs):
        # save both forms   
        self.uf.save(*args, **kwargs)
        return super(ProfileForm, self).save(*args, **kwargs)

    class Meta:
        model = UserProfile
        fields = ('image', 'gender')

class PasswordForm(forms.ModelForm):
    oldpassword = forms.CharField(widget=PasswordInput(),
                                  label=_('Current Password'))
    password1 = forms.CharField(widget=PasswordInput(),
                                label=_('New Password'))
    password2 = forms.CharField(widget=PasswordInput(),
                                label=_('New Password (again)'))

    def clean_oldpassword(self):
        oldpassword = self.cleaned_data.get("oldpassword")
        if oldpassword and not self.instance.check_password(oldpassword):
            raise forms.ValidationError(_("Please type your current password."))
        return oldpassword

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_('The new passwords are not the same'))
        
        return password2

    def save(self):
        self.instance.set_password(self.cleaned_data["password2"])
        self.instance.save()
        return self.instance

    class Meta:
        model = User
        fields = ('oldpassword','password1','password2')


class EmailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    password = forms.CharField(
                    widget=PasswordInput(),
                    label=_('Current Password')
                )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        email_msg = "Email address already using by another user!"
        
        if len(email) > 75:
            raise forms.ValidationError(_('Email address too long. '
                                           'Please enter maximum 75 characters.'))
        elif self.instance.email == email:
            raise forms.ValidationError(_("Please enter a new email address"))
        # search email on User table
        if email and User.objects.filter(email=email):
            raise forms.ValidationError(_(email_msg))
        # search email on EmailChange table 
        elif email and EmailChange.objects.filter(email=email):
            raise forms.ValidationError(_(email_msg))
        
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password and not self.instance.check_password(password):
            raise forms.ValidationError(_("Please type your current password"))
        return password

    def save(self):
        return self.instance

    class Meta:
        model = User
        fields = ('email','password')

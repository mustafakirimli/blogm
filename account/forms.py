from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from account.models import UserProfile,EmailChange
from django import forms
from django.forms import CharField, Form, PasswordInput
from PIL import Image

class RegisterForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField(label=_("E-mail"))
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password (Confirm)"),
                                widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u_('Email addresses already exists.'))
        return email

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
    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=30,
                                label=_("Username"),
                                error_messages={'invalid': _("Username can contain any letters or numbers, without spaces")})

    password = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)


class UserForm(forms.ModelForm):
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
    oldpassword = forms.CharField(widget=PasswordInput(),label=_('Current Password'))
    password1 = forms.CharField(widget=PasswordInput(),label=_('New Password'))
    password2 = forms.CharField(widget=PasswordInput(),label=_('New Password (again)'))

    def clean_oldpassword(self):
        if self.cleaned_data.get("oldpassword") and not self.instance.check_password(self.cleaned_data["oldpassword"]):
            raise forms.ValidationError(_("Please type your current password."))
        return self.cleaned_data["oldpassword"]

    def clean_password2(self):
        if self.cleaned_data.get('password1') and self.cleaned_data.get('password2') and self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError(_('The new passwords are not the same'))
        return self.cleaned_data['password2']

    def save(self):
        self.instance.set_password(self.cleaned_data["password2"])
        self.instance.save()
        return self.instance

    class Meta:
        model = User
        fields = ('oldpassword','password1','password2')
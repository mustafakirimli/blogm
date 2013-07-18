from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django import forms
from django.forms import CharField, Form, PasswordInput
from PIL import Image
from django.contrib.auth import authenticate

from account.models import UserProfile,EmailChange

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=75, 
                            label=_("E-mail"))
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password (Confirm)"),
                                widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).count():
            raise forms.ValidationError(_('Email addresses already exists.'))
        return email

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_('The passwords are not the same'))
        
        return self.cleaned_data

    def save(self):
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

class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = User
        fields = ('first_name', 'last_name')
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('image', 'gender')


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
        
        if self.instance.email == email:
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

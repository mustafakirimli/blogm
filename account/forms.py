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
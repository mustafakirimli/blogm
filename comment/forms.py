from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django import forms
from django.forms import CharField, Form
from PIL import Image
from django.contrib.contenttypes.models import ContentType

from comment.models import Comment

class CommentForm(forms.ModelForm):

    def clean_fullname(self):
        fullname = self.cleaned_data.get('fullname')

        if len(fullname) > 100:
            raise forms.ValidationError(_('Ensure this value has at most 100 characters'))
        return fullname

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if len(email) > 100:
            raise forms.ValidationError(_('Ensure this value has at most 100 characters'))
        return email

    parent_id = forms.CharField(widget=forms.HiddenInput())
    comment_type = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, user, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        comment_type = ContentType.objects.get(app_label="post", model="post")
        instance = super(CommentForm, self).save(commit=False)
        instance.user = self.user
        instance.comment_type = comment_type
        instance.activation_key = User.objects.make_random_password()
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Comment
        fields = ('fullname', 'email', 'content', 'parent_id')
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django import forms
from django.forms import CharField, Form
from PIL import Image

from comment.models import Comment

class CommentForm(forms.ModelForm):
    parent_id = forms.CharField(widget=forms.HiddenInput())
    comment_type = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = Comment
        fields = ('fullname', 'email', 'content', 'parent_id')
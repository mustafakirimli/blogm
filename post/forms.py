from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django import forms
from django.forms import CharField, Form
from PIL import Image

from post.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('name','title','description','content','image')
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from post.models import Post
from django import forms
from django.forms import CharField, Form
from PIL import Image

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('name','title','description','content','image')
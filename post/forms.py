from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django import forms
from django.forms import CharField, Form
from PIL import Image

from post.models import Post

class PostForm(forms.ModelForm):
    
    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        instance = super(PostForm, self).save(commit=False)
        instance.user = self.user
        instance.activation_key = User.objects.make_random_password()
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Post
        fields = ('name','title','description','content','image')
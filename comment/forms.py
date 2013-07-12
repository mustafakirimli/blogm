from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django import forms
from django.forms import CharField, Form
from PIL import Image

from comment.models import Comment

class CommentForm(forms.ModelForm):
    parent_id = forms.CharField(widget=forms.HiddenInput())
    comment_type = forms.CharField(widget=forms.HiddenInput())
    reply_id = forms.CharField(widget=forms.HiddenInput(), 
                               required=False)

    def __init__(self, user, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.user = user
        if self.user.is_authenticated():
            self.fields['fullname'].widget = forms.HiddenInput()
            self.fields['email'].widget = forms.HiddenInput()
        else:
            self.fields['fullname'].required = True
            self.fields['email'].required = True

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

    def save(self, commit=True):
        reply_id = self.cleaned_data.get("reply_id")
        if reply_id:
            comment_type = Comment.type_comment
            parent_id = reply_id
        else:
            comment_type = Comment.type_post
            parent_id = self.cleaned_data["parent_id"]
        
        instance = super(CommentForm, self).save(commit=False)
        instance.user = self.user
        instance.comment_type = comment_type
        instance.parent_id = parent_id
        instance.activation_key = User.objects.make_random_password()

        # if user is authenticated, fill form from user object
        if instance.user.is_authenticated():
            instance.fullname = "%s %s" %(instance.user.first_name,
                                          instance.user.last_name)
            instance.email = instance.user.email

        if commit:
            instance.save()
        return instance

    class Meta:
        model = Comment
        fields = ('fullname', 'email', 'content', 'parent_id')
from django.utils.translation import ugettext as _
from django import forms

from comment.models import Comment
from post.models import Post

class CommentForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.user = user
        if self.user.is_authenticated():
            self.fields['fullname'].widget = forms.HiddenInput()
            self.fields['email'].widget = forms.HiddenInput()
        else:
            self.fields['fullname'].required = True
            self.fields['email'].required = True

    class Meta:
        model = Comment
        fields = ('fullname', 'email', 'content')

class ReplyForm(CommentForm):
    parent_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Comment
        fields = ('fullname', 'email', 'content', 'parent_id')
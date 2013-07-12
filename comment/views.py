from django.db import models
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404, redirect

from comment.models import Comment
from comment.forms import CommentForm
from post.views import detail

def add_comment(request):
    post_id = request.POST.get("parent_id")
    if request.method == 'POST':
        form = CommentForm(request.user, request.POST)
        if form.is_valid():
            comment = form.save()
            if request.user.is_authenticated():
                comment.approve()
            else:
                comment.notify_admin.delay(comment)
            messages.success(request, _("Comment created succesfully."))
            return redirect("post_detail", post_id=post_id)
        return detail(request, post_id, form=form)

def approve_comment(request, activation_key):
    try:
        # get comment with given activation key
        c = get_object_or_404(Comment, activation_key=activation_key)
        # approve comment
        c.approve()
        # redirect to homepage
        messages.info(request, _("Comment approved."))
    except:
        messages.info(request, _("Comment approve problem!"))

    return redirect("home")
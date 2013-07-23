from django.db import models
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404, redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from comment.models import Comment
from comment.forms import CommentForm, ReplyForm
from post.views import detail
from post.models import Post
from comment.tasks import send_email_validation

def add_comment(request, post_id):
    """
    Process add comment post request
    """
    if request.method == 'POST':
        form = CommentForm(request.user, request.POST)
        if form.is_valid():
            # get post object with id
            post = Post.objects.get(id=post_id)

            # set comment user, post instance and parent (comment type)
            form.instance.user = request.user
            form.instance.post = post
            form.instance.parent = post

            # insert comment
            comment = form.save()

            # if user is auth. approve comment directly and fill user data
            if request.user.is_authenticated():
                # approve comment
                comment.approve()

                # fill user fullname, email data and save
                comment.fullname = "%s %s" %(request.user.first_name,
                                             request.user.last_name)
                comment.email = request.user.email
                comment.save()
            # if user not auth. create and send activation key with email
            else:
               # create activation key 
                comment.activation_key = User.objects.make_random_password()
                comment.save()
                send_email_validation.delay(comment)

            # add success message            
            messages.success(request, _("Comment created succesfully."))

            # redirect to post detail page
            return redirect("post_detail", post_id=post_id)

        # if form is not valid render post detail for showing errors
        return detail(request, post_id, comment_form=form)
    else:
        return redirect("post_detail", post_id=post_id)

def add_reply(request, post_id):
    """
    Process add comment post request
    """
    if request.method == 'POST':
        comment_id = request.POST.get("parent_id")
        form = ReplyForm(request.user, request.POST)
        if form.is_valid():
            post = Post.objects.get(id=post_id)
            comment = Comment.objects.get(id=comment_id)
            form.instance.user = request.user
            form.instance.post = post
            form.instance.parent = comment
            reply = form.save()
            if request.user.is_authenticated():
                reply.approve()
                reply.fullname = "%s %s" %(request.user.first_name,
                                             request.user.last_name)
                reply.email = request.user.email
                reply.save()
            else:
                comment.activation_key = User.objects.make_random_password()
                comment.save()
                send_email_validation.delay(reply)
            messages.success(request, _("Comment created succesfully."))
            return redirect("post_detail", post_id=post_id)
        return detail(request, post_id, reply_form=form)
    else:
        return redirect("post_detail", post_id=post_id)

def approve_comment(request, activation_key):
    """
    Approve anonymous users comment with given activation_key
    """
    # get comment with given activation key
    c = get_object_or_404(Comment, activation_key=activation_key)
    
    # approve comment
    c.approve()
    
    # redirect to homepage
    messages.info(request, _("Comment approved."))

    return redirect("message")
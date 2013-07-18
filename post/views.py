from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User

from comment.forms import CommentForm, ReplyForm
from post.models import Post
from post.forms import PostForm
from comment.models import Comment

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.user, 
                        request.POST, 
                        request.FILES)
        if form.is_valid():
            # save form, create post
            post = form.save()

            # add resize image task to celery
            post.resize_post_image.delay(post)

            # add notify admin task to celery
            # post.notify_admin.delay(post)
            post.approve()

            messages.success(request, _("Post created succesfully."))
            return redirect("my_posts")
    else:
        form = PostForm(request.user)

    return render(request, 'post/create_post.html', {
        'form': form,
    })

def edit_post(request, post_id):
    post = get_object_or_404(Post, 
                             pk=post_id,
                             user=request.user)

    if request.method == 'POST':
        form = PostForm(request.user,
                        request.POST, 
                        request.FILES, 
                        instance=post)
        if form.is_valid():
            # update post
            post = form.save()

            # add resize image task to celery
            post.resize_post_image.delay(post)

            # add notify admin task to celery
            post.notify_admin.delay(post)
            
            messages.success(request, _("Post updated succesfully."))
            return redirect("my_posts")
    else:
        form = PostForm(request.user, instance=post)

    return render(request, 'post/edit_post.html', {
        'form': form,
    })

def detail(request, post_id, comment_form=None, reply_form=None):
    # get (active and approved) post or raise 404
    post = get_object_or_404(Post, 
                             pk=post_id, 
                             is_active=True, 
                             is_approved=True)

    # get (active and approved) post comments
    comments = post.get_comments()

    # get (active and approved) comment replies
    replies = post.get_replies()

    # if form is not None, this method calling from comment.views.add_comment
    if not comment_form:
        comment_form = CommentForm(request.user)

    if not reply_form:
        reply_form = ReplyForm(request.user)
    
    return render(request, 'post/detail.html', {
        'post': post, 
        'comment_form': comment_form, 
        'reply_form': reply_form,
        'comments': comments,
        'replies': replies
    })

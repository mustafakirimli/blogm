from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User

from comment.forms import CommentForm, ReplyForm
from post.models import Post
from post.forms import PostForm
from post.tasks import resize_post_image
from post.utils import sort_replies
from comment.models import Comment
from decorators import cache_on_auth

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, 
                        request.FILES)
        if form.is_valid():
            # set user to form instance
            form.instance.user = request.user

            # save form, create post
            post = form.save()

            # add resize image task to celery
            resize_post_image.delay(post)

            messages.success(request, _("Post created succesfully."))
            return redirect("my_posts")
    else:
        form = PostForm()

    return render(request, 'post/create_post.html', {
        'form': form,
    })

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, 
                             pk=post_id,
                             user=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, 
                        request.FILES, 
                        instance=post)
        if form.is_valid():
            # set user to form instance
            form.instance.user = request.user
            
            # update post
            post = form.save()

            # add resize image task to celery
            resize_post_image.delay(post)

            messages.success(request, _("Post updated succesfully."))
            return redirect("my_posts")
    else:
        form = PostForm(instance=post)

    return render(request, 'post/edit_post.html', {
        'form': form,
    })


@cache_on_auth(600)
def detail(request, post_id, comment_form=None, reply_form=None):
    # get (active and approved) post or raise 404
    post = get_object_or_404(Post, 
                             pk=post_id, 
                             is_active=True, 
                             is_approved=True)

    # get (active and approved) post comments
    comments = post.get_comments()

    # get (active and approved) comment replies
    replies = sort_replies(replies = post.get_replies())

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

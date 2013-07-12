from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from comment.forms import CommentForm
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
            post.notify_admin.delay(post)

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

def detail(request, post_id, form=None):
    # get (active and approved) post or raise 404
    post = get_object_or_404(Post, 
                             pk=post_id, 
                             is_active=True, 
                             is_approved=True)

    # get (active and approved) post comments
    comments = post.get_comments()

    # new comment form
    post_type = ContentType.objects.get(app_label="post", model="post")
    initial = {"parent_id": post_id, "comment_type": post_type.id}

    # if form is not None, this method calling from comment.views.add_comment
    if not form:
        form = CommentForm(request.user, initial=initial)
    
    return render(request, 'post/detail.html', {
        'post': post, 
        'form': form, 
        'comments': comments
    })

def approve_post(request, activation_key):
    try:
        # get post with given activation key
        p = get_object_or_404(Post, activation_key=activation_key)
        # approve post
        p.approve()
        # redirect to homepage
        messages.info(request, _("Post approved."))
    except:
        messages.info(request, _("Post approve problem!"))

    return redirect("home")

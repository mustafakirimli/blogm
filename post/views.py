from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from post.forms import PostForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from comment.forms import CommentForm
from post.models import Post
from comment.models import Comment
from django.contrib.auth.models import User

def index(request):
    return HttpResponse("Blog Posts!")

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.activation_key = User.objects.make_random_password()
            post.is_active = True
            post.is_approved = False
            post.save()
            post.resize_post_image.delay(post)
            post.notify_admin.delay(post)
            messages.success(request, _("Post created succesfully."))
            return HttpResponseRedirect(reverse("my_posts"))
    else:
        form = PostForm()

    return render(request, 'post/create_post.html', {
        'form': form,
    })

def edit_post(request, post_id):
    post = get_object_or_404(Post, 
                             pk=post_id,
                             user=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.is_approved = False
            post.save()
            post.notify_admin.delay(post)
            post.resize_post_image.delay(post)
            messages.success(request, _("Post updated succesfully."))
            return HttpResponseRedirect(reverse("my_posts"))
    else:
        form = PostForm(instance=post)

    return render(request, 'post/edit_post.html', {
        'form': form,
    })

def detail(request, post_id):
    # get (active and approved) post or raise 404
    post = get_object_or_404(Post, 
                             pk=post_id, 
                             is_active=True, 
                             is_approved=True)

    # get (active and approved) post comments
    comments = Comment.objects.filter(parent_id=post_id, 
                                      is_active=True, 
                                      is_approved=True)

    # new comment form
    post_type = ContentType.objects.get(app_label="post", model="post")
    initial = {"parent_id":post_id, 
               "comment_type":post_type.id
               }
    form = CommentForm(initial=initial)
    
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

    return HttpResponseRedirect(reverse("home"))

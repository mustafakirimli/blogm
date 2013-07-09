from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from post.forms import PostForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

def index(request):
    return HttpResponse("Blog Posts!")

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            post.resize_post_image.delay(post)
            messages.success(request, _("Post created succesfully."))
            return HttpResponseRedirect(reverse("my_posts"))
    else:
        form = PostForm()

    return render(request, 'post/create_post.html', {
        'form': form,
    })

def edit_post(request, post_id):
    return HttpResponse("Edit Post!")

def detail(request, post_id):
    return HttpResponse("Post Detail!")
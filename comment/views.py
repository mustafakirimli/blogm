from django.http import HttpResponse
from comment.forms import CommentForm
from django.http import HttpResponseRedirect
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from comment.models import Comment
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

def index(request):
    return HttpResponse("Welcome to my blog!")

def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.comment_type = ContentType.objects.get(app_label="post", model="post")
            comment.activation_key = User.objects.make_random_password()
            comment.is_approved = False
            comment.save()
            comment.notify_admin.delay(comment)
            messages.success(request, _("Comment created succesfully."))
        return HttpResponseRedirect(reverse("post_detail", kwargs={'post_id':request.POST.get("parent_id")}))

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

    return HttpResponseRedirect(reverse("home"))
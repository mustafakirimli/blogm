from django.http import HttpResponse
from comment.forms import CommentForm
from django.http import HttpResponseRedirect
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

def index(request):
    return HttpResponse("Welcome to my blog!")

def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.comment_type = ContentType.objects.get(app_label="post", model="post")
            comment.save()
            messages.success(request, _("Comment created succesfully."))
        return HttpResponseRedirect(reverse("post_detail", kwargs={'post_id':request.POST.get("parent_id")}))

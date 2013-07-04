from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class Post(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    description = models.CharField(max_length=255)
    image = models.ImageField(_("Post Image"), upload_to="upload/post/", blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True,blank=True)

    def getLatestPost(self, count=3):
        posts = Post.objects.filter(is_active=True, is_approved=True).order_by("-id")[:count]
        return posts

    def getMainPost(self, count=1):
        exclude_ids = [p.id for p in self.getLatestPost()]
        posts = Post.objects.filter(is_active=True, is_approved=True).exclude(id__in=exclude_ids).order_by('?')[:count]
        return posts

    def isVisible(self):
        return self.is_active == True and self.is_approved == True

    def __unicode__(self):
        return self.name
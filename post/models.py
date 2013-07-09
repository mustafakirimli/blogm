from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from celery import task
import PIL
from PIL import Image
import settings

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

    @task
    def resize_post_image(self):
        image_path = "%s/%s" %(settings.MEDIA_ROOT, self.image)

        basewidth = 200
        image = Image.open(image_path)
        # ImageOps compatible mode
        if image.mode not in ("L", "RGB"):
            image = image.convert("RGB")

        wpercent = (basewidth/float(image.size[0]))
        hsize = int((float(image.size[1])*float(wpercent)))
        image = image.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
        image.save(image_path)
        return True

    class Meta:
        app_label = 'post'

    def __unicode__(self):
        return self.name
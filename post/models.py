import PIL
import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from celery import task
from PIL import Image
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import get_template 
from django.template import Context
from comment.models import Comment

class Post(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    description = models.CharField(max_length=255)
    image = models.ImageField(_("Post Image"), upload_to="upload/post/", blank=True, null=True)
    activation_key =  models.CharField(max_length=30, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True,blank=True)

    @staticmethod
    def get_latest_post(count=3):
        posts = Post.objects.filter(is_active=True, is_approved=True).order_by("-id")[:count]
        return posts

    @staticmethod
    def get_main_post(count=1):
        exclude_ids = [p.id for p in Post.get_latest_post()]
        posts = Post.objects.filter(is_active=True, is_approved=True).exclude(id__in=exclude_ids).order_by('?')[:count]
        return posts

    def get_comments(self):
        content_type = Comment.type_post()
        post_type_id = content_type.id
        return Comment.objects.filter(is_active=True, 
                                     is_approved=True, 
                                     comment_type=post_type_id,
                                     parent_id=self.id)

    def is_visible(self):
        return self.is_active == True and self.is_approved == True

    @task
    def resize_post_image(self):
        if not self.image:
            return True

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

    @task
    def notify_admin(self):
        site = Site.objects.get_current()
        # send email with template
        send_mail(
            _('Please approve new post!'),
            get_template('email/post/approve_post.html').render(
                Context({
                    'site': site,
                    'user': self.user,
                    'post': self
                })
            ),
            '',
            settings.ADMINS,
            fail_silently = True
        )
        return True

    def approve(self):
        self.is_approved = True
        self.save()
        return self.is_approved

    class Meta:
        app_label = 'post'

    def __unicode__(self):
        return self.name
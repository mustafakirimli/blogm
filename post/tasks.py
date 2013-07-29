import settings
import PIL

from celery import task
from PIL import Image
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import get_template 
from django.contrib.sites.models import Site
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse

from blogm.utils import purge_url_cache
from post.models import Post
from comment.models import Comment
from post.utils import purge_comment_cache

@task
def resize_post_image(post):
    """
    Resize given posts image
    """
    if not post.image:
        return True

    image_path = "%s/%s" %(settings.MEDIA_ROOT, post.image)

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

def purge_post_cache(sender, **kwargs):
    post = kwargs["instance"]

    if not isinstance(post, Post):
        post = post.parent 
    
    # purge post cache
    purge_url_cache(reverse("post_detail", args=[post.id]))

    # purge comment cache    
    purge_comment_cache(post_id=post.id)

post_save.connect(purge_post_cache, sender=Post, dispatch_uid="pasppc")
post_save.connect(purge_post_cache, sender=Comment, dispatch_uid="pasppc2")
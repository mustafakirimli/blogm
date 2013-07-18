import settings
import PIL

from celery import task
from PIL import Image
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import get_template 
from django.contrib.sites.models import Site

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


from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
from django.dispatch import receiver

from blogm.utils import purge_url_cache, purge_cache
from post.models import Post

@receiver(post_save, sender=Post)
def purge_homepage_cache(sender, **kwargs):
    #post = kwargs["instance"]
    
    # purge post cache
    purge_url_cache(reverse("home"))
    purge_cache("latest_posts")
    purge_cache("main_post")
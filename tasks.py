from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse

from blogm.utils import purge_url_cache, purge_cache
from post.models import Post

def purge_homepage_cache(sender, **kwargs):
    #post = kwargs["instance"]
    
    # purge post cache
    purge_url_cache(reverse("home"))
    purge_cache("latest_posts")
    purge_cache("main_post")

pre_save.connect(purge_homepage_cache, sender=Post, dispatch_uid="pbsphc")
post_save.connect(purge_homepage_cache, sender=Post, dispatch_uid="pasphc")
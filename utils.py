import hashlib
from django.conf import settings
from django.core.cache import cache
from django.utils.encoding import iri_to_uri
from django.utils.translation import get_language

def get_template_cache_key(cache_name, identify=None):
    """
    Returns template cache key
    """
    if identify is None:
        identify = hashlib.md5()
    else:
        identify = hashlib.md5(str(identify))

    cache_key = 'template.cache.%s.%s' % (cache_name, identify.hexdigest())
    
    return cache_key

def get_url_cache_key(url, language=None, key_prefix=None):
    if key_prefix is None:
        key_prefix = settings.CACHE_MIDDLEWARE_KEY_PREFIX
    
    ctx = hashlib.md5()
    path = hashlib.md5(iri_to_uri(url))
    
    cache_key = 'views.decorators.cache.cache_page.%s.%s.%s.%s' % (
        key_prefix, 
        'GET', 
        path.hexdigest(), 
        ctx.hexdigest()
    )
    
    if settings.USE_I18N:
        cache_key += '.%s' % (language or get_language())

    return cache_key

def purge_cache(key, key_prefix=settings.CACHE_MIDDLEWARE_KEY_PREFIX):
    # set cache key prefix
    cache.key_prefix = key_prefix

    # delete cache
    cache.delete(key)

def purge_template_cache(cache_name, identify):
    cache_key = get_template_cache_key(cache_name, identify=identify)
    purge_cache(cache_key)

def purge_url_cache(url):
    # get cache key
    url_key_visitor = get_url_cache_key(url, key_prefix="_auth_false_")
    url_key_member = get_url_cache_key(url, key_prefix="_auth_true_")

    purge_cache(url_key_visitor, "_auth_false_")
    purge_cache(url_key_member, "_auth_true_")

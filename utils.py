import hashlib
from django.conf import settings
from django.core.cache import cache

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

def purge_cache(key, key_prefix=None):
    if key_prefix is None:
        key_prefix = settings.CACHE_MIDDLEWARE_KEY_PREFIX

    # set cache key prefix
    cache.key_prefix = key_prefix

    # delete cache
    cache.delete(key)

def purge_template_cache(cache_name, identify):
    cache_key = get_template_cache_key(cache_name, identify=identify)
    purge_cache(cache_key)
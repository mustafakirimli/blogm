import hashlib
from django.utils.encoding import iri_to_uri
from django.conf import settings
from django.utils.translation import get_language
from django.core.cache import cache

def url_cache_key(url, language=None, key_prefix=None):
    if key_prefix is None:
        key_prefix = settings.CACHE_MIDDLEWARE_KEY_PREFIX
    ctx = hashlib.md5()
    path = hashlib.md5(iri_to_uri(url))
    cache_key = 'views.decorators.cache.cache_page.%s.%s.%s.%s' % (
        key_prefix, 'GET', path.hexdigest(), ctx.hexdigest())
    if settings.USE_I18N:
        cache_key += '.%s' % (language or get_language())
    return cache_key

def purge_cache(key, key_prefix=None):
    if key_prefix is None:
        key_prefix = settings.CACHE_MIDDLEWARE_KEY_PREFIX

    # set cache key prefix
    cache.key_prefix = key_prefix

    # delete cache
    cache.delete(key)

def url_cache_purge(url):
    # get cache key
    url_key_visitor = url_cache_key(url, key_prefix="_auth_false_")
    url_key_member = url_cache_key(url, key_prefix="_auth_true_")

    purge_cache(url_key_visitor, "_auth_false_")
    purge_cache(url_key_member, "_auth_true_")

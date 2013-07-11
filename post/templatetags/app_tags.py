from django import template
import hashlib

register = template.Library()

@register.filter(name='md5')
def md5_string(value):
    return hashlib.md5(value).hexdigest()

@register.filter(name='get_hash')
def get_hash(value):
    try:
        return value.__hash__()
    except Exception, e:
        print e
        return None
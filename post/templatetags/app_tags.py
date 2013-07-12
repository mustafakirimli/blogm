import hashlib

from django import template
from comment.models import Comment

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

@register.filter(name='get_replies')
def get_replies(value):
    try:
        comment = Comment.objects.get(id=value)
        replies = comment.get_replies()
        return replies
    except Exception, e:
        print e
        return None

import hashlib

from django import template
from comment.models import Comment

register = template.Library()

@register.filter(name='md5')
def md5_string(value):
    return hashlib.md5(value).hexdigest()

@register.filter(name='get_hash')
def get_hash(value):
    return value.__hash__()

@register.filter(name='get_dict_value')
def get_dict_value(value, arg):
	return arg[value] if value in arg else False
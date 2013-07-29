from django.views.decorators.cache import cache_page
from functools import wraps
from django.utils.decorators import available_attrs
from django.contrib.messages.api import get_messages
from django.contrib import messages

def cache_on_auth(timeout):
    """
    Cache a view with user authenticated status
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            # get request message object
            storage = messages.get_messages(request)

            # if request object hasn't message, cache given view
            if not storage:
                # user auth status
                is_auth = request.user.is_authenticated()

                # if user is authenticated returns "_auth_true_" prefix
                # if not returns "_auth_false_"
                key_prefix = "_auth_%s_" % str(is_auth).lower()

                # return cache_page decorator
                return cache_page(timeout, 
                                  key_prefix=key_prefix)(view_func)(request, *args, **kwargs)
            else:
                # return function without cache_page decorator
                return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

from django.views.decorators.cache import cache_page
from functools import wraps
from django.utils.decorators import available_attrs
from django.contrib import messages

def cache_on_auth(timeout):
    """
    Cache a view with user authenticated status
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            # user auth status
            is_auth = request.user.is_authenticated()

            # if user is authenticated returns "_auth_true_" prefix
            # if not returns "_auth_false_"
            key_prefix = "_auth_%s_" % str(is_auth).lower()

            # return cache_page decorator
            return cache_page(timeout, 
                              key_prefix=key_prefix)(view_func)(request, *args, **kwargs)
        return _wrapped_view
    return decorator

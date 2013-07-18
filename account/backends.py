from django.contrib.auth.models import User, check_password
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

class EmailAuthBackend(object):
    """
    Email Authentication Backend
    """
    
    def authenticate(self, username=None, password=None):
        """ Authenticate a user based on email address as the user name. """
        user = User.objects.get(email=username)
        if not user.check_password(password):
            raise ValidationError(_("Invalid email/password"))
        if not user.is_active:
            raise ValidationError(_("Disabled account. Please contact blog admin"))
        if not user.get_profile().is_approved:
            raise ValidationError(_("Not activated account! Please activate your account"))
        return user

    def get_user(self, user_id):
        """ Get a User object from the user_id. """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
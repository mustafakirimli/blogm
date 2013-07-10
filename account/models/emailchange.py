from django.db import models
from django.contrib.auth.models import User
from celery import task
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import get_template 
from django.template import Context
from django.utils.translation import ugettext as _

class EmailChange(models.Model):
    # user
    user = models.ForeignKey(User)
    
    # new email address
    email = models.CharField(max_length=75)
    
    # email change requests activation key
    activation_key = models.CharField(max_length=30)
    
    # email change request status 
    # True: pending request
    # False: approved request
    is_active = models.BooleanField(default=False)

    # email change request created time
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def pending_requests(user):
        """
        returns active -pending- email change requests for given user
        """
        change = EmailChange.objects.filter(user=user, is_active=True)
        return change[0] if change else False

    @task
    def send_activation_email(self):
        """
        send email change confirmation email to new address.
        """
        site = Site.objects.get_current()
        # send email with template
        send_mail(
            _('Please confirm email change request!'),
            get_template('email/account/email_activate.html').render(
                Context({
                    'site': site,
                    'user': self.user,
                    'change': self
                })
            ),
            '',
            [self.email],
            fail_silently = True
        )
        return True

    class Meta:
        app_label = 'account'

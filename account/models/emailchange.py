from django.db import models
from django.contrib.auth.models import User
from celery import task
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import get_template 
from django.template import Context
from django.utils.translation import ugettext as _

class EmailChange(models.Model):
    user = models.ForeignKey(User)
    email = models.CharField(max_length=75)
    activation_key =  models.CharField(max_length=30)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def pending_requests(user):
        change = EmailChange.objects.filter(user=user, is_active=True)
        return change[0] if change else False

    @task
    def send_activation_email(self):
        site = Site.objects.get_current()
        # send email with template
        send_mail(
            _('Please confirm email change!'),
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
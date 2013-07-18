from celery import task
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import get_template 
from django.template import Context
from django.utils.translation import ugettext as _

@task
def send_account_activation_email(profile):
    """
    Sends account activation email to user
    """
    # get current site for url
    site = Site.objects.get_current()
    # send email with template
    send_mail(
        _('Thanks for signing up!'),
        get_template('email/account/activate.html').render(
            Context({
                'site': site,
                'user': profile.user,
                'profile': profile
            })
        ),
        '',
        [profile.user.email],
        fail_silently = True
    )
    return True

@task
def send_email_change_validation_email(emailchange):
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
                'user': emailchange.user,
                'change': emailchange
            })
        ),
        '',
        [emailchange.email],
        fail_silently = True
    )
    return True
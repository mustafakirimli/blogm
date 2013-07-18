from celery import task
from django.utils.translation import ugettext as _
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.template.loader import get_template 
from django.template import Context

@task
def send_email_validation(comment):
    """
    New comment email validaton for anonymous user
    """
    site = Site.objects.get_current()
    # send email with template
    send_mail(
        _('Please approve email address for your comment!'),
        get_template('email/comment/approve_comment.html').render(
            Context({
                'site': site,
                'comment': comment
            })
        ),
        '',
        [comment.email,],
        fail_silently = True
    )
    return True
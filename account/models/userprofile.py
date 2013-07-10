from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _
from celery import task
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import get_template 
from django.template import Context

class UserProfile(models.Model):
    # user
    user = models.OneToOneField(User)

    # is approved -activated-
    is_approved = models.BooleanField(default=False)

    # activation key
    activation_key = models.CharField(max_length=30, null=True)

    # profile pictures -resizing to 100px-
    image = models.ImageField(_("Profile Pic"), 
                              upload_to="upload/profile/", 
                              blank=True, 
                              null=True)
    
    # gender
    GENDER_CHOICES = (
        ('M', _('Male')),
        ('F', _('Female')),
    )
    gender = models.CharField(max_length=1, 
                              choices=GENDER_CHOICES, 
                              null=True, 
                              blank=True)

    def __str__(self):
        return "%s's profile" % self.user

    def activate(self):
        """
        Activate user -profile-
        """
        self.is_approved = True
        self.save()
        return self.is_approved

    @task
    def send_activation_email(self):
        # get current site for url
        site = Site.objects.get_current()
        # send email with template
        send_mail(
            _('Thanks for signing up!'),
            get_template('email/account/activate.html').render(
                Context({
                    'site': site,
                    'user': self.user,
                    'profile': self
                })
            ),
            '',
            [self.user.email],
            fail_silently = True
        )
        return True

    class Meta:
        app_label = 'account'

# user <-> profile connection
def create_user_profile(sender, instance, created, **kwargs):  
    if created:
       profile, created = UserProfile.objects.get_or_create(user=instance)  

post_save.connect(create_user_profile, sender=User) 
User.profile = property(lambda u: u.get_profile() )
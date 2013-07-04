from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    is_approved = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=30, null=True)
    image = models.ImageField(_("Profile Pic"), upload_to="upload/profile/", blank=True, null=True)
    GENDER_CHOICES = (
        ('M', _('Male')),
        ('F', _('Female')),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)

    def __str__(self):
        return "%s's profile" % self.user 

def create_user_profile(sender, instance, created, **kwargs):  
    if created:
       profile, created = UserProfile.objects.get_or_create(user=instance)  
 
post_save.connect(create_user_profile, sender=User) 
 
User.profile = property(lambda u: u.get_profile() )


class EmailChange(models.Model):
    user = models.ForeignKey(User)
    email = models.CharField(max_length=75)
    activation_key =  models.CharField(max_length=30)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
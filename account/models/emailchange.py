from django.db import models
from django.contrib.auth.models import User

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

    class Meta:
        app_label = 'account'
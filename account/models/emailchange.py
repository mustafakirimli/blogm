from django.db import models
from django.contrib.auth.models import User

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
    is_confirmed = models.BooleanField(default=True)

    # email change request created time
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def pending_requests(user):
        """
        returns active -pending- email change requests for given user
        """
        change = EmailChange.objects.filter(user=user, is_confirmed=True)
        return change[0] if change else False

    @staticmethod
    def create_request(user, email):
        # generate random hash
        activation_key = User.objects.make_random_password()

        # set all the old requests to false for this user
        EmailChange.objects.filter(user=user).update(is_confirmed=False)

        # create request
        email_change = EmailChange.objects.create(user=user, 
                                                  email=email, 
                                                  is_confirmed=True, 
                                                  activation_key=activation_key)
        return email_change

    def activate_email(self):
        """
        activate email change requests -mark as completed-
        """
        # set new email address to user object
        self.user.email = self.email
        self.user.save()

        # set status to false
        self.is_confirmed = False
        self.save()

        # return status
        return self.is_confirmed

    class Meta:
        app_label = 'account'

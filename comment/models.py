from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _
from celery import task
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import get_template 
from django.template import Context
import settings

class Comment(models.Model):
    limit = (models.Q(app_label='post', model='post') |                         
             models.Q(app_label='comment', model='comment'))
    comment_type = models.ForeignKey(ContentType, limit_choices_to=limit)
    parent_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('comment_type', 'parent_id')
    fullname = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField()
    activation_key =  models.CharField(max_length=30, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def getActiveComments(self):
        return Comment.object.filter(status=True, approved=True)

    def getActiveUserComments(self, user_id):
        return Comment.object.filter(status=True, approved=True, user_id=user_id)

    def getActiveBlogComments(self):
        return Comment.object.filter(status = True, approved=True, comment_type=models.Q(model='post'))

    def getActiveCommentReplies(self):
        return Comment.object.filter(status = True, approved=True, comment_type=models.Q(model='comment'))


    @task
    def notify_admin(self):
        site = Site.objects.get_current()
        # send email with template
        send_mail(
            _('Please approve new comment!'),
            get_template('email/comment/approve_comment.html').render(
                Context({
                    'site': site,
                    'comment': self
                })
            ),
            '',
            settings.ADMINS,
            fail_silently = True
        )
        return True

    def approve(self):
        self.is_approved = True
        self.save()
        return self.is_approved
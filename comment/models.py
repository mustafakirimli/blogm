from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Comment(models.Model):
    limit = (models.Q(app_label='post', model='post') |                         
             models.Q(app_label='comment', model='comment'))
    comment_type = models.ForeignKey(ContentType, limit_choices_to=limit)
    parent_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('comment_type', 'parent_id')
    fullname = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField()
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
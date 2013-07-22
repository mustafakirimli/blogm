import settings

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse

from post.utils import purge_comment_cache

class Comment(models.Model):
    post = models.ForeignKey('post.Post')
    limit = (models.Q(app_label='post', model='post') |                         
             models.Q(app_label='comment', model='comment'))
    comment_type = models.ForeignKey(ContentType, limit_choices_to=limit)
    parent_id = models.PositiveIntegerField()
    parent = generic.GenericForeignKey('comment_type', 'parent_id')
    fullname = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField()
    activation_key =  models.CharField(max_length=30, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def approve(self):
        """
        Approve comment
        """
        self.is_approved = True
        self.save()

        # purge post comment cache
        purge_comment_cache(post_id=self.post.id)
        
        return self.is_approved
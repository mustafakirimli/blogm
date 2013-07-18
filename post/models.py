from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _

from comment.models import Comment
from post.managers import PostManager

class Post(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    description = models.CharField(max_length=255)
    image = models.ImageField(_("Post Image"), 
                              upload_to="upload/post/", 
                              blank=True, 
                              null=True)
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True,blank=True)

    objects = PostManager()

    def get_comments(self):
        """
        Get all comment for this post
        """
        type = ContentType.objects.get_for_model(self)
        return Comment.objects.filter(is_active=True, 
                                     is_approved=True, 
                                     post=self,
                                     comment_type=type
                                     ).order_by("id")

    def get_replies(self):
        """
        Get this post's replies.
        returns replies grouped by parent_id
        """
        type = ContentType.objects.get_for_model(Comment)
        objects = Comment.objects.filter(is_active=True, 
                                     is_approved=True, 
                                     post=self,
                                     comment_type=type
                                     ).order_by("id")
        
        replies = {}
        for r in objects:
            if not r.parent_id in replies:
                replies[r.parent_id] = []
            replies[r.parent_id].append(r)

        return replies

    class Meta:
        app_label = 'post'
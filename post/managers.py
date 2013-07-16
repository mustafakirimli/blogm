from django.db import models

class PostManager(models.Manager):
    def latest_posts(self):
        posts = self.filter(is_active=True, 
                            is_approved=True).order_by('-id')
        return posts

    def random_posts(self):
        posts = self.filter(is_active=True, 
                            is_approved=True).order_by('-id')
        return posts
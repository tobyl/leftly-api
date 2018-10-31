from django.db import models
from .constants import POST_TYPE

class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    type = models.CharField(choices=POST_TYPE, default='Post', max_length=32)

    class Meta:
        ordering = ('created',)

from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


class Like(models.Model):
    """
    Like model, related to 'owner' and 'post'.
    'owner' is a User instance and 'post' is a Post instance.
    'unique_together' makes sure a user can't like the same post twice.
    https://docs.djangoproject.com/en/3.2/ref/models/fields/#django.db.models.ForeignKey.related_name
    https://docs.djangoproject.com/en/3.2/ref/models/options/#unique-together
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, related_name='likes', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        # this is to avoid the post to be liked multiple time bu same user and will cause integrity error
        unique_together = ['owner', 'post']

    def __str__(self):
        return f'{self.owner} {self.post}'
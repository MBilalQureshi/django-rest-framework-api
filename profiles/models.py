from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Modal):
    owner = models.OneToOneField(User, on_delete=modals.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank_true)
    image = models.ImageField(
        upload_to='images/', default='../default_profile_oojj4p'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"
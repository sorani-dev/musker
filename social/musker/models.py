from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """User Profile Model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        'self',
        related_name='followed_by',
        symmetrical=False,
        blank=True)

    def __str__(self):
        return self.__repr__();

    def __repr__(self):
        return self.user.username

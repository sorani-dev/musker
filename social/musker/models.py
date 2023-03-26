from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create Meep Model
class Meep(models.Model):

    user = models.ForeignKey(
        User, related_name="meeps",
        on_delete=models.DO_NOTHING
    )
    
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.user} "
            f"{self.created_at:%Y-%m-%d %H:%M:%S} "
            f"{self.body}..."
        )

    def __repr__(self):
        return self.__str__()
    

class Profile(models.Model):
    """User Profile Model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        'self',
        related_name='followed_by',
        symmetrical=False,
        blank=True)
    
    updated_at = models.DateTimeField(User, auto_now=True)

    def __str__(self):
        return self.__repr__();

    def __repr__(self):
        return self.user.username


# Create Profile when new User signs up
@receiver(post_save, sender=User)
def create_profile(sender: models.base.ModelBase, instance: User, created: bool, **kwargs) -> None:
    print(type(sender), type(instance), type(created))
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        # Have the user follow themselves
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

# post_save.connect(create_profile, sender=User)

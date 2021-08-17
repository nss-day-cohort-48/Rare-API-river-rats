from django.db import models
from django.contrib.auth.models import User  # pylint:disable=(imported-auth-user)


class RareUser(models.Model):
    """RareUser Model
    Args:
        models (OneToOneField): The user information for the RareUser
        bio (CharField): The bio of the user
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50)
    profile_image_url = models.CharField(max_length=50)
    created_on = models.DateField()

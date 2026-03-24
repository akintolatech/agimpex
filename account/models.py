from django.db import models
from django.conf import settings


# Create your models here.
class Profile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    photo = models.ImageField(
        upload_to='photos',
        blank=True,
        null=True
    )

    phone_number = models.CharField(max_length=11, null=True, blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

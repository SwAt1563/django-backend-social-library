from django.db import models
from autoslug import AutoSlugField
from django.conf import settings
from django.urls import reverse
# Create your models here.


class Profile(models.Model):
    # first and last name in users
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    slug = AutoSlugField(unique=True, always_update=True, populate_from='user')
    image = models.ImageField(null=True, blank=True, upload_to='users_images/')
    # black: can form be empty
    # charfield and textfield can't be null just empty string
    phone = models.CharField(blank=True, max_length=20)
    age = models.PositiveIntegerField(null=True, blank=True)
    address = models.CharField(max_length=200,  blank=True)
    status = models.CharField(max_length=200,  blank=True)
    about_me = models.CharField(max_length=500, blank=True)


    def __str__(self):
        return self.user.username

    def get_absolute_path(self):
        return reverse('user_profile:profile', args=[self.slug])

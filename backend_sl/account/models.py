from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models import Count
# Create your models here.

def validate_email(email):
    import re
    if not re.match(r'^[0-9]{7}@student\.birzeit\.edu$', email):
        raise ValidationError('wrong email format')

class UserAccount(AbstractUser):
    question = models.CharField(max_length=200, null=True, blank=True)
    answer = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(unique=True, max_length=100, validators=[validate_email])
    created = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)



    # this used by profile slug
    def __str__(self):
        return self.username

    # for update slug when change the username
    def save(self, *args, **kwargs):
        if hasattr(self, 'profile'):
            self.profile.save()
        super().save(*args, **kwargs)

    @property
    def get_total_user_stars(self):
        if hasattr(self, 'posts'):
            return self.posts.aggregate(total=Count('stars'))['total']
        return 0



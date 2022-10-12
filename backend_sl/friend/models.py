from django.db import models
from django.conf import settings
# Create your models here.


class UserFollowing(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    following_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_id} follow {self.following_user_id}'

    class Meta:
        # for don't let user1 follow user2 twice times
        # it work like indexes in the database
        constraints = (models.UniqueConstraint(fields=('user_id', 'following_user_id'), name='unique_followers'),)
        ordering = ("-created", )
from django.db import models
from django.conf import settings
# Create your models here.


class Notification(models.Model):
    content = models.CharField(max_length=200)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                  related_name='my_sent_notifications')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                  related_name='my_received_notifications')

    def __str__(self):
        return f'{self.from_user} send: {self.content}, to: {self.to_user}'
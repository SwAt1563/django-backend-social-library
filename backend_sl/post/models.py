from django.db import models
from autoslug import AutoSlugField
from django.urls import reverse
from django.conf import settings
from django.core.validators import ValidationError


# Create your models here.
def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ('.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class Post(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        COMPLETED = "COMPLETED", "Completed"
        BLOCKED = "BLOCKED", "Blocked"

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    file = models.FileField(upload_to='posts_files/', validators=(validate_file_extension,))
    slug = AutoSlugField(unique=True, always_update=True, populate_from='title')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default=Status.PENDING, choices=Status.choices)

    def __str__(self):
        return self.title

    def get_absolute_path(self):
        return reverse('post:post_detail', args=[self.slug])

    @property
    def get_post_stars_count(self):
        if hasattr(self, 'stars'):
            return self.stars.count()
        return 0

    @property
    def posted_by(self):
        return self.user.get_full_name


class Comment(models.Model):
    comment = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} comment on {self.post.title} with this comment: {self.comment}'


class Star(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='stars')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stars')


    class Meta:
        # for don't let user make more than one star on post
        # it work like indexes in the database
        constraints = (models.UniqueConstraint(fields=('post', 'user'), name='unique_star'),)


    def __str__(self):
        return f'user: {self.user} make star on post: {self.post.title}'



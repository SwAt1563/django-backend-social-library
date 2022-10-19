# Generated by Django 4.0 on 2022-10-18 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_post_status'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='star',
            constraint=models.UniqueConstraint(fields=('post', 'user'), name='unique_star'),
        ),
    ]
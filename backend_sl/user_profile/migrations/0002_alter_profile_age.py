# Generated by Django 4.1 on 2022-10-11 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]

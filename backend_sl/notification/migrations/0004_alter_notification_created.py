# Generated by Django 4.0 on 2022-10-13 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0003_alter_notification_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

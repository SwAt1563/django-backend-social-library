# Generated by Django 4.1 on 2022-10-11 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed'), ('BLOCKED', 'Blocked')], default='PENDING', max_length=20),
        ),
    ]

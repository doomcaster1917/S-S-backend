# Generated by Django 4.2 on 2023-05-27 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0013_remove_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar_url',
            field=models.CharField(default=False, max_length=455),
        ),
    ]
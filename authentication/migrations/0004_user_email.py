# Generated by Django 4.2 on 2023-05-17 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_user_first_name_user_last_name_user_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.CharField(default=False, max_length=255, unique=True),
        ),
    ]
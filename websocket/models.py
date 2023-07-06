from django.db import models
# from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, user_id, first_name, last_name, avatar_url, password=None):

        if user_id is None:
            raise TypeError('Users must have a user_id(instead username).')

        user = self.model(user_id=user_id, first_name=first_name, last_name=last_name, avatar_url=avatar_url)

        user.save()

        return user

    def create_superuser(self, user_id, password):

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.model(user_id=user_id)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.IntegerField(db_index=True, unique=True, default=None)
    first_name = models.CharField(max_length=255, default='User', blank=True)
    last_name = models.CharField(max_length=255, default='User', blank=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar_url = models.CharField(db_index=True, max_length=455)
    group = models.ForeignKey('websocket.Group', on_delete=models.SET_NULL, default=None, null=True)

    USERNAME_FIELD = 'user_id'
    # REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        """ Строковое представление модели (отображается в консоли) """
        return f'{self.first_name} {self.last_name} * {self.user_id}'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name

# Create your models here.

# User = get_user_model()

class Group(models.Model):
    owner_id = models.IntegerField(unique=True, default=None)

    def __str__(self) -> str:
        return f"Group {self.owner_id}"

    @staticmethod
    def add_group(owner_id, guest_id):
        group = Group(owner_id=owner_id)
        group.save()
        players = User.objects.filter(user_id__in=[owner_id, guest_id])
        for player in players:
            player.group = group
            player.save()


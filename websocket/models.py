from django.db import models
# from django.contrib.auth import get_user_model
from django.urls import reverse
from authentication.models import User
import authentication.models

# Create your models here.

# User = get_user_model()

class Group(models.Model):
    owner_id = models.IntegerField(unique=True, default=False, primary_key=True)
    members = models.ManyToManyField(User)

    def __str__(self) -> str:
        return f"Group {self.owner_id}"
    def add_group(self, owner_id, guest_id):
        group = Group(owner_id=owner_id)
        group.save()
        guest = authentication.models.User.objects.get(user_id=guest_id)
        owner = authentication.models.User.objects.get(user_id=owner_id)
        group.members.add(guest, owner)

    def delete_group(self, owner_id):
        Group.objects.filter(owner_id=owner_id).delete()


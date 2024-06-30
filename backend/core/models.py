from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class UserType(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    user_type = GenericForeignKey("content_type", "object_id")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_type")


class StaffUser(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="staff_user"
    )
    department = models.CharField(max_length=50)


class CustomerUser(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="customer_user"
    )
    address = models.CharField(max_length=100)


class AdminUser(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="admin_user"
    )

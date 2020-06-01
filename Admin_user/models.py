from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    mobile = models.CharField(max_length=20, unique=True, null=True)
    date_of_birth = models.DateTimeField(null=True)
    is_mobile = models.BooleanField(default=False, null=True)
    is_email = models.BooleanField(default=False, null=True)
    admin_img = models.ImageField(upload_to="media/", null=True)
    updated_at = models.DateTimeField(auto_now=True)
    account_id = models.IntegerField(unique=True, null=True)
    REQUIRED_FIELDS = ['mobile', 'date_of_birth', 'is_mobile', 'is_email', 'admin_img', 'updated_at', 'account_id']

    class Meta:
        verbose_name_plural = "User"








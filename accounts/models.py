from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_TYPES = (
        ("user", "user"),
        ("agent", "agent"),
    )

    user_type = models.CharField(max_length=5, choices=USER_TYPES, default="user")



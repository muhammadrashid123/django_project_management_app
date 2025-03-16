import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'  # Use email to login
    REQUIRED_FIELDS = ['username']  # Username required in addition to email

    def __str__(self):
        return self.email
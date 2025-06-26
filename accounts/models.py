from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_customer = models.BooleanField(default=True)  # If you'll later have vendors too
    # Add more fields if needed (e.g., phone number)

    def __str__(self):
        return self.username

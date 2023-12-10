from django.db import models
from ...management.models import CustomUser


class Admin(CustomUser):
    class RoleChoices(models.TextChoices):
        ADMIN = ("ADMIN", "Admin")
        SUPER_ADMIN = ("SUPER_ADMIN", "SuperAdmin")

    type = models.CharField(max_length=255, choices=RoleChoices.choices, default=RoleChoices.ADMIN)

    def __str__(self):
        return f"{self.name} - {self.phone_number}"

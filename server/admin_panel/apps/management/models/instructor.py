from django.db import models
from ...management.models import CustomUser, null_false, null_true


class Instructor(CustomUser):
    subject = models.ForeignKey('testing.Subject', on_delete=models.PROTECT, **null_true)
    solving_test_number = models.IntegerField(default=30)

    def __str__(self):
        return f"{self.id} - {self.phone_number}"

from django.db import models
from ...core.models import IsActiveCreatedUpdatedAtAbstract, null_false, null_true


class Statistics(IsActiveCreatedUpdatedAtAbstract):
    instructor = models.ForeignKey('management.Instructor', on_delete=models.PROTECT, **null_false)
    student = models.ForeignKey('management.Student', on_delete=models.PROTECT, **null_false)
    subject = models.ForeignKey('testing.Subject', on_delete=models.PROTECT, **null_false)
    section = models.ForeignKey('testing.Section', on_delete=models.PROTECT, **null_false)
    checked_tests = models.TextField(**null_false)
    total_tests = models.IntegerField(default=0)
    right_count = models.IntegerField(default=0)
    wrong_count = models.IntegerField(default=0)
    percentage = models.FloatField(default=0.0)
    solved_time = models.CharField(max_length=255, **null_true)

    def __str__(self):
        return f"{self.id}"

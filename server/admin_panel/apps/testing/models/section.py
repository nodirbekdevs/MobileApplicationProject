from django.db import models
from ...core.models import IsActiveCreatedUpdatedAtAbstract, null_false, null_true


class Section(IsActiveCreatedUpdatedAtAbstract):
    instructor = models.ForeignKey('management.Instructor', on_delete=models.PROTECT)
    subject = models.ForeignKey('testing.Subject', on_delete=models.PROTECT)
    title_uz = models.CharField(max_length=1000, **null_false)
    title_ru = models.CharField(max_length=1000, **null_false)
    description_uz = models.TextField(**null_true)
    description_ru = models.TextField(**null_true)
    total_tests = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id} - {self.title_uz}"

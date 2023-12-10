from django.db import models
from django.contrib.postgres.fields import ArrayField
from ...core.models import IsActiveCreatedUpdatedAtAbstract, null_false, null_true


class Test(IsActiveCreatedUpdatedAtAbstract):
    instructor = models.ForeignKey('management.Instructor', on_delete=models.PROTECT, **null_false)
    subject = models.ForeignKey('testing.Subject', on_delete=models.PROTECT, **null_false)
    section = models.ForeignKey('testing.Section', on_delete=models.PROTECT, **null_false)
    image = models.CharField(max_length=255, **null_true)
    question_uz = models.CharField(max_length=1000, **null_false)
    question_ru = models.CharField(max_length=1000, **null_false)
    variants_uz = ArrayField(models.CharField(max_length=1000, **null_false))
    variants_ru = ArrayField(models.CharField(max_length=1000, **null_false))
    correct_answer_uz = models.TextField(**null_false)
    correct_answer_ru = models.TextField(**null_false)
    is_testing = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}"

from django.db import models
from ...core.models import IsActiveCreatedUpdatedAtAbstract, null_false


class Subject(IsActiveCreatedUpdatedAtAbstract):
    title_uz = models.CharField(max_length=255, **null_false)
    title_ru = models.CharField(max_length=255, **null_false)
    description_uz = models.TextField(**null_false)
    description_ru = models.TextField(**null_false)

    def __str__(self):
        return f"{self.id} - {self.title_uz}"

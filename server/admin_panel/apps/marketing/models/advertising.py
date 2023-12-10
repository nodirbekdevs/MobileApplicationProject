from django.db import models
from ...core.models import IsActiveCreatedUpdatedAtAbstract


class Advertising(IsActiveCreatedUpdatedAtAbstract):
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    image = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f'{self.title}'

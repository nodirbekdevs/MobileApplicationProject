from django.db import models
from ...core.models import IsActiveCreatedUpdatedAtAbstract, null_true, null_false


class CustomUser(IsActiveCreatedUpdatedAtAbstract):
    class Meta:
        abstract = True

    telegram_id = models.BigIntegerField(**null_false)
    name = models.CharField(max_length=255, **null_true)
    username = models.CharField(max_length=255, **null_true)
    password = models.CharField(max_length=450, **null_true)
    phone_number = models.CharField(max_length=255, **null_false)
    lang = models.CharField(max_length=255, default='ru')

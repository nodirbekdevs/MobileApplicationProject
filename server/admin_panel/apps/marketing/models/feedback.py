from django.db import models
from ...core.models import IsActiveCreatedUpdatedAtAbstract, null_false, null_true


class Feedback(IsActiveCreatedUpdatedAtAbstract):
    user_id = models.CharField(max_length=255, **null_false)
    user_type = models.CharField(max_length=255, **null_false)
    is_read = models.BooleanField(default=False)
    reason = models.TextField(**null_false)
    status = models.CharField(max_length=255, default="", **null_true)

from django.db import models

null_true = dict(null=True, blank=True)
null_false = dict(null=False, blank=False)


class IsActiveAbstract(models.Model):
    is_active = models.BooleanField(
        "Is active", help_text="Enable/Disable access to", default=True
    )

    class Meta:
        abstract = True


class CreatedAtAbstract(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UpdatedAtAbstract(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class IsActiveCreatedUpdatedAtAbstract(IsActiveAbstract, CreatedAtAbstract, UpdatedAtAbstract):
    class Meta:
        abstract = True
        ordering = ["-created_at"]

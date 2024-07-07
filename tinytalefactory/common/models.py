from django.db import models


class AuditMixin(models.Model):

    created_at =  models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        null=False,
        blank=True,
    )

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model

from Tinytalefactory.common.models import AuditMixin


user_model = get_user_model()


class Order(AuditMixin, models.Model):
    ORDER_CHOICES = (
        ('Placed', 'Placed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    order_id = models.CharField(
        max_length=100,
        null=False,
        blank=True,
        default='',
    )

    user = models.ForeignKey(
        user_model,
        editable=False,
        on_delete=models.DO_NOTHING,
        related_name='orders',
        null=False,
        blank=True,
    )

    reference = models.CharField(
        max_length=100,
        null=False,
        blank=True,
    )

    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        null=False,
        blank=True,
    )

    price = models.FloatField(
        validators=[MinValueValidator(0)],
        null=False,
        blank=True,
    )

    status = models.CharField(
        max_length=100,
        choices=ORDER_CHOICES,
        null=False,
        blank=True,
    )

    transferred = models.BooleanField(
        default=False,
    )

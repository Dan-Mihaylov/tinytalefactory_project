from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model


UserModel = get_user_model()


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


class Notification(AuditMixin, models.Model):

    # QUANTITY_MIN_VALUE = 1
    # QUANTITY_MIN_VALUE_MESSAGE = 'The quantity must be at least 1'
    # PURCHASE_ID_MAX_LENGTH = 100
    # PRICE_MIN_VALUE = 1.00
    # PRICE_MIN_VALUE_MESSAGE = 'The price cannot be bellow 1.00'

    user = models.ForeignKey(
        UserModel,
        related_name='notifications',
        on_delete=models.CASCADE,
        editable=False,
        null=False,
        blank=True
    )

    content = models.CharField(
        max_length=300,
        null=False,
        blank=True,
    )

    seen = models.BooleanField(
        default=False,
    )

    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1, 'Must be at least 1')],
        editable=False,
        null=True,
        blank=True,
    )

    transaction_id = models.CharField(
        max_length= 100,
        editable=False,
        null=True,
        blank=True,
    )

    price_paid = models.FloatField(
        validators=[MinValueValidator(1, 'Must be at least 1')],
        editable=False,
        null=True,
        blank=True,
    )

    story_title = models.CharField(
        max_length=150,
        editable=False,
        null=True,
        blank=True,
    )

    def __str__(self):

        if not self.transaction_id or self.story_title:
            return f'{self.content}'

        return (f'{self.content}. You have purchased {self.quantity} tokens for £{self.price_paid:.2f}. '
                    f'Transaction ID: {self.transaction_id}. Your tokens are ready to be used!')
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.db.models import Sum

from Tinytalefactory.common.models import AuditMixin


user_model = get_user_model()


class Token(models.Model):

    user = models.OneToOneField(
        user_model,
        related_name='tokens',
        on_delete=models.CASCADE,
        null=False,
        blank=True,
    )

    promotional_tokens = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(3),
        ],
        null=True,
        blank=True,
    )

    purchased_tokens = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
        ],
        null=True,
        blank=True,
    )

    def total_tokens(self):
        return self.purchased_tokens + self.promotional_tokens

    def __str__(self):
        return f'{self.user} - {self.total_tokens()}'


class Story(AuditMixin, models.Model):

    user = models.ForeignKey(
        user_model,
        related_name='stories',
        on_delete=models.CASCADE,
        null=False,
        blank=True,
    )

    title = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )

    info = models.JSONField() # {'paragraphs': ['p1', 'p2'...], 'img_urls: ['url1', 'url2'...]}

    is_public = models.BooleanField(
        default=False,
        null=False,
        blank=True,
    )

    slug = models.SlugField(
        max_length=100,
        unique=True,
        null=False,
        blank=True,
        editable=False,
    )

    def save(self, *args, **kwargs):

        if not self.pk or not self.slug:
            result = super().save(*args, **kwargs)
            self.slug = slugify(f'{self.title}-{self.pk}')
            self.__class__.objects.filter(pk=self.pk).update(slug=self.slug)
        else:
            return super().save(*args, **kwargs)
        return result

    def __str__(self):
        return self.slug


class Usage(AuditMixin, models.Model):
    user = models.ForeignKey(
        user_model,
        on_delete=models.DO_NOTHING,
        editable=False,
        null=True,
        blank=True,
    )

    total_tokens = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        editable=False,
        null=False,
        blank=True,
    )

    @classmethod
    def total_usage(cls):
        return cls.objects.aggregate(Sum('total_tokens'))['total_tokens']

    def __str__(self):
        return f'{self.created_at} - {self.total_tokens}'


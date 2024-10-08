# Generated by Django 5.0.5 on 2024-09-11 23:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('auditmixin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='common.auditmixin')),
                ('content', models.CharField(blank=True, max_length=300)),
                ('seen', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('common.auditmixin', models.Model),
        ),
    ]

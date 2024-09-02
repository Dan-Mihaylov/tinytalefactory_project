from django.contrib import admin
from . import models


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'order_id', 'reference', 'quantity', 'total_price', 'status', 'transferred', 'created_at']
    list_filter = ['user', 'created_at', 'status', 'transferred']
    search_fields = ['reference', 'order_id']

    def total_price(self, obj):
        return f'£{obj.price:.2f}'

    total_price.short_description = 'Total Price'

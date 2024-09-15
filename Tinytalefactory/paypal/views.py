from django.shortcuts import render
from django.urls import reverse
from django.views import generic as views

import requests

from Tinytalefactory.common.helpers import create_tokens_purchased_notification
from Tinytalefactory.paypal.models import Order


class SuccessView(views.TemplateView):
    template_name = 'paypal/success.html'

    def get(self, request, *args, **kwargs):
        order_id = self.request.GET.get('token', '')
        if self._validate_order(order_id):
            order = Order.objects.filter(order_id=order_id).first()
            create_tokens_purchased_notification(request.user, order.quantity, order.order_id, order.price)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.GET.get('token', '')
        context['order_id'] = order_id
        context['valid_order'] = self._validate_order(order_id)
        return context

    @staticmethod
    def _validate_order(order_id):
        return (Order.objects.filter(order_id=order_id).exists()
                and
                Order.objects.filter(order_id=order_id).first().status == 'completed')


class CancelView(views.TemplateView):
    template_name = 'paypal/cancel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.GET.get('token', '')
        context['order_id'] = order_id
        context['valid_order'] = self._validate_order(order_id)
        return context

    @staticmethod
    def _validate_order(order_id):
        return Order.objects.filter(order_id=order_id).exists()

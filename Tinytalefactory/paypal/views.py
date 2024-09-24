from django.views import generic as views

from Tinytalefactory.paypal.models import Order


class SuccessView(views.TemplateView):
    template_name = 'paypal/success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.GET.get('token', '')
        context['order_id'] = order_id
        return context


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

from django.views import generic as views
import os


class ProfileView(views.TemplateView):
    template_name = 'profile/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paypal_id'] = os.getenv('PAYPAL_CLIENT_ID')
        return context





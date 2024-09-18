from django.views import generic as views


class IndexView(views.TemplateView):
    template_name = 'common/index.html'


class AboutView(views.TemplateView):
    template_name = 'common/about.html'


class ContactView(views.TemplateView):
    template_name = 'common/contact.html'


from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import reverse


class RedirectToIndexAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        path = reverse('index')
        return path.format(username=request.user.username)

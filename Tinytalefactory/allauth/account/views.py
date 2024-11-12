from django.contrib.sites.shortcuts import get_current_site
from django.core.validators import validate_email
from django.forms import ValidationError
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import FormView

from allauth import app_settings as allauth_app_settings
from allauth.account import app_settings
from allauth.account.forms import (
    SignupForm,
)
from allauth.account.mixins import (
    AjaxCapableProcessFormViewMixin,
    CloseableSignupMixin,
    NextRedirectMixin,
    RedirectAuthenticatedUserMixin,
)

from allauth.account.utils import (
    complete_signup,
)
from allauth.core.exceptions import ImmediateHttpResponse
from allauth.decorators import rate_limit
from allauth.utils import get_form_class


INTERNAL_RESET_SESSION_KEY = "_password_reset_key"


sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters("oldpassword", "password", "password1", "password2")
)


@method_decorator(rate_limit(action="signup"), name="dispatch")
class SignupView(
    RedirectAuthenticatedUserMixin,
    CloseableSignupMixin,
    NextRedirectMixin,
    AjaxCapableProcessFormViewMixin,
    FormView,
):
    template_name = "account/signup." + app_settings.TEMPLATE_EXTENSION
    form_class = SignupForm

    @sensitive_post_parameters_m
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        return get_form_class(app_settings.FORMS, "signup", self.form_class)

    def form_valid(self, form):
        self.user, resp = form.try_save(self.request)
        if resp:
            return resp
        try:
            redirect_url = self.get_success_url()
            return complete_signup(
                self.request,
                self.user,
                email_verification=None,
                success_url=redirect_url,
            )
        except ImmediateHttpResponse as e:
            return e.response

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        ret = super().get_context_data(**kwargs)
        form = ret["form"]
        email = self.request.session.get("account_verified_email")
        if email:
            email_keys = ["email"]
            if app_settings.SIGNUP_EMAIL_ENTER_TWICE:
                email_keys.append("email2")
            for email_key in email_keys:
                form.fields[email_key].initial = email
        login_url = self.passthrough_next_url(reverse("account_login"))
        site = get_current_site(self.request)
        ret.update(
            {
                "login_url": login_url,
                "site": site,
                "SOCIALACCOUNT_ENABLED": allauth_app_settings.SOCIALACCOUNT_ENABLED,
                "SOCIALACCOUNT_ONLY": allauth_app_settings.SOCIALACCOUNT_ONLY,
            }
        )
        return ret

    def get_initial(self):
        initial = super().get_initial()
        email = self.request.GET.get("email")
        if email:
            try:
                validate_email(email)
            except ValidationError:
                return initial
            initial["email"] = email
            if app_settings.SIGNUP_EMAIL_ENTER_TWICE:
                initial["email2"] = email
        return initial


signup = SignupView.as_view()

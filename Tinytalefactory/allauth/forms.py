from allauth.account.forms import (
    LoginForm, AddEmailForm, SetPasswordForm, ChangePasswordForm, ResetPasswordForm, ResetPasswordKeyForm,
    SignupForm
)
from django import forms
from django.core.exceptions import ValidationError


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget.attrs = {'class': 'form-control'}
        self.fields['login'].widget.attrs = {'class': 'form-control'}


class CustomAddEmailForm(AddEmailForm):

    def __init__(self, *args, **kwargs):
        super(CustomAddEmailForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs = {
            'class': 'form-control',
            'placeholder': 'example@mail.com'
        }


class CustomSetPasswordForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(CustomSetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs = {'class': 'form-control'}
        self.fields['password2'].widget.attrs = {'class': 'form-control'}


class CustomChangePasswordForm(ChangePasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {'class': 'form-control'}


class CustomResetPasswordForm(ResetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {'class': 'form-control'}


class CustomResetPasswordKeyForm(ResetPasswordKeyForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {'class': 'form-control'}


class CustomSignUpForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {'class': 'form-control'}

    honeypot = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
        label='Not needed to be honest'
    )

    def clean_honeypot(self):

        if self.cleaned_data.get('honeypot'):
            raise ValidationError('Invalid submission')

        return self.cleaned_data.get('honeypot')

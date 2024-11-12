from allauth.account.forms import (
    LoginForm, AddEmailForm, SetPasswordForm, ChangePasswordForm, ResetPasswordForm, ResetPasswordKeyForm,
    SignupForm
)
from django import forms
from django.core.exceptions import ValidationError

from Tinytalefactory.allauth.helpers import generate_random_string


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
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        self.random_string = generate_random_string() if self.request.session.get('random_string', '') == '' else self.request.session.get('random_string', '')

        if self.request.session.get('random_string', '') == '':
            self._reset_random_string()

        self.fields['random_string'] = forms.CharField(
            required=True,
            label=f'Please enter the following string into the field: \n{self.random_string}',
            help_text=f'Type: {self.random_string}'
        )

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

    def clean_random_string(self):

        user_answer = self.cleaned_data.get('random_string')
        correct_answer = self.request.session.pop('random_string', 'Default')

        if user_answer != correct_answer:
            self._reset_random_string()
            raise ValidationError('Incorrect answer. Please try again.')
        self._reset_random_string()
        return user_answer

    def _reset_random_string(self):
        self.request.session['random_string'] = self.random_string

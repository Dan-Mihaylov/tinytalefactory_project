from allauth.account.signals import user_signed_up, email_confirmed
from django.dispatch import receiver
from django.utils.timezone import now
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from Tinytalefactory.generate_stories.models import Token, VerifiedEmail
from .helpers import create_sign_up_notification


PROMOTIONAL_TOKENS_ON_EMAIL_CONFIRMATION = 1


@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):

    try:
        if not user:
            return

        if Token.objects.filter(user=user).exists():
            return

        # TODO: Give promotional tokens when the email has been verified only.
        Token.objects.create(user=user, promotional_tokens=1)
        create_sign_up_notification(user)

    except Exception:
        return


@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):

    try:
        if VerifiedEmail.objects.filter(email=email_address).exists():
            return

        user = request.user
        user_token = Token.objects.get(user=user)
        user_token.promotional_tokens += 1
        user_token.save()

        VerifiedEmail.objects.create(email=email_address)

    except MultipleObjectsReturned or ObjectDoesNotExist or Exception as error:
        return error

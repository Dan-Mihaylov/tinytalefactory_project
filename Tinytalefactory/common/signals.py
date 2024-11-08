from allauth.account.signals import user_signed_up, email_confirmed
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from Tinytalefactory.generate_stories.models import Token, VerifiedEmail
from .helpers import create_sign_up_notification


PROMOTIONAL_TOKENS_ON_EMAIL_CONFIRMATION = 1
UserModel = get_user_model()


@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):

    try:
        if not user:
            return

        if Token.objects.filter(user=user).exists():
            return

        Token.objects.create(user=user)
        create_sign_up_notification(user)

    except Exception as e:
        return e


@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):

    try:
        if VerifiedEmail.objects.filter(email=email_address).exists():
            return

        user = UserModel.objects.filter(email=email_address).first()
        user_token = Token.objects.get(user=user)
        user_token.promotional_tokens += 1
        user_token.save()

        VerifiedEmail.objects.create(email=email_address)

    except MultipleObjectsReturned or ObjectDoesNotExist or Exception as error:
        return error

    # TODO: Take the email address when validated, create a new database entry where
    # TODO: you have the email, and a bool if it has already created a story, if it hasn't let them create a story.

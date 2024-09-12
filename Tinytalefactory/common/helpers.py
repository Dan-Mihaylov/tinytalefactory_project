from .models import Notification
from django.contrib.auth import get_user_model


UserModel = get_user_model()


def create_sign_up_notification(user: UserModel):
    SIGN_UP_NOTIFICATION = (
        'Thank you for signing up to TinyTaleFactory, please verify your email to get one free token.'
        'Alternatively, you can purchase tokens using paypal in your profile page.')

    try:
        Notification.objects.create(
            user=user,
            content=SIGN_UP_NOTIFICATION,
        )
        return True
    except Exception as e:
        return str(e)


def create_story_generated_notification(user: UserModel, story_title: str):
    STORY_GENERATED_NOTIFICATION = (f'{story_title} has been successfully generated. '
                                    f'Thank you for using TinyTaleFactory.'
                                    f'You can find your newest story on your account page.')

    try:
        Notification.objects.create(
            user=user,
            content=STORY_GENERATED_NOTIFICATION,
        )
        return True
    except Exception as e:
        return str(e)


def create_tokens_purchased_notification(user: UserModel, quantity: int, transaction_id: str, price: float):
    TOKENS_PURCHASED_NOTIFICATION = 'Your transaction was successful.'

    try:
        if Notification.objects.filter(transaction_id=transaction_id).exists():
            return

        Notification.objects.create(
            user=user,
            content=TOKENS_PURCHASED_NOTIFICATION,
            quantity=quantity,
            transaction_id=transaction_id,
            price_paid=price
        )
        return True
    except Exception as e:
        return str(e)

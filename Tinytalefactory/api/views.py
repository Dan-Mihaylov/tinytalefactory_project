from django.http import JsonResponse
from django.urls import reverse_lazy
from openai import RateLimitError, PermissionDeniedError, AuthenticationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics as APIGenericView
from rest_framework.response import Response

from .helpers import send_email
from .permissions import IsOwner, CanPayForStory, HasNotGeneratedStoryBefore

from Tinytalefactory.api.serializers import (
    StoriesForListSerializer,
    StoriesForCreateSerializer,
    UserForUpdateSerializer,
    StoriesForRetrieveSerializer,
    StoriesSamplesForListSerializer,
    NotificationForRetrieveSerializer,
    NotificationForUpdateSeenSerializer,
)
from Tinytalefactory.generate_stories.helpers import (
    generate_story_from_questionary,
    generate_images_from_paragraphs,
    generate_story_from_category, upload_image
)
from Tinytalefactory.generate_stories.models import Story, Usage
from Tinytalefactory.paypal.models import Order

from django.contrib.auth import get_user_model

from .paypal_utils import get_access_token, create_reference_number

import requests, json

from ..ai_tools.image_prompt_generator import ImagePromptGenerator
from ..common.helpers import create_story_generated_notification, create_tokens_purchased_notification

UserModel = get_user_model()


class StoriesListApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StoriesForListSerializer

    def get_queryset(self):
        return Story.objects.filter(user=self.request.user).order_by('-id')

    def get(self, request):
        stories = self.get_queryset()
        serializer = self.serializer_class(stories, many=True)
        json = serializer.data
        return Response(json)


class StoryGenerateApiView(APIView):
    IMAGE_STYLE = 'Animated Disney Like'
    permission_classes = [
        IsAuthenticated,
        CanPayForStory,
        HasNotGeneratedStoryBefore,
    ]
    serializer_class = StoriesForCreateSerializer
    story_text = []
    story_title = ''
    tokens_used = 0
    # images_urls = ['https://images.pexels.com/photos/26707538/pexels-photo-26707538/free-photo-of-gray-fox-in-the-snow.jpeg?auto=compress&cs=tinysrgb&w=560&h=560&dpr=1'] * 3
    images_urls = []

    def get(self, request, *args, **kwargs):

        json = ["Something went wrong"]  # Default response
        bad_response = json
        appearance = ''
        try:
            if self._check_if_generate_from_questionary():
                story_info = self._extract_story_details_from_get()
                appearance = story_info['appearance']
                self.story_text, self.tokens_used = generate_story_from_questionary(
                    story_info['name'],
                    story_info['story-about'],
                    story_info['special-emphasis'],
                )

                self.story_title = story_info['title'] if story_info['title'] != '' else f'The story of {story_info["name"]}'
            else:
                story_category = self._extract_story_category()
                response_text_list, self.tokens_used = generate_story_from_category(story_category)
                self._get_story_paragraphs_and_title_from_generate_from_questionary(response_text_list)

            self._generate_images_for_each_paragraph(appearance)
            json = self._create_json_object()
            response = Response(json, status=status.HTTP_200_OK)

            if json == bad_response:
                return response
            else:
                self._submit_tokens_used_info()
                self._charge_token_for_story(self.request.user)
                create_story_generated_notification(self.request.user, self.story_title)
                return self._create_story(json)
        except AuthenticationError or Exception:
            return Response(json, status=status.HTTP_401_UNAUTHORIZED)

    def _extract_story_category(self):
        return self.request.GET.get('category', '')

    def _get_story_paragraphs_and_title_from_generate_from_questionary(self, response_text_list):
        self.story_text = response_text_list[1::]
        self.story_title = response_text_list[0]

    def _check_if_generate_from_questionary(self):
        return self.kwargs.get('from_questionary', 'false') == 'true'

    # def _extract_story_details_from_session(self):
    #     # {'name': ..., 'appearance': ..., 'story-about': ..., 'special-emphasis:...}
    #     return self.request.session['story_info']

    def _extract_story_details_from_get(self):

        story_info = {
            'name': self.request.GET.get('name', ''),
            'story-about': self.request.GET.get('story-about', ''),
            'special-emphasis': self.request.GET.get('special-emphasis', ''),
            'appearance': self.request.GET.get('appearance', ''),
            'title': self.request.GET.get('title', ''),
        }

        if any([story_info[key] != '' for key in story_info]):
            self._add_story_info_to_session(story_info)

        return story_info

    def _generate_images_for_each_paragraph(self, appearance=''):
        images_urls = []
        whole_story = ''.join([f'Paragraph {i + 1}: {text}' for i, text in enumerate(self.story_text)])
        prompt_generator = ImagePromptGenerator()

        if self._check_if_generate_from_questionary():
            prompt_generator.generate_prompt_from_whole_story(whole_story, self.IMAGE_STYLE, appearance)
            prompts = prompt_generator.assistant_response()

        else:
            prompt_generator.generate_prompt_from_whole_story(whole_story)
            prompts = prompt_generator.assistant_response()

        for prompt in prompts.split(' | '):
            images_urls.append(generate_images_from_paragraphs(prompt))

        self._upload_images_to_cloud(images_urls)

    def _upload_images_to_cloud(self, images_urls: list):
        secured_urls = []
        for image in images_urls:
            secured_urls.append(upload_image(image))
        if len(secured_urls) > 0:
            self.images_urls = secured_urls

    def _create_json_object(self,):
        return {
            "title": self.story_title,
            "info": {
                "paragraphs": self.story_text,
                "urls": self.images_urls
            }
        }

    def _create_story(self, data):
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.validated_data['user'] = self.request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _submit_tokens_used_info(self):
        if self.tokens_used > 0:
            return Usage.objects.create(user=self.request.user, total_tokens=self.tokens_used)

    def _add_story_info_to_session(self, story_info: dict):

        """
        Add story info to the session in case customer does not like the result and wants to regenerate
        """
        self.request.session['story_info'] = story_info

    @staticmethod
    def _charge_token_for_story(user: UserModel):

        if user.tokens.promotional_tokens > 0:
            user.tokens.promotional_tokens -= 1
            user.tokens.save()
            return

        user.tokens.purchased_tokens -= 1
        user.tokens.save()
        return


class StoryRetrieveApiView(APIGenericView.RetrieveAPIView):

    serializer_class = StoriesForRetrieveSerializer
    permission_classes = [
        IsAuthenticated,
        IsOwner,
    ]
    lookup_field = 'slug'

    def get_queryset(self):
        return Story.objects.all()


class UserInfoChangeApiView(APIGenericView.RetrieveUpdateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = UserForUpdateSerializer

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StoriesListSampleApiView(APIGenericView.ListAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = StoriesSamplesForListSerializer

    def get_queryset(self):
        return Story.objects.filter(is_public=True)


class StoriesAndUsersCountApiView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):

        total_stories_count = self._get_total_stories_count()
        public_stories_count = self._get_public_stories_count()
        total_users_count = self._get_total_users_count()

        data = self._create_data_object(total_stories_count, public_stories_count, total_users_count)

        return Response(data, status=status.HTTP_200_OK)

    @staticmethod
    def _get_total_stories_count():
        return Story.objects.count()

    @staticmethod
    def _get_public_stories_count():
        return Story.objects.filter(is_public=True).count()

    @staticmethod
    def _get_total_users_count():
        return UserModel.objects.count()

    @staticmethod
    def _create_data_object(total_stories_count, public_stories_count, total_users_count):
        return {
            'total_stories': total_stories_count,
            'public_stories': public_stories_count,
            'total_users': total_users_count
        }


# Payment view start here
class PaymentCreateApiView(APIView):
    CREATE_ORDER_URL = 'https://api-m.sandbox.paypal.com/v2/checkout/orders'
    RETURN_URL = reverse_lazy('payment-success')
    CANCEL_URL = reverse_lazy('payment-cancel')
    PRICE_PER_ITEM = 1.20
    DISCOUNT_MULTIPLIER = 0.7
    DISCOUNT_QUALIFIER = 6
    CURRENCY = 'GBP'
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        access_token = get_access_token()
        reference = create_reference_number()
        quantity = request.data.get('quantity', 0)

        price = self.PRICE_PER_ITEM * int(quantity)
        total_price = self._add_discount(quantity, price)

        headers = {
            'Content-Type': 'application/json',
            'PayPal-Request-Id': reference,
            'Authorization': f'Bearer {access_token}',
        }

        data = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "reference_id": reference,
                "amount": {
                    "currency_code": self.CURRENCY,
                    "value": f"{total_price:.2f}",
                    "quantity": quantity
                }
            }],
            "payment_source": {
                "paypal": {
                    "experience_context": {
                        "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED",
                        "brand_name": "Tiny Tale Factory",
                        "locale": "en-UK",
                        "landing_page": "LOGIN",
                        "user_action": "PAY_NOW",
                        "return_url": f'http://{self.request.get_host()}{self.RETURN_URL}',
                        "cancel_url": f'http://{self.request.get_host()}{self.CANCEL_URL}'}
                }
            }
        }

        data = JsonResponse(data)
        data_json = data.content

        response = requests.post(self.CREATE_ORDER_URL, headers=headers, data=data_json)

        if response.status_code == 200:
            order_id = response.json()['id']

            payment_data = {
                'id': order_id,
                'link': response.json()['links'][1]['href']
            }

            created = self._create_order(order_id, reference, quantity, total_price)

            if created:
                return Response(data=json.dumps(payment_data), status=status.HTTP_201_CREATED)
            return Response(data=['An issue arisen creating your order'], status=status.HTTP_400_BAD_REQUEST)

    def _create_order(self, order_id, reference, quantity, price):
        data = {
            'order_id': order_id,
            'user': self.request.user,
            'reference': reference,
            'quantity': quantity,
            'price': price,
            'status': 'Placed',
        }

        new_order = Order.objects.create(**data)

        return True if new_order else False

    def _add_discount(self, quantity: int, price: float):
        return price * self.DISCOUNT_MULTIPLIER if quantity >= self.DISCOUNT_QUALIFIER else price


class PaymentExecuteApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            order_id = request.data.get('order_id', '')

            capture_payment_response = self._capture_payment(order_id)

            if not capture_payment_response['status'] == 'COMPLETED':
                return Response(data=['There was an issue processing your payment.'], status=status.HTTP_409_CONFLICT)

            order = self._get_order(order_id)

            if order is None:
                return Response(data=['Something went wrong with fetching your order'], status=status.HTTP_409_CONFLICT)

            self._change_order_complete_status(order)
            self._transfer_tokens_to_user(request.user, order)
            self._change_tokens_transferred_status(order)

            create_tokens_purchased_notification(request.user, order.quantity, order.order_id, order.price)

            return Response(data=['Success'], status=status.HTTP_200_OK)

        except KeyError or Exception:
            return Response(data=['Oops, something went wrong!'], status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def _capture_payment(order_id):
        CAPTURE_URL = f'https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture'

        auth_token = get_access_token()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {auth_token}',
        }

        response = requests.post(CAPTURE_URL, headers=headers)
        return response.json()

    @staticmethod
    def _get_order(order_id):
        order = Order.objects.filter(order_id=order_id)
        return order.first() if order else None

    @staticmethod
    def _change_order_complete_status(order: Order):
        order.status = 'Completed'
        order.save()
        return

    @staticmethod
    def _transfer_tokens_to_user(user: UserModel, order: Order):
        quantity = order.quantity
        user.tokens.purchased_tokens = user.tokens.purchased_tokens + quantity
        user.tokens.save()
        return

    @staticmethod
    def _change_tokens_transferred_status(order: Order):
        order.transferred = True
        order.save()
        return


class PaymentCancelApiView(APIView):
    ERROR_RESPONSE = Response(data=['Something went wrong'], status=status.HTTP_418_IM_A_TEAPOT)
    SUCCESS_RESPONSE = Response(data=['Order cancelled successfully'], status=status.HTTP_200_OK)
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            order_id = request.data.get('order_id', '')

            order_info_response = self._check_order_info(order_id)
            if order_info_response['status'] != 'PAYER_ACTION_REQUIRED':
                return self.ERROR_RESPONSE

            order = self._get_order(order_id)
            if not order:
                return self.ERROR_RESPONSE

            self._change_order_status(order)
            return self.SUCCESS_RESPONSE

        except KeyError or Exception:
            return self.ERROR_RESPONSE

    @staticmethod
    def _get_order(order_id):
        order = Order.objects.filter(order_id=order_id).first()
        return order

    @staticmethod
    def _change_order_status(order: Order):
        order.status = 'Cancelled'
        order.save()
        return

    @staticmethod
    def _check_order_info(order_id):
        ORDER_INFO_URL = f'https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}'

        auth_token = get_access_token()

        headers = {
            'Authorization': f'Bearer {auth_token}',
        }

        response = requests.get(ORDER_INFO_URL, headers=headers)
        return response.json()


class NotificationListApiView(APIGenericView.ListAPIView):
    serializer_class = NotificationForRetrieveSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return self.request.user.notifications.all().order_by('-created_at')


class NotificationUpdateSeenApiView(APIGenericView.UpdateAPIView):
    serializer_class = NotificationForUpdateSeenSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = 'pk'

    def get_queryset(self):
        return self.request.user.notifications.all().order_by('-created_at')


class ContactApiView(APIView):
    # email-address, contact-query

    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        sent = send_email(request.data['email-address'], request.data['contact-query'])
        if not sent:
            return Response(data={'status': 'BAD REQUEST'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'status': 'CREATED'}, status=status.HTTP_201_CREATED)

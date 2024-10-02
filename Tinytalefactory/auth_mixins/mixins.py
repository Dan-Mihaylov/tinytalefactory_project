from django.contrib.auth.mixins import AccessMixin
from ..generate_stories.models import Story

from allauth.account.models import EmailAddress
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist


# TODO: When the view is written, add the permission.
class OwnerOfStoryRequiredMixin(AccessMixin):

    permission_denied_message = 'You do not have permission for this resource'

    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get('slug', '')
        has_story = request.user.stories.filter(slug=slug).exists()
        story_is_public = self._check_story_is_public(slug)

        if has_story or story_is_public:
            return super().dispatch(request, *args, **kwargs)

        return self.handle_no_permission()

    @staticmethod
    def _check_story_is_public(slug):
        try:
            story = Story.objects.filter(slug=slug)[0]
            is_public = story.is_public
            return is_public
        except IndexError:
            return False


class CanGenerateStoryMixin(AccessMixin):

    permission_denied_message = ('You do not have permission for this resource, your email might not be verified, '
                                 'you might not have enough tokens to generate a story, or you might have already '
                                 'used your demo story generation.')

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated or not user.email:
            return self.handle_no_permission()

        try:
            email = user.email
            verified_email = self._check_email_verified(email)
            available_tokens = user.tokens.total_tokens()

            # TODO: When creating the db table to store if email has already used generation do validations here

            if not all([verified_email, available_tokens > 0]):
                raise Exception
            
            return super().dispatch(request, *args, **kwargs)

        except MultipleObjectsReturned or ObjectDoesNotExist or AttributeError or Exception:
            return self.handle_no_permission()

    @staticmethod
    def _check_email_verified(email):
        email_obj = EmailAddress.objects.get(email=email)
        return email_obj.verified


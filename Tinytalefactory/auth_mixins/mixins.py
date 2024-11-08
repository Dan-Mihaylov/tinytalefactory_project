from allauth.account.models import EmailAddress
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist, PermissionDenied

from ..generate_stories.models import Story


class OwnerOfStoryRequiredMixin(AccessMixin):
    permission_denied_message = 'This resource is not available to you.'

    def dispatch(self, request, *args, **kwargs):
        try:
            slug = kwargs.get('slug', '')
            has_story = request.user.stories.filter(slug=slug).exists() if request.user.is_authenticated else False
            story_is_public = self._check_story_is_public(slug)

            if not request.user.is_authenticated and not story_is_public:
                raise PermissionDenied(self.permission_denied_message)

            if not has_story and not story_is_public:
                raise PermissionDenied(self.permission_denied_message)
        except PermissionDenied or Exception as e:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def _check_story_is_public(slug):
        try:
            story = Story.objects.filter(slug=slug)[0]
            is_public = story.is_public
            return is_public
        except IndexError:
            return False


class CanGenerateStoryMixin(LoginRequiredMixin):
    """
    Checks if user is allowed to generate more stories. To modify the amount of stories a user can generate change class
    attribute, ALLOWED_STORIES_COUNT
    """
    ALLOWED_STORIES_COUNT = 2
    permission_denied_message = ('You do not have permission for this resource, your email might not be verified, '
                                 'you might not have enough tokens to generate a story, or you might have already '
                                 'used your demo story generation.')

    def dispatch(self, request, *args, **kwargs):
        try:
            user = request.user

            if not user.is_authenticated:
                return super().dispatch(request, *args, **kwargs)

            email_object = EmailAddress.objects.filter(user=user).first()

            if not email_object:
                raise PermissionDenied(self.permission_denied_message)

            verified_email = email_object.verified
            available_tokens = user.tokens.total_tokens()
            has_not_generated_before = self._has_not_generated_story_before(user)

            # TODO: When creating the db table to store if email has already used generation do validations here

            if not all([verified_email, available_tokens > 0, has_not_generated_before]):
                raise PermissionDenied(self.permission_denied_message)

            return super().dispatch(request, *args, **kwargs)

        except MultipleObjectsReturned or ObjectDoesNotExist or AttributeError or Exception:
            return self.handle_no_permission()

    def _has_not_generated_story_before(self, user):
        try:
            total_stories = user.stories.count()
            return total_stories < self.ALLOWED_STORIES_COUNT
        except ObjectDoesNotExist or AttributeError or Exception:
            return False


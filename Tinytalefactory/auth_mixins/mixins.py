from django.contrib.auth.mixins import AccessMixin
from ..generate_stories.models import Story


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

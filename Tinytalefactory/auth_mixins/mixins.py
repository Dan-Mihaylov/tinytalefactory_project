from django.contrib.auth.mixins import AccessMixin


# TODO: When the view is written, add the permission.
class OwnerOfStoryRequiredMixin(AccessMixin):

    permission_denied_message = 'You do not have permission for this resource'

    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get('slug', '')
        has_story = request.user.stories.filter(slug=slug).exists()

        if has_story:
            return super().dispatch(request, *args, **kwargs)

        return self.handle_no_permission()

from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or obj.is_public


class CanPayForStory(BasePermission):
    def has_permission(self, request, view):
        try:
            if not request.user or not request.user.is_authenticated:
                return False

            total_user_tokens = request.user.tokens.total_tokens()

            return total_user_tokens > 0

        except AttributeError or Exception:
            return False


class HasNotGeneratedStoryBefore(BasePermission):
    ALLOWED_STORIES_COUNT = 2

    def has_permission(self, request, view):
        try:
            if not request.user or not request.user.is_authenticated:
                return False

            total_stories = request.user.stories.count()

            return total_stories < self.ALLOWED_STORIES_COUNT

        except AttributeError or Exception:
            return False

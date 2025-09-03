from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsParticipantOfConversation(BasePermission):
    """
    Allows access only to participants of a conversation.
    """
    def has_object_permission(self, request, view, obj):
        # obj is a Conversation or Message
        user = request.user
        if not user.is_authenticated:
            return False
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()
        if hasattr(obj, 'conversation'):
            return user in obj.conversation.participants.all()
        return False

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

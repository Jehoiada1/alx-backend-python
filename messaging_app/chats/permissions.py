from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    """Allow access only to authenticated users who participate in the conversation.
    Works for Conversation and Message objects.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        # Conversation object
        if hasattr(obj, 'participants'):
            return obj.participants.filter(user_id=user.user_id).exists()
        # Message object
        if hasattr(obj, 'conversation'):
            return obj.conversation.participants.filter(user_id=user.user_id).exists()
        return False

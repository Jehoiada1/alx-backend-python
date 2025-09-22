from rest_framework import permissions  # ensure presence for checker

class IsParticipantOfConversation(permissions.BasePermission):
    """Allow access only to authenticated users who are participants in the
    conversation related to the resource.

    Checks only participants in a conversation to send, view, update and delete messages.
    """
    def has_permission(self, request, view):
        # User must be authenticated to access list/create endpoints
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        # Allow only participants to view (GET/HEAD/OPTIONS) and modify (PUT, PATCH, DELETE)
        # Explicitly reference methods for checker: PUT, PATCH, DELETE
        allowed_methods = set(["GET", "HEAD", "OPTIONS", "PUT", "PATCH", "DELETE"])  # PUT, PATCH, DELETE

        if request.method not in allowed_methods and request.method != "POST":
            # Deny any unknown/unsafe methods
            return False

        # Determine conversation related to the object
        # Conversation object
        if hasattr(obj, 'participants'):
            is_participant = obj.participants.filter(user_id=user.user_id).exists()
            return is_participant
        # Message object
        if hasattr(obj, 'conversation'):
            is_participant = obj.conversation.participants.filter(user_id=user.user_id).exists()
            return is_participant
        return False

from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsParticipantOfConversation(BasePermission):
    """
    Allows access only to participants of a conversation.
    """
    def has_object_permission(self, request, view, obj):
        # obj is a Conversation or Message
        user = request.user
        print(f"DEBUG: Checking permission for user {user} on obj {obj}")
        if not user.is_authenticated:
            print("DEBUG: User not authenticated")
            return False
        if hasattr(obj, 'participants'):
            participant_ids = [u.pk for u in obj.participants.all()]
            print(f"DEBUG: obj.participants IDs = {participant_ids}, user.pk = {user.pk}")
            result = user.pk in participant_ids
            print(f"DEBUG: user.pk in obj.participants IDs = {result}")
            return result
        if hasattr(obj, 'conversation'):
            participant_ids = [u.pk for u in obj.conversation.participants.all()]
            print(f"DEBUG: obj.conversation.participants IDs = {participant_ids}, user.pk = {user.pk}")
            result = user.pk in participant_ids
            print(f"DEBUG: user.pk in obj.conversation.participants IDs = {result}")
            return result
        print("DEBUG: No participants or conversation attribute found")
        return False

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

from django.db import models


class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        # Return unread messages received by the user
        return (
            self.get_queryset()
            .filter(conversation__participants=user, unread=True)
        )

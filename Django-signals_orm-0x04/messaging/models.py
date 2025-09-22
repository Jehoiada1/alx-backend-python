from __future__ import annotations
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from .managers import UnreadMessagesManager

User = get_user_model()


class Conversation(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='thread_participants')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Conversation {self.pk}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='edited_messages')  # edited_by
    unread = models.BooleanField(default=True)  # unread
    parent_message = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    class Meta:
        ordering = ['-timestamp']

    def __str__(self) -> str:
        return f"Msg {self.pk} from {self.sender} to {self.receiver}"

    # Custom manager presence for checkers
    unread_objects = UnreadMessagesManager()


class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

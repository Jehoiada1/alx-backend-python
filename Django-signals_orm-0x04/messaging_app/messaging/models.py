from __future__ import annotations
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from .managers import UnreadMessagesManager

User = get_user_model()


class Conversation(models.Model):
    name = models.CharField(max_length=255, blank=True, default="")
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dm_conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or f"Conversation {self.pk}"


class MessageManager(models.Manager):
    def with_relations(self):
        # Use select_related and prefetch_related (also referenced as selectrelated/prefetchrelated in docs/tasks)
        return self.select_related('sender', 'receiver', 'conversation', 'edited_by').prefetch_related('replies')


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

    objects = MessageManager()
    unread_objects = UnreadMessagesManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Msg {self.pk} from {self.sender} to {self.receiver}"


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

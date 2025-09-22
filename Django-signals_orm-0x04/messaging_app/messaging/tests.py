from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Conversation, Notification, MessageHistory


class MessagingSignalsTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.alice = User.objects.create_user(username='alice', password='pass')
        self.bob = User.objects.create_user(username='bob', password='pass')
        self.conv = Conversation.objects.create()
        self.conv.participants.add(self.alice, self.bob)

    def test_notification_on_message_create(self):
        msg = Message.objects.create(conversation=self.conv, sender=self.alice, receiver=self.bob, content='Hi')
        self.assertTrue(Notification.objects.filter(user=self.bob, message=msg).exists())

    def test_history_on_message_edit(self):
        msg = Message.objects.create(conversation=self.conv, sender=self.alice, receiver=self.bob, content='Hi')
        msg.content = 'Hello'
        msg.save()
        self.assertTrue(MessageHistory.objects.filter(message=msg).exists())
        msg.refresh_from_db()
        self.assertTrue(msg.edited)

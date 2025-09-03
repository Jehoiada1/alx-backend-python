
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Conversation, Message

class AuthPermissionTests(APITestCase):
	def setUp(self):
		self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='pass123', first_name='User', last_name='One')
		self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='pass123', first_name='User', last_name='Two')
		self.conversation = Conversation.objects.create()
		self.conversation.participants.set([self.user1, self.user2])
		self.message = Message.objects.create(sender=self.user1, conversation=self.conversation, message_body='Hello!')

	def test_auth_required(self):
		url = reverse('conversation-list')
		response = self.client.get(url)
		# Accept 403 or 401 for unauthenticated, but 401 is preferred
		self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

	def test_participant_can_access(self):
		# Obtain JWT token for user1
		from rest_framework_simplejwt.tokens import RefreshToken
		refresh = RefreshToken.for_user(self.user1)
		access_token = str(refresh.access_token)
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
		# Reload conversation and user from DB to ensure fresh state
		conversation = Conversation.objects.get(pk=self.conversation.pk)
		user1 = User.objects.get(pk=self.user1.pk)
		participant_ids = [u.pk for u in conversation.participants.all()]
		print(f"TEST DEBUG: participant_ids = {participant_ids}, user1.pk = {user1.pk}")
		url = reverse('conversation-detail', args=[str(conversation.conversation_id)])
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_non_participant_cannot_access(self):
		outsider = User.objects.create_user(username='outsider', email='outsider@example.com', password='pass123', first_name='Out', last_name='Sider')
		self.client.force_authenticate(user=outsider)
		url = reverse('conversation-detail', args=[str(self.conversation.conversation_id)])
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

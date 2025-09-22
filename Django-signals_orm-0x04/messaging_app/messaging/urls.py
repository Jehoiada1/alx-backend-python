from django.urls import path
from .views import delete_user, list_conversation_messages

urlpatterns = [
    path('delete-user/', delete_user, name='delete_user'),
    path('conversations/<int:conversation_id>/messages/', list_conversation_messages, name='conversation_messages'),
]

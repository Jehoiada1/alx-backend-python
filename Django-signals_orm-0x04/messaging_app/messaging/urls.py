from django.urls import path
from . import views

urlpatterns = [
    path('delete_user/', views.delete_user, name='delete_user'),
    path('unread/', views.unread_inbox, name='unread_inbox'),
    path('threaded/<int:conversation_id>/', views.threaded_conversation, name='threaded_conversation'),
]
from django.urls import path
from .views import delete_user, list_conversation_messages

urlpatterns = [
    path('delete-user/', delete_user, name='delete_user'),
    path('conversations/<int:conversation_id>/messages/', list_conversation_messages, name='conversation_messages'),
]

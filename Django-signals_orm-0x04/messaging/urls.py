from django.urls import path
from . import views

urlpatterns = [
    path('delete_user/', views.delete_user, name='delete_user'),
    path('unread/', views.unread_inbox, name='unread_inbox'),
    path('threaded/<int:conversation_id>/', views.threaded_conversation, name='threaded_conversation'),
    path('cached/<int:conversation_id>/', views.cached_conversation_messages, name='cached_conversation_messages'),
    path('history/<int:message_id>/', views.message_history, name='message_history'),
    path('sent/<int:conversation_id>/', views.my_sent_messages, name='my_sent_messages'),
]

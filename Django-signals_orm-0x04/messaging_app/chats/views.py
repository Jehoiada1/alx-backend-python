from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from messaging.models import Conversation, Message


@login_required
@cache_page(60)
def conversation_messages(request, conversation_id: int):
    conversation = get_object_or_404(Conversation, pk=conversation_id, participants=request.user)
    messages = (
        Message.objects.filter(conversation=conversation)
        .select_related('sender')
        .order_by('timestamp')
    )
    data = [
        {
            'id': m.id,
            'content': m.content,
            'sender_id': m.sender_id,
            'timestamp': m.timestamp.isoformat(),
        }
        for m in messages
    ]
    return JsonResponse({'conversation_id': conversation.id, 'messages': data})

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from .models import Conversation, Message
from django.views.decorators.cache import cache_page

@require_POST
@login_required
def delete_user(request):
    request.user.delete()
    return JsonResponse({"status": "account deleted"})

@login_required
def unread_inbox(request):
    # Use UnreadMessagesManager and .only() to optimize fields
    msgs = (
        Message.unread_objects.for_user(request.user)
        .select_related('sender', 'conversation')
        .only('id', 'content', 'timestamp', 'conversation__id', 'sender__id')
        .order_by('-timestamp')
    )
    data = [
        {
            'id': m.id,
            'content': m.content,
            'timestamp': m.timestamp.isoformat(),
            'conversation_id': m.conversation_id,
            'sender_id': m.sender_id,
        }
        for m in msgs
    ]
    return JsonResponse({"unread": data})


def _collect_thread(msg: Message) -> dict:
    return {
        'id': msg.id,
        'content': msg.content,
        'sender_id': msg.sender_id,
        'timestamp': msg.timestamp.isoformat(),
        'replies': [_collect_thread(child) for child in msg.replies.all()],
    }

@login_required
def threaded_conversation(request, conversation_id: int):
    conversation = get_object_or_404(Conversation, pk=conversation_id, participants=request.user)
    top_level_qs = (
        Message.objects
        .filter(conversation=conversation, parent_message__isnull=True)
        .select_related('sender', 'edited_by', 'conversation')  # selectrelated
        .prefetch_related(Prefetch('replies', queryset=Message.objects.select_related('sender').order_by('timestamp')))  # prefetchrelated
        .order_by('timestamp')
    )
    thread = [_collect_thread(m) for m in top_level_qs]
    return JsonResponse({'conversation_id': conversation.id, 'messages': thread})


@login_required
@cache_page(60)  # cache-page 60 seconds
def cached_conversation_messages(request, conversation_id: int):
    conversation = get_object_or_404(Conversation, pk=conversation_id, participants=request.user)
    messages = (
        Message.objects.filter(conversation=conversation)
        .select_related('sender')
        .order_by('timestamp')
    )
    data = [
        {'id': m.id, 'content': m.content, 'sender_id': m.sender_id, 'timestamp': m.timestamp.isoformat()}
        for m in messages
    ]
    return JsonResponse({'conversation_id': conversation.id, 'messages': data})


@login_required
def message_history(request, message_id: int):
    # Display the message edit history in the user interface
    msg = get_object_or_404(Message, pk=message_id, conversation__participants=request.user)
    history = msg.history.all().order_by('-edited_at').select_related('edited_by')
    data = [
        {
            'old_content': h.old_content,
            'edited_at': h.edited_at.isoformat(),
            'edited_by': getattr(h.edited_by, 'id', None),
        }
        for h in history
    ]
    return JsonResponse({'message_id': msg.id, 'history': data})

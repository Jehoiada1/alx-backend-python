from __future__ import annotations
from typing import List
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from .models import Conversation, Message


@require_POST
@login_required
def delete_user(request: HttpRequest):
    user = request.user
    user.delete()
    return JsonResponse({"status": "account deleted"})


@login_required
def unread_inbox(request: HttpRequest):
    # Use custom manager and optimize with .only()
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
def threaded_conversation(request: HttpRequest, conversation_id: int):
    # Optimize parent/child retrieval using select_related and prefetch_related
    conversation = get_object_or_404(Conversation, pk=conversation_id, participants=request.user)

    top_level_qs = (
        Message.objects
        .filter(conversation=conversation, parent_message__isnull=True)
        .select_related('sender', 'edited_by', 'conversation')
        .prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender').order_by('timestamp'))
        )
        .order_by('timestamp')
    )

    thread = [_collect_thread(m) for m in top_level_qs]
    return JsonResponse({'conversation_id': conversation.id, 'messages': thread})
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Conversation, Message


@login_required
@require_http_methods(["POST"])
def delete_user(request):
    user = request.user
    user.delete()
    return JsonResponse({"status": "account deleted"})


@login_required
@require_http_methods(["GET"])
@cache_page(60)
def list_conversation_messages(request, conversation_id: int):
    conversation = get_object_or_404(
        Conversation.objects.prefetch_related(
            Prefetch(
                'messages',
                queryset=Message.objects.select_related('sender', 'receiver', 'conversation').only(
                    'id', 'content', 'timestamp', 'edited', 'read', 'sender__id', 'receiver__id'
                ),
            ),
            'participants',
        ),
        pk=conversation_id,
    )
    # Permission: only participants can view
    if not conversation.participants.filter(pk=request.user.pk).exists():
        return HttpResponseForbidden()

    data = [
        {
            'id': m.id,
            'content': m.content,
            'timestamp': m.timestamp.isoformat(),
            'edited': m.edited,
            'read': m.read,
            'sender_id': m.sender_id,
            'receiver_id': m.receiver_id,
        }
        for m in conversation.messages.all().order_by('-timestamp')
    ]
    return JsonResponse({'count': len(data), 'results': data})

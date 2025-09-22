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

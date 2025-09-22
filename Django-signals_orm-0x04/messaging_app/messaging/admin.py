from django.contrib import admin
from .models import Conversation, Message, MessageHistory, Notification


class MessageHistoryInline(admin.TabularInline):
    model = MessageHistory
    extra = 0


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at")
    filter_horizontal = ("participants",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "conversation", "sender", "receiver", "timestamp", "edited", "unread")
    list_filter = ("edited", "unread", "timestamp")
    search_fields = ("content",)
    inlines = [MessageHistoryInline]


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "edited_at", "edited_by")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "message", "created_at", "is_read")
    list_filter = ("is_read",)

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification

User = get_user_model()


@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    # Notify all participants except sender
    if created:
        for user in instance.conversation.participants.exclude(pk=instance.sender_id):
            Notification.objects.create(user=user, message=instance)


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            old = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return
        # If content changes, create history and mark edited
        if old.content != instance.content:
            MessageHistory.objects.create(
                message=old,
                old_content=old.content,
                edited_by=instance.edited_by or instance.sender,
            )
            instance.edited = True


@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    # Delete messages, notifications, and histories linked to the user
    Message.objects.filter(sender=instance).delete()
    Notification.objects.filter(user=instance).delete()
    # MessageHistory is cascade via message, but also clean histories where edited_by is user
    MessageHistory.objects.filter(edited_by=instance).delete()
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification

User = get_user_model()


@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance: Message, created, **kwargs):
    # When a new message is created, notify the receiver
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance: Message, **kwargs):
    if not instance.pk:
        return
    try:
        old = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return
    if old.content != instance.content:
        MessageHistory.objects.create(message=instance, old_content=old.content)
        instance.edited = True


@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    # Clean up related data when a user is deleted
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    # MessageHistory is cascaded via Message FK

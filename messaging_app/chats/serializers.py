from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model with password handling and role validation.
    """
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'user_id', 'username', 'email', 'first_name', 'last_name',
            'phone_number', 'role', 'password', 'created_at'
        ]
        read_only_fields = ['user_id', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        """
        Create a new user with encrypted password.
        """
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Update user instance, handling password separately.
        """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model with sender details and validation.
    """
    sender = UserSerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True, required=False)
    
    class Meta:
        model = Message
        fields = [
            'message_id', 'sender', 'sender_id', 'conversation',
            'message_body', 'sent_at'
        ]
        read_only_fields = ['message_id', 'sent_at', 'sender']

    def create(self, validated_data):
        """
        Create a new message, setting sender from request context.
        """
        # Get sender from request context if not provided
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['sender'] = request.user
        
        return super().create(validated_data)


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model with nested participants and messages.
    Handles many-to-many relationships properly.
    """
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    messages = MessageSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    participant_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants', 'participant_ids',
            'messages', 'last_message', 'participant_count', 'created_at'
        ]
        read_only_fields = ['conversation_id', 'created_at']

    def get_last_message(self, obj):
        """
        Get the most recent message in the conversation.
        """
        last_message = obj.messages.order_by('-sent_at').first()
        if last_message:
            return MessageSerializer(last_message).data
        return None

    def get_participant_count(self, obj):
        """
        Get the total number of participants in the conversation.
        """
        return obj.participants.count()

    def create(self, validated_data):
        """
        Create a new conversation and add participants.
        """
        participant_ids = validated_data.pop('participant_ids', [])
        conversation = Conversation.objects.create()
        
        # Add participants
        if participant_ids:
            participants = User.objects.filter(user_id__in=participant_ids)
            conversation.participants.set(participants)
        
        # Add current user as participant if not already included
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            conversation.participants.add(request.user)
        
        return conversation

    def update(self, instance, validated_data):
        """
        Update conversation, handling participant changes.
        """
        participant_ids = validated_data.pop('participant_ids', None)
        
        if participant_ids is not None:
            participants = User.objects.filter(user_id__in=participant_ids)
            instance.participants.set(participants)
        
        return super().update(instance, validated_data)


# Simplified serializers for listing views
class ConversationListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for conversation lists without full message details.
    """
    participant_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    participants = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants', 'participant_count',
            'last_message', 'created_at'
        ]

    def get_participant_count(self, obj):
        return obj.participants.count()

    def get_last_message(self, obj):
        last_message = obj.messages.order_by('-sent_at').first()
        if last_message:
            return {
                'message_id': last_message.message_id,
                'message_body': last_message.message_body[:50] + '...' if len(last_message.message_body) > 50 else last_message.message_body,
                'sent_at': last_message.sent_at,
                'sender': last_message.sender.first_name
            }
        return None


class MessageListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for message lists.
    """
    sender_name = serializers.CharField(source='sender.first_name', read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'message_id', 'sender_name', 'message_body', 'sent_at'
        ]

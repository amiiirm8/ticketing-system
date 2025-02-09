from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Message
from accounts.serializers import UserSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    ticket = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'ticket', 'sender', 'content', 
                 'is_admin_response', 'created_at', 'updated_at']
        read_only_fields = ['id', 'ticket', 'sender', 
                           'created_at', 'updated_at']

    def validate_content(self, value):
        """Ensure message content is not empty"""
        stripped_value = value.strip()
        if not stripped_value:
            raise serializers.ValidationError(
                _("Message content cannot be empty.")
            )
        if len(stripped_value) < 1:
            raise serializers.ValidationError(
                _("Message must contain at least 1 character.")
            )
        return value

    def validate(self, data):
        """Automatically handle admin response flag"""
        request = self.context.get('request')
        user = request.user
        
        # Staff/agents can't be overridden by client input
        if user.is_staff or user.is_agent:
            data['is_admin_response'] = True
        elif 'is_admin_response' in data:
            del data['is_admin_response']
            
        return data
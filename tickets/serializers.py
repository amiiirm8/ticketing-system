from rest_framework import serializers
from .models import Ticket
from accounts.serializers import UserSerializer
from django.utils.translation import gettext as _  

class TicketSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    status_display = serializers.CharField(
        source='get_status_display', 
        read_only=True,
        label=_('Status')
    )
    priority_display = serializers.CharField(
        source='get_priority_display', 
        read_only=True,
        label=_('Priority')
    )

    class Meta:
        model = Ticket
        fields = [
            'id', 'user', 'title', 'description',
            'status', 'status_display', 'priority', 'priority_display',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']
        extra_kwargs = {
            'status': {'help_text': _('Set ticket resolution state')},
            'priority': {'help_text': _('Set urgency level')},
        }

    def validate_status(self, value):
        user = self.context['request'].user
        if value == Ticket.Status.CLOSED and not (user.is_staff or user.is_agent):
            raise serializers.ValidationError(
                _('Only staff or agents can close tickets.')
            )
        return value
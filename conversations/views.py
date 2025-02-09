from rest_framework import viewsets, mixins
from rest_framework.exceptions import NotFound
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Message
from .serializers import MessageSerializer
from .permissions import HasTicketAccess
from tickets.models import Ticket
from django.http import Http404


class MessageViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    """
    ViewSet for managing ticket messages.
    """
    serializer_class = MessageSerializer
    permission_classes = [HasTicketAccess]

    @swagger_auto_schema(
        operation_description="Get all messages for a specific ticket",
        manual_parameters=[
            openapi.Parameter(
                'ticket_pk',
                openapi.IN_PATH,
                description="ID of the ticket",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        """Get all messages for a specific ticket"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new message for a specific ticket",
        manual_parameters=[
            openapi.Parameter(
                'ticket_pk',
                openapi.IN_PATH,
                description="ID of the ticket",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=MessageSerializer
    )
    def create(self, request, *args, **kwargs):
        """Create a new message for a specific ticket"""
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        """Messages ordered by creation date (newest first)"""
        return Message.objects.filter(
            ticket_id=self.kwargs['ticket_pk']
        ).select_related('sender').order_by('-created_at')

    def get_serializer_context(self):
        """Add ticket to context for validation"""
        context = super().get_serializer_context()
        context['ticket'] = self._get_ticket()
        return context

    def perform_create(self, serializer):
        """Auto-set sender and admin response flag"""
        serializer.save(
            ticket=self._get_ticket(),
            sender=self.request.user,
            is_admin_response=(
                self.request.user.is_staff or 
                self.request.user.is_agent
            )
        )

    def _get_ticket(self):
        """Retrieve and cache the ticket instance for the request lifecycle"""
        if not hasattr(self, '_ticket'):
            try:
                self._ticket = Ticket.objects.get(pk=self.kwargs['ticket_pk'])
            except Ticket.DoesNotExist:
                raise Http404(_('Ticket not found or access denied.'))  # Custom error message
        return self._ticket
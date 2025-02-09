from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from tickets.models import Ticket

class HasTicketAccess(BasePermission):
    """Verify user has access to the ticket's messages"""
    
    def has_permission(self, request, view):
        ticket = get_object_or_404(
            Ticket, 
            pk=view.kwargs.get('ticket_pk')
        )
        return (
            request.user == ticket.user or
            request.user.is_staff or
            request.user.is_agent
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
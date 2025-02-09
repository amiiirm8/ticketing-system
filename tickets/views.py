from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ticket
from .serializers import TicketSerializer
from .permissions import TicketPermission

class TicketViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing tickets
    
    - Users can create and manage their own tickets
    - Staff/Agents can manage all tickets
    - Filtering available on status/priority
    - Search by title/description
    - Ordering by creation/update date and priority
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [TicketPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'priority']
    ordering = ['-created_at']

    def get_queryset(self):
        """Return queryset filtered by user permissions"""
        user = self.request.user
        
        # Admins/Agents see all tickets
        if user.is_staff or user.is_agent:
            return self.queryset.all()
            
        # Regular users see only their tickets
        return self.queryset.filter(user=user)

    def perform_create(self, serializer):
        """Automatically associate ticket with current user"""
        serializer.save(user=self.request.user)
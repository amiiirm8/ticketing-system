from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'title', 
        'user', 
        'status', 
        'priority', 
        'created_at'
    ]
    
    list_filter = [
        'status', 
        'priority', 
        'created_at'
    ]
    
    search_fields = [
        'title', 
        'description', 
        'user__email'
    ]
    
    readonly_fields = [
        'created_at', 
        'updated_at'
    ]
    
    fieldsets = (
        (None, {'fields': ('user', 'title', 'description')}),
        ('Status', {'fields': ('status', 'priority')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
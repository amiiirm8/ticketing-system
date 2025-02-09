# conversations/admin.py
from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'sender', 'created_at')
    search_fields = ('ticket__title', 'sender__username', 'content')
    list_filter = ('ticket', 'sender')

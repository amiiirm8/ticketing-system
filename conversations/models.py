from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from tickets.models import Ticket

class Message(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name=_('ticket'),
        help_text=_('Associated ticket for this message')
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name=_('sender'),
        help_text=_('User who sent the message')
    )
    content = models.TextField(
        _('content'),
        help_text=_('Message content (minimum 1 character)')
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    is_admin_response = models.BooleanField(
        _('admin response'),
        default=False,
        help_text=_('Indicates official staff response')
    )

    class Meta:
        ordering = ['-created_at'] 
        indexes = [
            models.Index(fields=['ticket', 'created_at']),
            models.Index(fields=['is_admin_response']),
        ]
        verbose_name = _('message')
        verbose_name_plural = _('messages')

    def __str__(self):
        return f"Message #{self.id} on Ticket #{self.ticket_id}"
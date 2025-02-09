from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Ticket(models.Model):
    class Status(models.TextChoices):
        OPEN = 'open', _('Open')
        PENDING = 'pending', _('Pending')
        CLOSED = 'closed', _('Closed')

    class Priority(models.TextChoices):
        LOW = 'low', _('Low')
        MEDIUM = 'medium', _('Medium')
        HIGH = 'high', _('High')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets',
        verbose_name=_('user'),
        help_text=_('User who created the ticket')
    )
    title = models.CharField(
        _('title'),
        max_length=255,
        help_text=_('Short description of the issue')
    )
    description = models.TextField(
        _('description'),
        help_text=_('Detailed explanation of the problem')
    )
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
        help_text=_('Current resolution state of the ticket')
    )
    priority = models.CharField(
        _('priority'),
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        help_text=_('Urgency level of the ticket')
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['created_at']),
        ]
        verbose_name = _('ticket')
        verbose_name_plural = _('tickets')

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
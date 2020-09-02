from django.db.models.signals import post_save
from .models import TicketAttachment, Ticket
from django.dispatch import receiver


@receiver(post_save, sender=TicketAttachment)
def add_attachment(sender, instance, created, **kwargs):
    if created:
        TicketAttachment.objects.create(ticket=instance.ticket.ticket_id)

@receiver(post_save, sender=TicketAttachment)
def save_attachment(sender, instance, created, **kwargs):
    instance.ticket.save()
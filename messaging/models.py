from django.db import models
from django.contrib.auth import get_user_model

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

User = get_user_model()

class Ticket(models.Model):
    STATUSES = (
        ("pending", "pending"),
        ("assigned", "assigned"),
        ("closed", "closed")
    )

    PRIORITIES = (
        (1, "Low"),
        (2, "Medium"),
        (3, "High")
    )

    PRIORITY_KEYWORDS = ["loan", "approval"]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tickets")
    title = models.CharField(max_length=250, blank=False)
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_tickets")
    status = models.CharField(max_length=10, choices=STATUSES, default="pending")
    priority = models.PositiveIntegerField(choices=PRIORITIES, default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def notify_ws_agent(self):
        """
        Inform assigned client there is a new message.
        """
        notification = {
            'type': 'new_ticket',
            'ticket_id': '{}'.format(self.id)
        }

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)("{}".format(self.agent.id), notification)
        
    def save(self, *args, **kwargs):
        """Notify assigned agent of new ticket"""
        super(Ticket, self).save(*args, **kwargs)
        self.notify_ws_agent()


class Message(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="conversations")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    body = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def notify_ws_clients(self):
        """
        Inform client there is a new message.
        """
        notification = {
            'type': 'recieve_group_message',
            'message': '{}'.format(self.id)
        }

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)("{}".format(self.sender.id), notification)
        async_to_sync(channel_layer.group_send)("{}".format(self.recipient.id), notification)

    def save(self, *args, **kwargs):
        """
        Trims white spaces, saves the message and notifies the recipient via WS
        if the message is new.
        """
        new = self.id
        self.body = self.body.strip()  # Trimming whitespaces from the body
        super(Message, self).save(*args, **kwargs)
        if new is None:
            self.notify_ws_clients()

    class Meta:
        ordering = ('-date_created',)

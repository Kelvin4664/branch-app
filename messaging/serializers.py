from os import write
from rest_framework import serializers
from .models import Ticket, Message


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Message
        exclude = ("ticket",)
        read_only_fields = ("recipient", "sender")

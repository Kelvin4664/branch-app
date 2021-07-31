from django.contrib import admin
from .models import Ticket, Message

class MessageInline(admin.TabularInline):
    model = Message

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("user", "agent", "status", "priority", "date_created")
    list_filter = ("agent", "priority", "status")
    inlines = (MessageInline,)


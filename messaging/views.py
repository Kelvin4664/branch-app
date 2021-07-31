from django.db.models.aggregates import Count
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.response import Response
from .models import Message, Ticket, User
from .serializers import TicketSerializer, MessageSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.viewsets import ModelViewSet

class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication scheme used by DRF. DRF's SessionAuthentication uses
    Django's session framework for authentication which requires CSRF to be
    checked. In this case we are going to disable CSRF tokens for the API.
    """

    def enforce_csrf(self, request):
        return


class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tickets = None
        template = None
        context = dict()
        if request.user.user_type == "agent":
            context["tickets"] = request.user.assigned_tickets.all()
            template = "core/chat.html"
        else:
            context["tickets"] = request.user.created_tickets.all()
            template = "core/users.html"


        return render(request, template, context)

class TicketListView(ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get_queryset(self):
        if self.request.user.user_type == "agent":
            tickets = self.request.user.assigned_tickets.all()
        else:
            tickets = self.request.user.created_tickets.all()

        return tickets

    def create(self, request, *args, **kwargs):
        message = request.data.get("body")
        freest_agent = User.objects.filter(user_type="agent").annotate(
            num_tickets=Count("assigned_tickets")).order_by("num_tickets").first()

        ticket = Ticket.objects.create(
            user = request.user,
            agent = freest_agent,
            title = message[0:230],
            status = "assigned",
        )

        for keyword in Ticket.PRIORITY_KEYWORDS:
            if Ticket.objects.filter(title__icontains=keyword).exists():
                ticket.priority = 3
                ticket.save()
                break

        ticket.conversations.create(
            sender = request.user,
            recipient = freest_agent,
            body = message
        )

        return Response({"ticket_id":ticket.id})


class MessageViewset(ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (CsrfExemptSessionAuthentication,)
    queryset = Message.objects.all()

    def get_queryset(self):
        ticket_id = self.kwargs.get('ticket_id')
        ticket = Ticket.objects.get(id=ticket_id)
        return ticket.conversations.all()

    def perform_create(self, serializer):
        ticket_id = self.kwargs.get('ticket_id')
        ticket = Ticket.objects.get(id=ticket_id)

        if ticket.agent == self.request.user:
            recipient = ticket.user
        else:
            recipient = ticket.agent
        serializer.save(ticket=ticket, recipient=recipient, sender=self.request.user)

    

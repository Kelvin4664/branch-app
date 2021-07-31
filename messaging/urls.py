from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("messages", views.MessageViewset)

urlpatterns = [
    path('', views.HomeView.as_view(), name="homeview"),
    path('api/v1/tickets/', views.TicketListView.as_view()),
    path('api/v1/tickets/<int:ticket_id>/', include(router.urls))
]
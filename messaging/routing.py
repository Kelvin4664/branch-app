from . import consumers

from django.conf.urls import url

websocket_urlpatterns = [
    url(r'^ws$', consumers.ChatConsumer.as_asgi()),
]

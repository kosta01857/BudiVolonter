from django.urls import include, path

from .consumers import ChatConsumer

websocket_urlpatterns = [path("chat", ChatConsumer.as_asgi())]

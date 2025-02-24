from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from authentication.consumers import SensorConsumer
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/sensors/$', SensorConsumer.as_asgi()),
    # path('ws/sensor_data/', consumers.SensorDataConsumer.as_asgi()),
    path('ws/sensor_data/', consumers.SensorDataConsumer.as_asgi()),
]
# websocket_urlpatterns = [
#     path('ws/sensor_data/', consumers.SensorDataConsumer.as_asgi()),
# ]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})

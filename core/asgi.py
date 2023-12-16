import os


from django.core.asgi import get_asgi_application
from django.urls import path

from quiz.consumers import TestConsumer
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter


ws_urlpatterns = [

	path('ws/test_cons/', TestConsumer.as_asgi()),
]

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = ProtocolTypeRouter(
    {
        'http':     get_asgi_application(),
        'websocket': AuthMiddlewareStack(URLRouter(ws_urlpatterns))
    }
)
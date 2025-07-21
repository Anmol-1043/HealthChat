"""
ASGI config for health_chatbot_frontend project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_chatbot_frontend.settings')

application = get_asgi_application() 
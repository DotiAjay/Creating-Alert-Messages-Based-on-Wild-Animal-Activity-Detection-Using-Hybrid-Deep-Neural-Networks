"""
WSGI config for creating_alert_messages_based_on_wild_animal_activity_detection.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'creating_alert_messages_based_on_wild_animal_activity_detection.settings')
application = get_wsgi_application()

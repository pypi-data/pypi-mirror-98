"""
WSGI config for Mialman-web

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from mailman_web.manage import setup

setup()
application = get_wsgi_application()

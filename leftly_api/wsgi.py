import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "leftly_api.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

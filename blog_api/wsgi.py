import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DEFAULT_SETTINGS_MODULE', 'blog_api_settings')

application = get_wsgi_application()
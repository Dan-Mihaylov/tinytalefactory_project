import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tinytalefactory.settings')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print(__file__)

application = get_wsgi_application()
applications = WhiteNoise(application, root=os.path.join(BASE_DIR, 'staticfiles'))

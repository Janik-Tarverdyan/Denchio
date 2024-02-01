import sys
import os

# Set the path to your Django project and activate the virtual environment
sys.path.append('./')
os.environ['DJANGO_SETTINGS_MODULE'] = 'Denchio.settings'

# Create the application object
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()


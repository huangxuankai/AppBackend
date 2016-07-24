import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
path = BASE_DIR
if path not in sys.path:
    sys.path.insert(0, BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'AppBackend.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

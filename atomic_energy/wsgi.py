"""
WSGI config for atomic_energy project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application
from startup_tasks import check_log, check_media
from pathlib import Path



# path = '/var/www/atomic-energy-v2/'
BASE_DIR = Path(__file__).resolve().parent.parent

if BASE_DIR not in sys.path:
	sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atomic_energy.settings')

# if not os.path.exists('/var/www/atomic-energy-v2/logs'):  
if not os.path.exists(os.path.join(BASE_DIR, 'logs')):
    check_log(BASE_DIR)
    
if not os.path.exists(os.path.join(BASE_DIR, 'media')):
    check_media(BASE_DIR)  

os.environ['HTTPS'] = 'on'
os.environ['wsgi.url_scheme'] = 'https'

application = get_wsgi_application()


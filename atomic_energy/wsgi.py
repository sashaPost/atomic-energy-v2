"""
WSGI config for atomic_energy project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atomic_energy.settings')

# application = get_wsgi_application()

import os
import sys
from django.core.wsgi import get_wsgi_application

# sys.path.append(r'/home/alexback/atomic_energy/')
# sys.path.append(r'/home/alexback/atomic_energy/atomic_energy/')
path = '/home/alexback/atomic_energy/atomic_energy/'
if path not in sys.path:
	sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atomic_energy.settings')

os.environ['HTTPS'] = 'on'
os.environ['wsgi.url_scheme'] = 'https'

application = get_wsgi_application()

# print(sys.path)

import os, sys
sys.path.append('/home/ubuntu/work')
os.environ['DJANGO_SETTINGS_MODULE'] = 'maths.settings_production'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
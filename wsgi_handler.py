import os, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
sys.path.append('/sites/cmp/apps')

os.environ['DJANGO_SETTINGS_MODULE'] = 'cmp.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

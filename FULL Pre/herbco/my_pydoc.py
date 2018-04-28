import django
import pydoc
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'herbco.settings'
django.setup()
pydoc.cli()

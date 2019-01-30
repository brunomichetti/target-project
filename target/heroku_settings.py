import os
GDAL_LIBRARY_PATH = os.path.expandvars(os.getenv('GDAL_LIBRARY_PATH'))
GEOS_LIBRARY_PATH = os.path.expandvars(os.getenv('GEOS_LIBRARY_PATH'))
#DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# use PostgreSQL database
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'target-db',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'POST': '5432'
    },
    'original': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.path.join(BASE_DIR, 'db.postgis'),
    }
}

import os

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'circle_test',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'USERNAME': 'circleci',
        'PASSWORD': ''
    }
}

ONESIGNAL = {
    'app_id': '',
    'api_auth_key': ''
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

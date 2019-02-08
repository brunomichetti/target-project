
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

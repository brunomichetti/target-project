import os

GDAL_LIBRARY_PATH = os.path.expandvars(os.getenv('GDAL_LIBRARY_PATH'))
GEOS_LIBRARY_PATH = os.path.expandvars(os.getenv('GEOS_LIBRARY_PATH'))


DATABASES["default"]["ENGINE"] = 'django.contrib.gis.db.backends.postgis'


# ws settings
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': "channels_redis.core.RedisChannelLayer",
        'CONFIG': {
            'hosts': [os.environ.get('REDIS_URL', 'redis://localhost:6379'),
                      ],  # [('127.0.0.1', 'redis://localhost:6379')],
        },
    }
}


ONESIGNAL = {
    'app_id': os.environ.get('ONESIGNAL_APP_ID', ''),
    'api_auth_key': os.environ.get('ONESIGNAL_AUTH_KEY', '')
}


SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get('FB_APP_ID', '')
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get('FB_SECRET', '')


EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

DATABASES = {
   'default': {
       'ENGINE': 'django.contrib.gis.db.backends.postgis',
       'NAME': 'target-db',
       'USER': 'postgres',
       'PASSWORD': 'postgres',
       'HOST': 'localhost',
       'POST': '5432'
   }
}

DEBUG = True

ALLOWED_HOSTS = ['*']

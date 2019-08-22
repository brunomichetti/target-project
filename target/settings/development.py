EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'target.app.manager@gmail.com'
EMAIL_HOST_PASSWORD = 'target-app'

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

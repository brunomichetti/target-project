from django.conf.urls import url
from django.urls import path
from users.views import facebook_login

urlpatterns = [    
    url(r'^facebook-login/', facebook_login),
]

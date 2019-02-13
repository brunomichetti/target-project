from django.conf.urls import url

from users.views import facebook_login, CustomUserView

urlpatterns = [    
    url(r'^facebook-login/', facebook_login),
    url(r'', CustomUserView.as_view()),
]

from django.urls import path

from users.views import facebook_login, CustomUserView

urlpatterns = [    
    path('facebook-login/', facebook_login),
    path('', CustomUserView.as_view()),
]

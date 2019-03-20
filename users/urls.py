from django.urls import path

from users.views import facebook_login, test_one_signal, CustomUserView

urlpatterns = [
    path('facebook-login/', facebook_login),
    path('test-one-signal/', test_one_signal),
    path('', CustomUserView.as_view(), name='account_email_verification_sent'),
]

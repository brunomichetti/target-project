"""target URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from rest_auth.registration.views import VerifyEmailView
from rest_auth.views import PasswordResetView


from users.views import FacebookLogin, confirm_email, test_one_signal

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('rest-auth/registration/account-confirm-email/<str:key>/',
         confirm_email),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('rest-auth/account-confirm-email/', VerifyEmailView.as_view(),
         name='account_email_verification_sent'),
    path('rest-auth/password/reset/',
         PasswordResetView.as_view(), name='password_reset'),
    path('rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('rest-auth/', include('rest_auth.urls')),
    path('users/', include('users.urls')),
    path('targets/', include('targets.urls')),
    path('chat/', include('chat.urls')),
]

urlpatterns += [
    path('manifest.json', TemplateView.as_view(
        template_name='onesignal/manifest.json',
        content_type='application/json')
        ),
    path('OneSignalSDKWorker.js', TemplateView.as_view(
        template_name='onesignal/OneSignalSDKWorker.js',
        content_type='application/x-javascript')
        ),
    path('OneSignalSDKWorker.js', TemplateView.as_view(
        template_name='onesignal/OneSignalSDKWorker.js',
        content_type='application/x-javascript')
        ),
]

from django.shortcuts import render

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from django.views.generic.base import TemplateView


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


def facebook_login(request):
    return render(request, 'facebook-test.html', {})

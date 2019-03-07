
from allauth.socialaccount.providers.facebook.views import (
    FacebookOAuth2Adapter)
from django.utils.functional import SimpleLazyObject
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from rest_auth.registration.views import SocialLoginView
from rest_framework.permissions import IsAuthenticated

from users.models import CustomUser
from users.serializers import CustomUserProfileSerializer
from target.settings import FB_APP_ID, ONE_SIGNAL_APP_ID


class FacebookLogin(SocialLoginView):

    adapter_class = FacebookOAuth2Adapter


class CustomUserView(generics.ListAPIView):

    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomUserProfileSerializer


def confirm_email(request, key):
    return JsonResponse({"key": key})


def facebook_login(request):
    return render(request, 'facebook-test.html', {'fb_app_id': FB_APP_ID})


def test_one_signal(request):
    return render(
        request,
        'test-onesignal.html',
        {'onesignal_app_id': ONE_SIGNAL_APP_ID}
    )


def get_user_request(request):
    request_user = request.user
    if isinstance(request_user, SimpleLazyObject):
        request_user = request_user._wrapped
    return request_user

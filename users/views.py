from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView, APIView
from rest_framework.permissions import IsAuthenticated
from django.utils.functional import SimpleLazyObject

from users.serializers import UpdateProfileSerializer
from users.models import CustomUser


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class CustomUserView(APIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)

    def put(self, request, format=None):
        serializer = UpdateProfileSerializer(data=request.data)
        current_user = request.user
        if isinstance(current_user, SimpleLazyObject):
            current_user = current_user._wrapped
        if current_user.is_authenticated and serializer.is_valid():
            for key in request.data:
                if key in current_user.__dict__:
                    current_user.__dict__[key] = request.data[key]
            current_user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)


def facebook_login(request):
    return render(request, 'facebook-test.html', {})

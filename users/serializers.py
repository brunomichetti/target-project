from django.db import transaction
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import UserDetailsSerializer

from users.apps import GENDER_CHOICES
from users.models import CustomUser


class SignUpSerializer(RegisterSerializer):

    name = serializers.CharField(max_length=150)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES)
    id_notifications = serializers.CharField(max_length=200)

    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.name = request.data['name']
        user.gender = request.data['gender']
        user.id_notifications = request.data['id_notifications']
        user.save()
        return user


class CustomUserProfileSerializer(UserDetailsSerializer):

    email = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=150, required=False)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, required=False)

    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'gender')

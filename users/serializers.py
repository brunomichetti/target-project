from django.db import transaction
from django.utils.decorators import method_decorator
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer

from users.apps import GENDER_CHOICES
from users.models import CustomUser


class SignUpSerializer(RegisterSerializer):
    name = serializers.CharField(max_length=150)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES)

    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.name = request.data['name']
        user.gender = request.data['gender']
        user.save()
        return user


class UpdateProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=150, required=False)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, required=False)

    class Meta:
        model = CustomUser
        fields = ('name', 'gender')

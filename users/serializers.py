from django.db import transaction
from django.utils.decorators import method_decorator
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer

from users.models import CustomUser


class SignUpSerializer(RegisterSerializer):
    name = serializers.CharField(max_length=150)
    gender = serializers.CharField(max_length=1)

    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.name = request.data['name']
        user.gender = request.data['gender']
        user.save()
        return user


class UpdateProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=150, required=False)
    gender = serializers.CharField(max_length=1, required=False)

    class Meta:
        model = CustomUser
        fields = ('name', 'gender')

    def validate_gender(self, gender):
        if not gender in ('M', 'F'):
            raise serializers.ValidationError('This field must be M or F.')
        return gender

from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from . import models
from users.models import CustomUser
from django.db import transaction


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

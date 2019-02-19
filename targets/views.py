import json
import pdb

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils.functional import SimpleLazyObject
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models import PointField

from targets.models import Target
from targets.serializers import TargetSerializer
from users.apps import MAX_TARGETS_PER_USER


class TargetView(APIView):
    serializer_class = TargetSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        current_user = request.user
        if isinstance(current_user, SimpleLazyObject):
            current_user = current_user._wrapped
        if current_user.is_authenticated:
            user_targets = Target.objects.filter(user_id=current_user.id)
            serializer = TargetSerializer(user_targets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def post(self, request, format=None):
        serializer = TargetSerializer(data=request.data)
        current_user = request.user
        if isinstance(current_user, SimpleLazyObject):
            current_user = current_user._wrapped
        if current_user.is_authenticated:
            if serializer.is_valid():
                user_targets = Target.objects.filter(user_id=current_user.id)
                if user_targets.count() >= MAX_TARGETS_PER_USER:
                    return Response("Users can't register more than " + str(MAX_TARGETS_PER_USER) + " targets.", status=status.HTTP_400_BAD_REQUEST)
                else:
                    j_pos = json.loads(request.data['position'])
                    new_target = Target(user_id=current_user.id, title=request.data["title"], topic=request.data["topic"],
                                        radius_in_m=request.data["radius_in_m"], position=Point(j_pos["latitude"], j_pos["longitude"]))
                    new_target.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

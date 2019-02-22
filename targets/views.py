import json
from django.db import transaction
from django.utils.functional import SimpleLazyObject
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import GEOSGeometry
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from targets.models import Target, Match
from targets.serializers import TargetSerializer, MatchSerializer
from users.apps import MAX_TARGETS_PER_USER
from users.views import get_user_request


class TargetView(APIView):

    serializer_class = TargetSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        current_user = get_user_request(request)
        if current_user.is_authenticated:
            user_targets = Target.objects.filter(user_id=current_user.id)
            serializer = TargetSerializer(user_targets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_403_FORBIDDEN)

    def post(self, request, format=None):
        serializer = TargetSerializer(data=request.data)
        current_user = get_user_request(request)
        if current_user.is_authenticated:
            if serializer.is_valid():
                user_targets = Target.objects.filter(user_id=current_user.id)
                if user_targets.count() >= MAX_TARGETS_PER_USER:
                    return Response(
                        "Users can't register more than "
                        f"{MAX_TARGETS_PER_USER} targets.",
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    j_pos = json.loads(request.data['position'])
                    new_target = Target(
                        user_id=current_user.id,
                        title=request.data["title"],
                        topic=request.data["topic"],
                        radius_in_m=float(request.data["radius_in_m"]),
                        position=Point(
                            j_pos["latitude"],
                            j_pos["longitude"])
                    )
                    new_target.save()
                    self.generate_matches(new_target, current_user)
                    return Response(serializer.data,
                                    status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_403_FORBIDDEN)

    @transaction.atomic
    def generate_matches(self, target, user):
        not_user_targets = Target.objects.exclude(user_id=user.id)
        for current_t in not_user_targets:
            if self.targets_match(target, current_t):
                new_match = Match(
                    target_1=target, target_2=current_t, topic=target.topic)
                new_match.save()

    def targets_match(self, t1, t2):
        return (t1.topic == t2.topic and
                t1.position.distance(t2.position) <=
                (t1.radius_in_m + t2.radius_in_m))


class TargetMatchView(APIView):

    serializer_class = MatchSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        current_user = get_user_request(request)
        if current_user.is_authenticated:
            user_targets = Target.objects.filter(user_id=current_user.id)
            matches = Match.objects.none()
            for t in user_targets:
                matches_of_target = Match.objects.filter(
                    Q(target_1=t) | Q(target_2=t))
                matches = matches | matches_of_target
            serializer = MatchSerializer(matches, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

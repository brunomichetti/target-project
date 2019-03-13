from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.http import Http404

from chat.models import MatchMessage, MessageResultsSetPagination
from chat.serializers import MatchMessageSerializer
from targets.models import Target, Match
from targets.serializers import TargetSerializer, MatchSerializer
from users.views import get_user_request


class TargetView(generics.ListCreateAPIView):

    queryset = Target.objects.all()
    serializer_class = TargetSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        current_user = get_user_request(self.request)
        return self.queryset.filter(user=current_user)

    def perform_create(self, serializer):
        current_user = get_user_request(self.request)
        serializer.save(user=current_user)


class TargetMatchesView(generics.ListAPIView):

    serializer_class = MatchSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        current_user = get_user_request(self.request)
        user_targets = Target.objects.filter(user_id=current_user.id)
        query_matches = Match.objects.none()
        for t in user_targets:
            matches_of_target = Match.objects.filter(
                Q(target_1=t) | Q(target_2=t)
            )
            query_matches = query_matches | matches_of_target
        return query_matches


class TargetDetailView(generics.DestroyAPIView):

    queryset = Target.objects.all()
    serializer_class = TargetSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        current_user = get_user_request(self.request)
        return self.queryset.filter(user=current_user)


class MatchMessagesDetailView(generics.ListAPIView):

    queryset = MatchMessage.objects.all()
    serializer_class = MatchMessageSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = MessageResultsSetPagination

    def get_queryset(self):
        current_t = Target.objects.get(id=self.kwargs['t_id'])
        current_m = Match.objects.get(id=self.kwargs['m_id'])
        if not(current_t.id in [current_m.target_1_id, current_m.target_2_id]):
            raise Http404("The match doesn't belong to the target")
        queryset = MatchMessage.objects.filter(
            in_match=self.kwargs['m_id']
        )
        return self.queryset

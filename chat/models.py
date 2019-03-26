from django.db import models
from rest_framework.pagination import PageNumberPagination

from targets.models import Match
from users.models import CustomUser


class MatchMessage(models.Model):
    in_match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    content = models.CharField(max_length=350)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='creator'
    )
    seen_at = models.DateTimeField(null=True, default=None)


class MessageResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 200

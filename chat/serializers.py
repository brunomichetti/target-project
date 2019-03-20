from rest_framework import serializers

from chat.models import MatchMessage


class MatchMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = MatchMessage
        fields = ('sent_by', 'content', 'created_at',)

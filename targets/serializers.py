from rest_framework import serializers

from drf_extra_fields.geo_fields import PointField

from targets.models import Target, Match
from targets.apps import TOPIC_CHOICES


class TargetSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=60)
    topic = serializers.ChoiceField(choices=TOPIC_CHOICES)
    position = PointField()
    radius_in_m = serializers.FloatField()

    class Meta:
        model = Target
        fields = ('title', 'topic', 'position', 'radius_in_m')

    def validate_radius_in_m(self, value):
        if value < 0.0:
            raise serializers.ValidationError(
                'radius must be equal or higher than 0.')
        return value


class MatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Match
        fields = ('target_1', 'target_2', 'topic')

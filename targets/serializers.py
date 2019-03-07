from rest_framework import serializers

from drf_extra_fields.geo_fields import PointField

from targets.models import Target, Match
from targets.apps import TOPIC_CHOICES
from users.apps import MAX_TARGETS_PER_USER


class TargetSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=60)
    topic = serializers.ChoiceField(choices=TOPIC_CHOICES)
    position = PointField()
    radius_in_m = serializers.FloatField()

    class Meta:
        model = Target
        fields = ('id', 'title', 'topic', 'position', 'radius_in_m', )

    def validate(self, attrs):
        current_user = self.context['request'].user
        user_targets = Target.objects.filter(user_id=current_user.id)
        if (user_targets.count() >= MAX_TARGETS_PER_USER):
            raise serializers.ValidationError(
                "Users can't register more than "
                f"{MAX_TARGETS_PER_USER} targets."
            )
        else:
            return super().validate(attrs)

    def validate_radius_in_m(self, value):
        if value < 0.0:
            raise serializers.ValidationError(
                'radius must be equal or higher than 0.')
        return value


class MatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Match
        fields = ('target_1', 'target_2', 'topic')

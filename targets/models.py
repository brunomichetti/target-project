from django.db import models
from django.contrib.gis.db.models import PointField

from users.models import CustomUser
from targets.apps import TOPIC_CHOICES


class Target(models.Model):
    title = models.CharField(max_length=60)
    topic = models.CharField(max_length=50, choices=TOPIC_CHOICES)
    position = PointField()
    radius_in_m = models.FloatField(default=0.0)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='targets')

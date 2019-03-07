from django.db import models
from django.contrib.gis.db.models import PointField

from targets.apps import TOPIC_CHOICES
from users.models import CustomUser


class Target(models.Model):
    title = models.CharField(max_length=60)
    topic = models.CharField(max_length=50, choices=TOPIC_CHOICES)
    position = PointField()
    radius_in_m = models.FloatField(default=0.0)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='targets')


class Match(models.Model):
    target_1 = models.ForeignKey(
        Target, on_delete=models.CASCADE, related_name='target_1')
    target_2 = models.ForeignKey(
        Target, on_delete=models.CASCADE, related_name='target_2')
    topic = models.CharField(max_length=50, choices=TOPIC_CHOICES)

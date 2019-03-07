import factory
import random

from django.contrib.gis.geos import Point

from targets.apps import TOPIC_CHOICES, NUMBER_OF_TOPICS
from targets.models import Target
from users.factory import CustomUserFactory


class TargetFactory(factory.DjangoModelFactory):

    title = factory.Sequence(lambda n: "Title %03d" % n)
    topic = TOPIC_CHOICES[random.randint(0, NUMBER_OF_TOPICS-1)][0]
    radius_in_m = factory.LazyAttribute(
        lambda m: round(random.uniform(0.0, 100.0), 4))
    position = Point(round(random.uniform(-180.0, 180.0), 5),
                     round(random.uniform(-90.0, 90.0), 5))
    user = factory.SubFactory(CustomUserFactory)

    class Meta:
        model = Target


class MatchFactory(factory.DjangoModelFactory):

    target_1 = factory.SubFactory(TargetFactory)
    target_2 = factory.SubFactory(TargetFactory)
    topic = TOPIC_CHOICES[random.randint(0, NUMBER_OF_TOPICS-1)][0]

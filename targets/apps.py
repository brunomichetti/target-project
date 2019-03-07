from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save


class TargetsConfig(AppConfig):
    name = 'targets'


TOPIC_CHOICES = (
    ('Football', _('Football')),
    ('Travel', _('Travel')),
    ('Politics', _('Politics')),
    ('Art', _('Art')),
    ('Dating', _('Dating')),
    ('Music', _('Music')),
    ('Movies', _('Movies')),
    ('Series', _('Series')),
    ('Food', _('Food')),
)

NUMBER_OF_TOPICS = len(TOPIC_CHOICES)


class TargetsConfig(AppConfig):
    name = 'targets'

    def ready(self):
        from .signals import generate_matches
        from .models import Target
        post_save.connect(generate_matches, sender=Target)

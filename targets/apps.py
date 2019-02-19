from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


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

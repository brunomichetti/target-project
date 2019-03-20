from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):

    name = 'users'


GENDER_CHOICES = (
    ('M', _('Male')),
    ('F', _('Female')),
)

NUMBER_OF_GENDERS = len(GENDER_CHOICES)

MAX_TARGETS_PER_USER = 10

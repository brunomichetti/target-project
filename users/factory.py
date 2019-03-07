import random
import factory
from faker import Faker
from faker.providers import person, profile, misc

from users.models import CustomUser
from users.apps import GENDER_CHOICES, NUMBER_OF_GENDERS


fake = Faker()
fake.add_provider(person)
fake.add_provider(profile)
fake.add_provider(misc)


class CustomUserFactory(factory.DjangoModelFactory):

    name = fake.name()  # pylint: disable=no-member
    email = fake.email()  # pylint: disable=no-member
    gender = GENDER_CHOICES[  # pylint: disable=no-member
        random.randint(0, NUMBER_OF_GENDERS-1)][0]
    username = fake.simple_profile()['username']  # pylint: disable=no-member
    password = fake.password(  # pylint: disable=no-member
        length=10,
        special_chars=True,
        digits=True,
        upper_case=True,
        lower_case=True
    )
    id_notifications = fake.uuid4()  # pylint: disable=no-member

    class Meta:
        model = CustomUser

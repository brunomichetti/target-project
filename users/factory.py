import factory
from faker import Faker
from faker.providers import person, profile

from users.models import CustomUser


fake = Faker()
fake.add_provider(person)
fake.add_provider(profile)


class CustomUserFactory(factory.DjangoModelFactory):
    name = fake.name()  # pylint: disable=no-member
    email = fake.email()  # pylint: disable=no-member
    gender = factory.Iterator(['M', 'F'])  # pylint: disable=no-member
    username = fake.simple_profile()['username']  # pylint: disable=no-member
    password = fake.password(  # pylint: disable=no-member
                    length=10,
                    special_chars=True,
                    digits=True,
                    upper_case=True,
                    lower_case=True
                )

    class Meta:
        model = CustomUser

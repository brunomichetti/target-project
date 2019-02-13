import factory
from faker import Faker

from users.models import CustomUser
faker = Faker()


class CustomUserFactory(factory.DjangoModelFactory):    
    name = faker.name()
    email = faker.email()
    gender = factory.Iterator(['M', 'F'])
    username = faker.simple_profile(sex=None)['username']
    password = faker.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)

    class Meta:
        model = CustomUser


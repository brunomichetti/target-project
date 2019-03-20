import pytest
import random
import unittest
from faker import Faker
from faker.providers import lorem

from channels.testing import WebsocketCommunicator

from chat.consumers import ChatConsumer
from chat.models import MatchMessage
from users.factory import CustomUserFactory
from targets.factory import MatchFactory, TargetFactory


fake = Faker()
fake.add_provider(lorem)


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_consumers():
    # initial data
    user1 = CustomUserFactory(
                username='user1test',
                email='user1@test.com'
            )
    user2 = CustomUserFactory(
            username='user2test',
            email='user2@test.com'
        )
    target1 = TargetFactory(user=user1)
    target2 = TargetFactory(user=user2)
    match_1_2 = MatchFactory(target_1=target1, target_2=target2)
    # chat user 1
    communicator_1 = WebsocketCommunicator(
        ChatConsumer,
        'chat/'f'{match_1_2.id}''/'
    )
    communicator_1.scope['user'] = user1
    communicator_1.scope['url_route'] = {
        'args': (),
        'kwargs': {'match_id': match_1_2.id}
    }
    # chat user 2
    communicator_2 = WebsocketCommunicator(
        ChatConsumer,
        'chat/'f'{match_1_2.id}''/'
    )
    communicator_2.scope['user'] = user2
    communicator_2.scope['url_route'] = {
        'args': (),
        'kwargs': {'match_id': match_1_2.id}
    }
    connected, subprotocol = await communicator_1.connect()
    assert connected
    connected, subprotocol = await communicator_2.connect()
    assert connected
    # messages
    hello = fake.sentence(  # pylint: disable=no-member
        nb_words=random.randint(2, 20),
        variable_nb_words=True,
        ext_word_list=None
    )
    answer = fake.sentence(  # pylint: disable=no-member
        nb_words=random.randint(2, 20),
        variable_nb_words=True,
        ext_word_list=None
    )
    # Test sending text
    await communicator_1.send_json_to({'message': hello})
    response = await communicator_1.receive_json_from()
    assert response['message'] == 'You : ' f'{hello}'
    response = await communicator_2.receive_json_from()
    assert response['message'] == f'{user1.name}' ' : ' f'{hello}'
    await communicator_2.send_json_to({'message': answer})
    response = await communicator_1.receive_json_from()
    assert response['message'] == f'{user2.name}' ' : ' f'{answer}'
    response = await communicator_2.receive_json_from()
    assert response['message'] == 'You : ' f'{answer}'
    # check MatchMessage were save
    assert MatchMessage.objects.filter(
        sent_by=user1,
        content=hello,
    ).exists
    assert MatchMessage.objects.filter(
        sent_by=user2,
        content=answer,
    ).exists
    # Close
    await communicator_1.disconnect()
    await communicator_2.disconnect()

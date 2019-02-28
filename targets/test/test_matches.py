import random
import json

from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.gis.geos import Point

from targets.apps import TOPIC_CHOICES, NUMBER_OF_TOPICS
from users.factory import CustomUserFactory
from targets.factory import TargetFactory
from targets.models import Target, Match


class CreateMatchesTestCase(APITestCase):

    def setUp(self):
        self.user1 = CustomUserFactory(
                        username='user1test',
                        email='user1@test.com'
                    )
        self.user2 = CustomUserFactory(
                        username='user2test',
                        email='user2@test.com'
                    )
        self.data_t1_u1 = {
            'position': json.dumps({"longitude": 1, "latitude": 1}),
            'radius_in_m': 5.1,
            'topic': 'Football',
            'title': 't1_of_u1'
        }
        self.data_t2_u1 = {
            'position': json.dumps({"longitude": -1123, "latitude": 12.26}),
            'radius_in_m': 15.7,
            'topic': 'Art',
            'title': 't2_of_u1'
        }
        self.data_t1_u2 = {
            'position': json.dumps({"longitude": 11, "latitude": 10}),
            'radius_in_m': 15,
            'topic': 'Football',
            'title': 't1_of_u2'
        }
        self.data_t2_u2 = {
            'position': json.dumps({"longitude": -87.77, "latitude": -391.55}),
            'radius_in_m': 9.04,
            'topic': 'Politics',
            'title': 't2_of_u2'
        }

    def test_create_correct_target_and_matches(self):
        self.client.force_authenticate(self.user1)  # pylint: disable=no-member
        self.client.post('/targets/', self.data_t1_u1, format='json')
        self.client.post('/targets/', self.data_t2_u1, format='json')
        self.client.logout()
        self.client.force_authenticate(self.user2)  # pylint: disable=no-member
        self.client.post('/targets/', self.data_t1_u2, format='json')
        self.client.post('/targets/', self.data_t2_u2, format='json')
        self.client.logout()
        self.assertEqual(Match.objects.count(), 1)
        t1_u1 = Target.objects.filter(title='t1_of_u1').get()
        t1_u2 = Target.objects.filter(title='t1_of_u2').get()
        self.client.force_authenticate(self.user1)  # pylint: disable=no-member
        response = self.client.get('/targets/matches/')
        self.assertEqual(response.data[0]['target_1'], t1_u2.id)
        self.assertEqual(response.data[0]['target_2'], t1_u1.id)
        self.assertEqual(response.data[0]['topic'], 'Football')

    def test_100_matches_with_fixed_topic(self):
        fixed_topic = TOPIC_CHOICES[random.randint(0, NUMBER_OF_TOPICS-1)][0]
        for i in range(10):
            x = random.uniform(-2.0, 2.0)
            y = random.uniform(-2.0, 2.0)
            TargetFactory.create(
                            user=self.user1,
                            topic=fixed_topic,
                            position=Point(x, y),
                            radius_in_m=random.uniform(5.0, 20.0)
                        )
        targets_data_u2 = []
        for i in range(10):
            x = random.uniform(-2.0, 2.0)
            y = random.uniform(-2.0, 2.0)
            new_data = {
                'position': json.dumps({"longitude": x, "latitude": y}),
                'radius_in_m': random.uniform(5.0, 20.0),
                'topic': fixed_topic,
                'title': 'title ' + str(x) + str(y),
            }
            targets_data_u2.append(new_data)
        self.client.force_login(self.user2)
        for d_t in targets_data_u2:
            self.client.post('/targets/', d_t, format='json')
        self.assertEqual(Match.objects.count(), 100)

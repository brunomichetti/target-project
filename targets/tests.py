import random
import pdb
import json
import factory

from django.test import TestCase
from rest_framework.test import APITestCase

from users.factory import CustomUserFactory
from targets.apps import TOPIC_CHOICES, NUMBER_OF_TOPICS
from targets.factory import TargetFactory
from targets.models import Target


class CreateTargetTestCase(APITestCase):

    def generate_json_from_position(self, pos):
        longitude = pos[0]
        latitude = pos[1]
        pos = {"longitude": longitude, "latitude": latitude}
        json_pos = json.dumps(pos)
        return json_pos

    def setUp(self):
        self.user1 = CustomUserFactory(
            username='user1test', email='user1@test.com')
        self.user2 = CustomUserFactory(
            username='user2test', email='user2@test.com')
        self.target = TargetFactory(user=self.user1)
        self.data = {
            'position': self.generate_json_from_position(self.target.position),
            'radius_in_m': self.target.radius_in_m,
            'topic': self.target.topic,
            'title': self.target.title
        }

    def test_correct_create_target(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post('/targets/', self.data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_error_create_more_than_10_targets(self):
        TargetFactory.create_batch(10, user=self.user2)
        self.client.force_authenticate(self.user2)
        response = self.client.post('/targets/', self.data, format='json')
        self.assertEqual(response.status_code, 400)
        user_targets = Target.objects.filter(user_id=self.user2.id)        
        self.assertEqual(user_targets.count(), 10)
        self.assertEqual(response.data, "Users can't register more than 10 targets.")

        

    def test_missing_field_error(self):
        self.data = {
            'position': self.generate_json_from_position(self.target.position),
            'radius_in_m': self.target.radius_in_m,
            'topic': self.target.topic,
        }
        self.client.force_authenticate(self.user2)
        response = self.client.post('/targets/', self.data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['title'][0]
                         [0:], 'This field is required.')

    def test_incorrect_radius_in_m_error(self):
        neg_radius = round(random.uniform(0.0001, 100.0), 4)*(-1)
        self.data = {
            'position': self.generate_json_from_position(self.target.position),
            'radius_in_m': neg_radius,
            'topic': self.target.topic,
            'title': self.target.title
        }
        self.client.force_authenticate(self.user1)
        response = self.client.post('/targets/', self.data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['radius_in_m'][0]
                         [0:], 'radius must be equal or higher than 0.')

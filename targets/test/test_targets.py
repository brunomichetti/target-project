import json
import random

from django.contrib.gis.geos import Point
from rest_framework.test import APITestCase

from targets.apps import TOPIC_CHOICES, NUMBER_OF_TOPICS
from targets.factory import TargetFactory, MatchFactory
from targets.models import Target, Match
from users.factory import CustomUserFactory


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
        self.client.force_authenticate(  # pylint: disable=no-member
            user=self.user1
        )
        response = self.client.post('/targets/', self.data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_error_create_more_than_10_targets(self):
        TargetFactory.create_batch(10, user=self.user2)
        self.client.force_authenticate(self.user2)  # pylint: disable=no-member
        response = self.client.post('/targets/', self.data, format='json')
        self.assertEqual(response.status_code, 400)
        user_targets = Target.objects.filter(user_id=self.user2.id)
        self.assertEqual(user_targets.count(), 10)
        self.assertEqual(
            response.data['non_field_errors'][0][0:],
            "Users can't register more than 10 targets."
        )

    def test_missing_field_error(self):
        self.data = {
            'position': self.generate_json_from_position(self.target.position),
            'radius_in_m': self.target.radius_in_m,
            'topic': self.target.topic,
        }
        self.client.force_authenticate(self.user2)  # pylint: disable=no-member
        response = self.client.post('/targets/', self.data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['title'][0]
                         [0:], 'This field is required.')

    def test_incorrect_radius_in_m_error(self):
        neg_radius = round(random.uniform(-100, 0.0001), 4)
        self.data = {
            'position': self.generate_json_from_position(self.target.position),
            'radius_in_m': neg_radius,
            'topic': self.target.topic,
            'title': self.target.title
        }
        self.client.force_authenticate(self.user1)  # pylint: disable=no-member
        response = self.client.post('/targets/', self.data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['radius_in_m'][0]
                         [0:], 'radius must be equal or higher than 0.')


class DeleteTargetTestCase(APITestCase):

    def setUp(self):
        self.user1 = CustomUserFactory(
            username='user1test', email='user1@test.com')
        self.user2 = CustomUserFactory(
            username='user2test', email='user2@test.com')
        self.target = TargetFactory(user=self.user1)

    def test_correct_delet_target(self):
        self.assertEqual(Target.objects.count(), 1)
        self.client.force_authenticate(self.user1)  # pylint: disable=no-member
        delete_id = str(self.target.id) + '/'
        response = self.client.delete('/targets/' + delete_id)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Target.objects.count(), 0)

    def test_not_owner_delete_target(self):
        target2 = TargetFactory(user=self.user2)
        self.assertEqual(Target.objects.count(), 2)
        delete_id = str(target2.id) + '/'
        self.client.force_authenticate(self.user1)  # pylint: disable=no-member
        response = self.client.delete('/targets/' + delete_id)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Target.objects.count(), 2)

    def test_delete_not_existing_target(self):
        self.assertEqual(Target.objects.count(), 1)
        self.client.force_authenticate(self.user1)  # pylint: disable=no-member
        delete_id = str(self.target.id + 1) + '/'
        response = self.client.delete('/targets/' + delete_id)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Target.objects.count(), 1)

    def test_delete_10_targets_and_100_matches(self):
        Target.objects.filter(id=self.target.id).delete()
        fixed_topic = TOPIC_CHOICES[random.randint(0, NUMBER_OF_TOPICS-1)][0]
        x = random.uniform(-2.0, 2.0)
        y = random.uniform(-2.0, 2.0)
        targets_user1 = TargetFactory.create_batch(
            10,
            user=self.user1,
            topic=fixed_topic,
            position=Point(x, y)
        )
        targets_user2 = TargetFactory.create_batch(
            10,
            user=self.user2,
            topic=fixed_topic,
            position=Point(x, y)
        )
        self.assertEqual(Match.objects.count(), 100)
        self.client.force_authenticate(self.user1)  # pylint: disable=no-member
        for t in targets_user1:
            delete_id = str(t.id) + '/'
            self.client.delete('/targets/' + delete_id)
        self.assertEqual(Match.objects.count(), 0)

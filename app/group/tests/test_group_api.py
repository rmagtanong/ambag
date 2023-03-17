"""
Tests for Group API
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Group

GROUP_URL = reverse('group:group-list')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_user_payload():
    return {
        'email': 'test@example.com',
        'password': 'test1234',
        'name': 'Test'
    }


class PublicGroupApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(GROUP_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateGroupExpenseApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(**create_user_payload())
        self.client.force_authenticate(self.user)

    def test_create_group_success(self):
        payload = {
            'group_name': 'Test Group'
        }

        res = self.client.post(GROUP_URL, payload)

        group = Group.objects.get(id=res.data['id'])

        self.assertEqual(res.data['group_name'], group.group_name)
        self.assertEqual(self.user, group.group_members.first())
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

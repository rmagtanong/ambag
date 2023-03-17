"""
Tests for Group API
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Group
from group.serializers import GroupSerializer

GROUP_URL = reverse('group:group-list')


def detail_url(group_id):
    return reverse('group:group-join', args=[group_id])


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_user_payload():
    return {
        'email': 'test@example.com',
        'password': 'test1234',
        'name': 'Test'
    }


def create_other_user_payload():
    return {
        'email': 'other@example.com',
        'password': 'other1234',
        'name': 'Other'
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

    def test_list_groups_member_only(self):
        self.client.post(GROUP_URL, {'group_name': 'Group 1'})
        self.client.post(GROUP_URL, {'group_name': 'Group 2'})

        self.user = create_user(**create_other_user_payload())
        self.client.force_authenticate(self.user)

        res = self.client.get(GROUP_URL)

        self.assertEqual(len(res.data), 0)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_join_group(self):
        group = self.client.post(GROUP_URL, {'group_name': 'Test Group'})
        group_id = group.data['id']

        self.user = create_user(**create_other_user_payload())
        self.client.force_authenticate(self.user)

        res = self.client.post(detail_url(group_id), payload={'group_name': 'Test Group'})

        group = Group.objects.get(id=group_id)
        serializer = GroupSerializer(group)

        self.assertEqual(len(serializer.data['group_members']), 2)
        self.assertEqual(serializer.data['group_members'][0]['name'], 'Test')
        self.assertEqual(serializer.data['group_members'][1]['name'], 'Other')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_join_group_existing_member(self):
        group = self.client.post(GROUP_URL, {'group_name': 'Test Group'})
        group_id = group.data['id']

        res = self.client.post(detail_url(group_id), payload={'group_name': 'Test Group'})

        group = Group.objects.get(id=group_id)
        serializer = GroupSerializer(group)

        self.assertEqual(len(serializer.data['group_members']), 1)
        self.assertEqual(serializer.data['group_members'][0]['name'], 'Test')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

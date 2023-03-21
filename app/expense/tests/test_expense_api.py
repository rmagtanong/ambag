"""
Test Expense API
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Group, Expense


GROUP_URL = reverse('group:group-list')


def detail_url(group_id):
    return reverse('group:expense-list', kwargs={'group_id': group_id})


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


def create_group(user):
    group = Group.objects.create(group_name='Test Group')
    group.group_members.add(user)
    return group


class PrivateExpenseApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(**create_user_payload())
        self.client.force_authenticate(self.user)

    def test_create_expense_success(self):
        group = create_group(self.user)
        other_user = create_user(**create_other_user_payload())
        payload = {
            'expense_name': 'Test Expense',
            'amount': Decimal('1.00'),
            'paid_by': self.user.email,
            'expense_members': [self.user.email,
                                other_user.email]
        }

        res = self.client.post(detail_url(group.pk), payload)

        expense = Expense.objects.get(id=res.data['id'])

        self.assertEqual(res.data['expense_name'], expense.expense_name)
        self.assertEqual(res.data['group']['id'], expense.group.pk)
        self.assertEqual(res.data['group']['group_name'], expense.group.group_name)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

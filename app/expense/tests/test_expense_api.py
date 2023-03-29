"""
Test Expense API
"""
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Group, Expense
from core.repository.expense_repository import ExpenseRepository


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

        self.group = create_group(self.user)
        self.other_user = create_user(**create_other_user_payload())

    def test_create_expense_success(self):
        payload = {
            'expense_name': 'Test Expense',
            'amount': Decimal('1.00'),
            'paid_by': self.user.email,
            'expense_members': [self.user.email,
                                self.other_user.email]
        }

        res = self.client.post(detail_url(self.group.pk), payload)

        expense = Expense.objects.get(id=res.data['id'])

        self.assertEqual(res.data['expense_name'], expense.expense_name)
        self.assertEqual(res.data['group']['id'], expense.group.pk)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_expense_invalid_paid_by(self):
        payload = {
            'expense_name': 'Test Expense',
            'amount': Decimal('1.00'),
            'paid_by': 'invalid_email',
            'expense_members': [self.user.email,
                                self.other_user.email]
        }

        with self.assertRaises(ValidationError) as cm:
            self.client.post(detail_url(self.group.pk), payload)

        expected_err_msg = 'paid_by email invalid, email=invalid_email'
        actual_err_msg = str(cm.exception.message)

        self.assertEqual(actual_err_msg, expected_err_msg)

    def test_create_expense_invalid_expense_member_email(self):
        payload = {
            'expense_name': 'Test Expense',
            'amount': Decimal('1.00'),
            'paid_by': self.user.email,
            'expense_members': [self.user.email,
                                'invalid_email']
        }

        with self.assertRaises(ValidationError) as cm:
            self.client.post(detail_url(self.group.pk), payload)

        expected_err_msg = 'expense_member email invalid, email=invalid_email'
        actual_err_msg = str(cm.exception.message)

        self.assertEqual(actual_err_msg, expected_err_msg)

    def test_create_expense_empty_members(self):
        payload = {
            'expense_name': 'Test Expense',
            'amount': Decimal('1.00'),
            'paid_by': self.user.email,
            'expense_members': []
        }

        with self.assertRaises(ValidationError) as cm:
            self.client.post(detail_url(self.group.pk), payload)

        expected_err_msg = 'expense_members should have at least 1 user'
        actual_err_msg = str(cm.exception.message)

        self.assertEqual(actual_err_msg, expected_err_msg)

    def test_get_all_expenses_per_group(self):
        ExpenseRepository.create_expense(
            expense_name='Test Expense 1',
            amount=1,
            group=self.group,
            paid_by=self.user,
            expense_members=[self.user,
                             self.other_user]
        )

        ExpenseRepository.create_expense(
            expense_name='Test Expense 2',
            amount=1,
            group=self.group,
            paid_by=self.user,
            expense_members=[self.user,
                             self.other_user]
        )

        res = self.client.get(detail_url(self.group.pk))

        self.assertEqual(len(res.data), 2)

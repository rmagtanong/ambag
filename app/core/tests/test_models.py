"""
Tests for Models
"""
from decimal import Decimal
from datetime import date

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user():
    return get_user_model().objects.create_user(
        email='test@example.com',
        password='test1234')


def create_other_user():
    return get_user_model().objects.create_user(
        email='other@example.com',
        password='other1234')


def create_group(user):
    group = models.Group.objects.create(group_name='Test Group')
    group.group_members.add(user)
    return group


class UserModelTests(TestCase):

    def test_create_user_with_email_success(self):
        email = 'test@example.com'
        password = 'test1234'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        sample_emails = [
            ['test1@EXAMPLE.COM', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test1234'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class GroupModelTests(TestCase):

    def test_create_group(self):
        group = models.Group.objects.create(
            group_name='Test Group'
        )

        self.assertEqual(group.group_name, 'Test Group')

    def test_new_group_no_expense(self):
        group = models.Group.objects.create(
            group_name='Test Group'
        )

        self.assertEqual(len(group.expenses.all()), 0)


class ExpenseModelTests(TestCase):

    def test_create_expense(self):
        user = create_user()
        group = create_group(user)

        expense = models.Expense.objects.create(
            expense_name='Test Expense',
            amount=Decimal('1.00'),
            paid_by=user,
            group=group,
            date_created=date.today(),
            date_modified=date.today()
        )

        self.assertEqual(expense.expense_name, 'Test Expense')
        self.assertEqual(expense.amount, Decimal('1.00'))
        self.assertEqual(expense.paid_by, user)
        self.assertEqual(expense.group, group)


class GroupSpendingModelTests(TestCase):

    def setUp(self):
        self.group = models.Group.objects.create(group_name='Test Group')

    def test_new_group_no_spending(self):
        self.assertEqual(self.group.spending.total_spending, 0)

    def test_update_group_spending(self):
        new_total_spending = 100

        self.group.spending.total_spending = new_total_spending
        self.group.spending.save()

        self.assertEqual(self.group.spending.total_spending,
                         new_total_spending)


class SpendingBreakdownModelTests(TestCase):

    def setUp(self):
        self.group = models.Group.objects.create(group_name='Test Group')
        self.user = create_user()
        self.other_user = create_other_user()
        self.expense = models.Expense.objects.create(
            expense_name='Test Expense 1',
            amount=100,
            group=self.group,
            paid_by=self.user
        )
        self.expense.expense_members.add(self.user, self.other_user)

    def test_spending_breakdown_creation(self):
        sb = models.SpendingBreakdown.objects.create(
            user=self.user,
            group=self.group,
            total_paid=100.00,
            total_spending=50.00
        )
        self.assertEqual(sb.user, self.user)
        self.assertEqual(sb.group, self.group)
        self.assertEqual(sb.total_paid, 100.00)
        self.assertEqual(sb.total_spending, 50.00)

    def test_spending_breakdown_uniqueness(self):
        models.SpendingBreakdown.objects.create(
            user=self.user,
            group=self.group,
            total_paid=100.00,
            total_spending=50.00
        )
        with self.assertRaises(Exception):
            models.SpendingBreakdown.objects.create(
                user=self.user,
                group=self.group,
                total_paid=150.00,
                total_spending=75.00
            )

    def test_get_spending_breakdown_by_user_and_group(self):
        spending_breakdown = models.SpendingBreakdown.objects.create(
            user=self.user,
            group=self.group,
            total_paid=100.00,
            total_spending=50.00
        )
        sb_from_db = models.SpendingBreakdown.objects.get(user=self.user,
                                                          group=self.group)
        self.assertEqual(sb_from_db, spending_breakdown)

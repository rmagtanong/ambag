"""
Tests for Models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user():
    email = 'test@example.com'
    password = 'test1234'

    return get_user_model().objects.create_user(
        email=email,
        password=password
    )


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

    def test_create_group_success(self):
        group = models.Group.objects.create(
            group_name='Test Group',
        )

        self.assertEqual(group.group_name, 'Test Group')

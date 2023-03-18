"""
Database models
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('Email must not be blank')

        user = self.model(email=self.normalize_email(email), **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user

    def get_by_email(self, email):
        return self.get(email=email)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField('Group',
                                    related_name='members',
                                    blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Group(models.Model):
    group_name = models.CharField(max_length=50)
    group_members = models.ManyToManyField(User,
                                           related_name='group_memberships')


class Expense(models.Model):
    expense_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    group = models.ForeignKey(Group,
                              on_delete=models.CASCADE,
                              related_name='expenses')
    paid_by = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='expenses_paid')
    expense_members = models.ManyToManyField(User,
                                             related_name='expenses_involved')

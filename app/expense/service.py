"""
Service layer for Expense API
"""
from rest_framework import status
from rest_framework.response import Response

from core.models import User
from core.repository.user_repository import UserRepository
from core.repository.group_repository import GroupRepository
from core.repository.expense_repository import ExpenseRepository

from expense.serializers import ExpenseSerializer


def create_expense(request):

    group = get_group(request['group_id'])

    paid_by = get_user(request['paid_by'])

    expense_members = get_expense_members(request['expense_members'])

    expense = save_expense(request['expense_name'],
                           request['amount'],
                           group,
                           paid_by,
                           expense_members)

    serializer = ExpenseSerializer(expense)

    return Response(serializer.data,
                    status=status.HTTP_201_CREATED)


def get_group(group_id):
    return GroupRepository.get_group(group_id)


def get_user(email):
    try:
        user = UserRepository.get_by_email(email)
    except User.DoesNotExist:
        return Response({
            'paid_by': f'User does not exist, email={email}'},
            status=status.HTTP_400_BAD_REQUEST)

    return user


def get_expense_members(expense_member_emails):
    expense_members = []

    for email in expense_member_emails:
        user = get_user(email)
        expense_members.append(user)

    return expense_members


def save_expense(expense_name, amount, group, paid_by, expense_members):
    return ExpenseRepository.create_expense(
        expense_name=expense_name,
        amount=amount,
        group=group,
        paid_by=paid_by,
        expense_members=expense_members
    )

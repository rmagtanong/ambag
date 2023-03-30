"""
Service layer for Expense API
"""
from decimal import Decimal

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

    update_balances(group, expense)

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


def update_balances(group, expense):
    update_group_spending(group.spending, expense.amount)

    update_total_paid(group, expense)

    update_user_spending(group, expense)


def update_group_spending(group_spending, amount):
    group_spending.total_spending += Decimal(str(amount))
    group_spending.save()


def update_total_paid(group, expense):
    spending_breakdown = expense.paid_by.spending_breakdowns.get(group=group)
    spending_breakdown.total_paid += Decimal(expense.amount)
    spending_breakdown.save()


def update_user_spending(group, expense):
    expense_members = expense.expense_members.all()
    amount_per_member = split_evenly(expense.amount, expense_members)

    for user in expense_members:
        spending_breakdown = user.spending_breakdowns.get(group=group)
        spending_breakdown.total_spending += amount_per_member
        spending_breakdown.save()


def split_evenly(amount, expense_members):
    no_members = len(expense_members)
    return round(Decimal(amount)/no_members, 2)

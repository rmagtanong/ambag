"""
Validator for Expense API request data
"""
from typing import Dict, List
from decimal import Decimal

from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def validate_expense_data(data: Dict, group_id: int) -> Dict:
    validated_data = {}

    # Validate expense_name
    expense_name = data.get('expense_name')
    validated_data['expense_name'] = is_str(expense_name)

    # Validate amount
    amount = data.get('amount')
    validated_data['amount'] = is_number(amount)

    # Validate paid_by email format
    paid_by_email = data.get('paid_by')
    validated_data['paid_by'] = is_email(paid_by_email)

    # Validate expense_members data type
    expense_members_emails = data.pop('expense_members', [])
    is_list(expense_members_emails)

    # Validate expense_members number of members
    has_expense_member(expense_members_emails)

    # Validate expense_members email format
    expense_members = []
    for email in expense_members_emails:
        is_email(email)
        expense_members.append(email)
    validated_data['expense_members'] = expense_members

    # Add group_id to validated data
    validated_data['group_id'] = group_id

    return validated_data


def is_str(expense_name):
    if not isinstance(expense_name, str):
        raise ValidationError('expense_name must be a string')
    return expense_name


def is_number(amount):
    if isinstance(amount, str):
        try:
            Decimal(amount)
        except ValidationError:
            ValidationError('amount must be convertible to a number')

    if not isinstance(amount, (int, float, str)):
        raise ValidationError('amount must be a number')

    return amount


def is_email(email):
    try:
        validate_email(email)
    except ValidationError:
        raise ValidationError(f'email invalid, email={email}')

    return email


def is_list(expense_members_emails):
    if not isinstance(expense_members_emails, List):
        raise ValidationError('expense_members must be a list')


def has_expense_member(expense_members_emails):
    if len(expense_members_emails) < 1:
        raise ValidationError('expense_members should have at least 1 user')

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
    if not isinstance(expense_name, str):
        raise ValidationError('expense_name must be a string')
    validated_data['expense_name'] = expense_name

    # Validate amount
    amount = data.get('amount')
    if isinstance(amount, str):
        try:
            Decimal(amount)
        except ValidationError:
            ValidationError('amount must be convertible to a number')

    if not isinstance(amount, (int, float, str)):
        raise ValidationError('amount must be a number')
    validated_data['amount'] = amount

    # Validate paid_by email format
    paid_by_email = data.get('paid_by')
    try:
        validate_email(paid_by_email)
    except ValidationError:
        raise ValidationError(f'paid_by email invalid, email={paid_by_email}')
    validated_data['paid_by'] = paid_by_email

    # Validate expense_members data type
    expense_members_emails = data.pop('expense_members', [])
    if not isinstance(expense_members_emails, List):
        raise ValidationError('expense_members must be a list')

    # Validate expense_members number of members
    if len(expense_members_emails) < 1:
        raise ValidationError('expense_members should have at least 1 user')

    # Validate expense_members email format
    expense_members = []
    for email in expense_members_emails:
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError(f'expense_member email invalid, email={email}')
        expense_members.append(email)
    validated_data['expense_members'] = expense_members

    # Add group_id to validated data
    validated_data['group_id'] = group_id

    return validated_data

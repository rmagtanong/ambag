from datetime import date
from decimal import Decimal

from django.db.models import QuerySet

from core.models import User, Group, Expense


class ExpenseRepository:

    @staticmethod
    def create_expense(expense_name: str,
                       amount: Decimal,
                       group: Group,
                       paid_by: User,
                       expense_members: list[User]) -> Expense:

        expense = Expense.objects.create(
            expense_name=expense_name,
            amount=amount,
            group=group,
            paid_by=paid_by,
            date_created=date.today(),
            date_modified=date.today()
        )
        expense.expense_members.set(expense_members)
        return expense

    @staticmethod
    def get_group_expenses(group_id: int) -> QuerySet[Expense]:
        return Expense.objects.filter(group_id=group_id)

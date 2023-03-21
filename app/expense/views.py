"""
Views for Expense API
"""
from datetime import date

from rest_framework import viewsets
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import User, Group, Expense
from expense import serializers


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ExpenseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        return Expense.objects.filter(group=group_id)

    def create(self, request, *args, **kwargs):
        group_id = self.kwargs['group_id']
        group = Group.objects.get(pk=group_id)

        data = request.data.copy()

        paid_by_email = data.get('paid_by')
        expense_members_emails = data.pop('expense_members', [])

        try:
            paid_by = User.objects.get(email=paid_by_email)
        except User.DoesNotExist:
            return Response({
                'paid_by': f'User does not exist, email={paid_by_email}'},
                status=status.HTTP_400_BAD_REQUEST)

        expense_members = []
        for email in expense_members_emails:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({
                    'expense_members': f'User does not exist, email={email}'},
                    status=status.HTTP_400_BAD_REQUEST)

            expense_members.append(user)

        expense = Expense.objects.create(
            expense_name=data.get('expense_name'),
            amount=data.get('amount'),
            date_created=date.today(),
            date_modified=date.today(),
            group=group,
            paid_by=paid_by
        )
        expense.expense_members.set(expense_members)

        return Response(self.serializer_class(expense).data,
                        status=status.HTTP_201_CREATED)

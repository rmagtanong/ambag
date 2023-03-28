"""
Views for Expense API
"""
from rest_framework import viewsets
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import User
from core.repository.user_repository import UserRepository
from core.repository.group_repository import GroupRepository
from core.repository.expense_repository import ExpenseRepository
from expense import serializers
from expense.validators import validate_expense_data


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ExpenseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        return ExpenseRepository.get_group_expenses(group_id)

    def create(self, request, *args, **kwargs):
        group_id = self.kwargs['group_id']
        data = request.data.copy()

        try:
            validated_data = validate_expense_data(data, group_id)
        except ValueError as e:
            return Response({
                'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST)

        group = GroupRepository.get_group(validated_data['group_id'])

        paid_by_email = validated_data['paid_by']
        expense_members_emails = validated_data['expense_members']

        try:
            paid_by = UserRepository.get_by_email(paid_by_email)
        except User.DoesNotExist:
            return Response({
                'paid_by': f'User does not exist, email={paid_by_email}'},
                status=status.HTTP_400_BAD_REQUEST)

        expense_members = []
        for email in expense_members_emails:
            try:
                user = UserRepository.get_by_email(email)
            except User.DoesNotExist:
                return Response({
                    'expense_members': f'User does not exist, email={email}'},
                    status=status.HTTP_400_BAD_REQUEST)

            expense_members.append(user)

        expense = ExpenseRepository.create_expense(
            expense_name=validated_data['expense_name'],
            amount=validated_data['amount'],
            group=group,
            paid_by=paid_by,
            expense_members=expense_members
        )

        return Response(self.serializer_class(expense).data,
                        status=status.HTTP_201_CREATED)

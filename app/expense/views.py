"""
Views for Expense API
"""
from rest_framework import viewsets
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.repository.expense_repository import ExpenseRepository

from expense import serializers
from expense.service import create_expense
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

        return create_expense(validated_data)

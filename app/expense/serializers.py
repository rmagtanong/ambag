from rest_framework import serializers

from core.models import Expense, User
from core.serializers import UserDataSerializer, GroupDataSerializer, DateField


class ExpenseSerializer(serializers.ModelSerializer):
    group = GroupDataSerializer()
    paid_by = UserDataSerializer()
    expense_members = UserDataSerializer(many=True, read_only=True)
    date_created = DateField()
    date_modified = DateField()

    class Meta:
        model = Expense
        fields = [
            'id',
            'expense_name',
            'amount',
            'date_created',
            'date_modified',
            'group',
            'paid_by',
            'expense_members'
        ]
        read_only_fields = ['id']

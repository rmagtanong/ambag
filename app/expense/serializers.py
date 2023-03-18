from rest_framework import serializers

from core.models import Expense
from group.serializers import GroupMemberSerializer


class CustomDateField(serializers.DateField):
    def to_representation(self, value):
        return value.strftime('%d-%b-%Y')


class ExpenseSerializer(serializers.ModelSerializer):
    expense_members = GroupMemberSerializer(many=True, read_only=True)
    date_created = CustomDateField()
    date_modified = CustomDateField()

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

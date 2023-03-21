"""
Common data serializers
"""
from rest_framework import serializers

from core.models import User, Group


class UserDataSerializer(serializers.ModelSerializer):
    """
    Represents `User` objects as
    {
        "name": "Name",
        "email": "name@example.com"
    }
    """
    class Meta:
        model = User
        fields = ['name', 'email']


class GroupDataSerializer(serializers.ModelSerializer):
    """
    Represents `Group` objects as
    {
        "id": 1
        "name": "Group Name"
    }
    """
    class Meta:
        model = Group
        fields = ['id', 'group_name']


class DateField(serializers.DateField):
    """
    Converts `date` to YYYY-Mon-DD format
    """
    def to_representation(self, value):
        return value.strftime('%d-%b-%Y')

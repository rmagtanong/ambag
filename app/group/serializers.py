from rest_framework import serializers

from core.models import Group, User
from core.serializers import UserDataSerializer


class GroupSerializer(serializers.ModelSerializer):
    group_members = UserDataSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = [
            'id',
            'group_name',
            'group_members'
        ]
        read_only_fields = ['id']

from rest_framework import serializers

from core.models import Group, User


class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email']


class GroupSerializer(serializers.ModelSerializer):
    group_members = GroupMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = [
            'id',
            'group_name',
            'group_members'
        ]
        read_only_fields = ['id']

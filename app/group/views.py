"""
Views for Group API
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Group
from group import serializers


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.GroupSerializer
    queryset = Group.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Add `User` that created `Group` as group_member
        :param serializer:
        :return:
        """
        user = self.request.user

        group = serializer.save()
        group.group_members.add(user)
        group.save()

        user.groups.add(group)
        user.save()

    def get_queryset(self):
        """
        Filter `Groups` where `User` is a group_member
        :return:
        """
        user = self.request.user
        return user.groups.all()

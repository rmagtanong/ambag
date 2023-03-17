"""
Views for Group API
"""
from rest_framework import viewsets
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

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

    @action(detail=True, methods=['post'])
    def join(self, request, *args, **kwargs):
        user = request.user
        group_id = self.kwargs['pk']

        group = Group.objects.get(id=group_id)

        if group.group_members.filter(id=user.id).exists():
            return Response({'detail': 'User is already a member of this group.'}, status=status.HTTP_400_BAD_REQUEST)

        group.group_members.add(user)
        user.groups.add(group)

        return Response({'detail': 'User has been added to the group.'}, status=status.HTTP_200_OK)

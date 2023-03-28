"""
Service layer for Group API
"""
from rest_framework import status
from rest_framework.response import Response

from core.models import User, Group
from core.repository.group_repository import GroupRepository


def join_group(user: User,
               group_id: int):

    group = get_group(group_id)

    if is_existing_member(group, user.id):
        return Response({
            'detail': 'User is already a member of this group.'},
            status=status.HTTP_400_BAD_REQUEST)

    add_member(group, user)

    return Response({
        'detail': 'User has been added to the group.'},
        status=status.HTTP_200_OK)


def get_group(group_id):
    return GroupRepository.get_group(group_id)


def is_existing_member(group, user_id):
    return GroupRepository.is_existing_member(group, user_id)


def add_member(group, user):
    GroupRepository.add_member(group, user)

from typing import Optional

from core.models import User, Group


class GroupRepository:

    @staticmethod
    def get_group(group_id: int) -> Optional[Group]:
        try:
            return Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return None

    @staticmethod
    def is_existing_member(group: Group,
                           user_id: int) -> bool:
        return group.group_members.filter(id=user_id).exists()

    @staticmethod
    def add_member(group: Group,
                   user: User) -> None:
        group.group_members.add(user)
        user.groups.add(group)

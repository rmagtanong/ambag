from core.models import Group


class GroupRepository:

    @staticmethod
    def get_group(group_id):
        try:
            return Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return None

    @staticmethod
    def is_existing_member(group, user_id):
        return group.group_members.filter(id=user_id).exists()

    @staticmethod
    def add_member(group, user):
        group.group_members.add(user)
        user.groups.add(group)

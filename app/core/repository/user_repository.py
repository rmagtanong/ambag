from core.models import User


class UserRepository:

    @staticmethod
    def get_by_email(email):
        return User.objects.get(email=email)

from core.models import User


class UserRepository:

    @staticmethod
    def get_by_email(email) -> User:
        return User.objects.get(email=email)

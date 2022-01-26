import bcrypt

from core import my_salt
from data import User
from data.UserRepository import UserRepository


class UserService:
    _instance = None

    def __new__(cls, user_repository: UserRepository):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            cls.__init__(cls._instance, user_repository)
        return cls._instance

    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository

    def create(self, user: User) -> None:
        if type(user.password) is str:
            user.password = bcrypt.hashpw(user.password.encode(), my_salt)
        else:
            raise Exception("password must be of type string")

        self.user_repo.create(user)

    def find_by_username(self, username):
        return self.user_repo.find_by_username(username)

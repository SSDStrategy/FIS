from data import *


class UserRepository:
    def find_by_id(self, id: int) -> User:
        return session.query(User).get(id)

    def find_by_username(self, username: str) -> User:
        return session.query(User).filter_by(username=username).first()

    def create(self, user: User) -> None:
        session.begin()
        session.merge(user)
        session.commit()

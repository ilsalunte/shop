from typing import NamedTuple
from shop.user import User


class UserIdNotFound(Exception):
    pass


class UserName(NamedTuple):
    user_id: str
    email: str


class UsersHandling:
    def __init__(self):
        self._users: dict[str, User] = {}
        self._counter = 0
        self.add_user(email='admin@admin', password='adminadmin', admin=True)

    def add_user(self, email: str, password: str, admin: bool = False, history: list = []) -> str:
        user_id = str(self._counter).zfill(4)

        user = User(
            user_id=user_id,
            email=email,
            password=password,
            admin=admin,
            history=history
        )

        self._users[user_id] = user

        self._counter += 1
        return user_id

    def delete_user(self, user_id: str) -> None:
        try:
            del self._users[user_id]
        except KeyError:
            raise UserIdNotFound from None

    def change_password(self, user_id: str, new_password: str) -> None:
        try:
            self._users[user_id].password = new_password
        except KeyError:
            raise UserIdNotFound from None

    def get_single_user(self, user_id):
        try:
            return self._users[user_id]
        except KeyError:
            raise UserIdNotFound from None

    def get_users_list(self):
        return [
            UserName(user_id=item.user_id, email=item.email)
            for item in self._users.values()
        ]


if __name__ == '__main__':
    test = UsersHandling()
    print(test.get_single_user('0000'))

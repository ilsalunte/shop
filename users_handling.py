from typing import Optional

from user import User, UserWithoutPassword, HistoryItem


class UserIdNotFound(Exception):
    pass


class WrongCredential(Exception):
    pass


class UsersHandling:
    def __init__(self):
        self._users: dict[str, User] = {}
        self._counter = 0
        self.add_user(email='admin@admin', password='adminadmin', is_admin=True)
        self.add_user(email='user@user', password='useruser')

    def add_user(self, email: str, password: str, is_admin: bool = False, history: Optional[list[HistoryItem]] = None) -> str:

        user = User(
            email=email,
            password=password,
            is_admin=is_admin,
            history=history or []
        )
        self._users[email] = user

        return email

    def delete_user(self, email: str) -> None:
        try:
            del self._users[email]
        except KeyError:
            raise UserIdNotFound from None

    def change_password(self, email: str, new_password: str) -> None:
        try:
            self._users[email].password = new_password
        except KeyError:
            raise UserIdNotFound from None

    def get_user(self, email: str) -> UserWithoutPassword:
        try:
            return self._users[email].get_user_without_password()
        except KeyError:
            raise UserIdNotFound from None

    def get_users_list(self) -> list[UserWithoutPassword]:
        return [
            item.get_user_without_password() for item in self._users.values()
        ]

    def login(self, email: str, password: str) -> None:
        if email not in self._users:
            raise WrongCredential('Podano nieprawidłowe dane logowania.')
        if not password == self._users[email].password:
            raise WrongCredential('Podano nieprawidłowe dane logowania.')

    def add_to_history(self, email: str, item: HistoryItem) -> None:
        try:
            return self._users[email].history.append(item)
        except KeyError:
            raise UserIdNotFound from None


if __name__ == '__main__':
    test = UsersHandling()
    lista = test.get_users_list()
    print(test.get_users_list())

from user import User, UserWithoutPassword


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

    def add_user(self, email: str, password: str, is_admin: bool = False, history: list = None) -> str:

        user = User(
            email=email,
            password=password,
            is_admin=is_admin,
            history=history
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

    def get_single_user(self, email) -> UserWithoutPassword:
        try:
            return self._users[email].get_user_without_password()
        except KeyError:
            raise UserIdNotFound from None

    def get_users_list(self) -> list[str]: # todo do poprawy
        return [
            item for item in self._users()
        ]

    def login(self, email, password) -> None:
        if email not in self._users:
            raise WrongCredential()
        if not password == self._users[email].password:
            raise WrongCredential()


if __name__ == '__main__':
    test = UsersHandling()
    print(test.get_single_user('0001'))


pass
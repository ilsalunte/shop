class UserWithoutPassword:
    def __init__(self, email: str, history: list, is_admin: bool):
        self.email = email
        self.history = history
        self.is_admin = is_admin

    def __repr__(self) -> str:
        return f'<{self.email}:{self.is_admin}>'


class User(UserWithoutPassword):
    def __init__(self, password: str, **kwargs):
        super().__init__(**kwargs)
        self.password = password

    def get_user_without_password(self) -> UserWithoutPassword:
        return UserWithoutPassword(email=self.email, history=self.history, is_admin=self.is_admin)

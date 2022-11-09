class User:
    def __init__(self, user_id: str, email: str, password: str, history: list, admin: bool):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.history = history
        self.admin = admin

    def __repr__(self) -> str:
        return f'<{self.user_id}:{self.email}:{self.password}:{self.admin}>'



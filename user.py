class User:
    def __init__(self, user_id, user_email, user_password, history, admin):
        self.user_id = user_id
        self.user_email = user_email
        self.user_password = user_password
        self.history = history
        self.admin = admin


USERS = {'admin@admin': User(1, 'admin@admin', 'adminadmin', [], True)}





class User:
    def __init__(self, user_id: int, username: str, email: str, password_hash: str, created_at: str = None):
        self._user_id = user_id
        self._username = username
        self._email = email
        self._password_hash = password_hash
        self._created_at = created_at

    # Properties (getters)
    @property
    def user_id(self):
        return self._user_id

    @property
    def username(self):
        return self._username

    @property
    def email(self):
        return self._email

    @property
    def password_hash(self):
        return self._password_hash

    @property
    def created_at(self):
        return self._created_at

    # Setters
    @username.setter
    def username(self, value):
        self._username = value

    @email.setter
    def email(self, value):
        self._email = value

    @password_hash.setter
    def password_hash(self, value):
        self._password_hash = value

    def __str__(self):
        return f"User(user_id={self._user_id}, username={self._username}, email={self._email}, created_at={self._created_at})"
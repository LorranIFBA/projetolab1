import mysql.connector
from Model.user import User

class UserDAO:
    def __init__(self):
        # Open database connection
        self.__connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="lab12"
        )
        self.__cursor = self.__connection.cursor()

    # Create
    def create_user(self, user: User):
        query = "INSERT INTO Users (username, email, password_hash) VALUES (%s, %s, %s)"
        values = (user.username, user.email, user.password_hash)
        self.__cursor.execute(query, values)
        self.__connection.commit()

    # Read
    def get_user_by_id(self, user_id: int) -> User:
        query = "SELECT user_id, username, email, password_hash, created_at FROM Users WHERE user_id = %s"
        self.__cursor.execute(query, (user_id,))
        result = self.__cursor.fetchone()
        if result:
            return User(result[0], result[1], result[2], result[3], result[4])
        return None

    def get_all_users(self) -> list[User]:
        query = "SELECT user_id, username, email, password_hash, created_at FROM Users"
        self.__cursor.execute(query)
        results = self.__cursor.fetchall()
        users = []
        for result in results:
            users.append(User(result[0], result[1], result[2], result[3], result[4]))
        return users

    # Update
    def update_user(self, user: User):
        query = "UPDATE Users SET username = %s, email = %s, password_hash = %s WHERE user_id = %s"
        values = (user.username, user.email, user.password_hash, user.user_id)
        self.__cursor.execute(query, values)
        self.__connection.commit()

    # Delete
    def delete_user(self, user_id: int):
        query = "DELETE FROM Users WHERE user_id = %s"
        self.__cursor.execute(query, (user_id,))
        self.__connection.commit()

    # Close database connection
    def close(self):
        if self.__cursor:
            self.__cursor.close()
        if self.__connection:
            self.__connection.close()

    # Context management (with block support)
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
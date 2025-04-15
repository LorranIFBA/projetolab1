import mysql.connector


class DatabaseManager:
    def __init__(self):
        # Open database connection
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="lab12"
        )
        self.cursor = self.connection.cursor()
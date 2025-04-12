from Model.user import User
from Model.userDAO import UserDAO


from Model.user import User
from Model.userDAO import UserDAO

class UserController:
    def __init__(self):
        pass

    # Create
    def add_user(self, user_id: int, username: str, email: str, password_hash: str):
        with UserDAO() as user_dao:
            user = User(user_id, username, email, password_hash)
            user_dao.create_user(user)

    # Read
    def get_user(self, user_id: int) -> 'User':
        with UserDAO() as user_dao:
            return user_dao.get_user_by_id(user_id)

    def get_all_users(self) -> list['User']:
        with UserDAO() as user_dao:
            return user_dao.get_all_users()

    # Update
    def update_user(self, user_id: int, username: str = None, email: str = None, password_hash: str = None):
        with UserDAO() as user_dao:
            user = user_dao.get_user_by_id(user_id)
            if not user:
                raise ValueError("User not found.")

            if username:
                user.username = username  # Use property, not setter method
            if email:
                user.email = email  # Use property, not setter method
            if password_hash:
                user.password_hash = password_hash  # Use property, not setter method

            user_dao.update_user(user)

    # Delete
    def delete_user(self, user_id: int):
        with UserDAO() as user_dao:
            user_dao.delete_user(user_id)





"""
# Create a controller instance
user_controller = UserController()

# Test CREATE operation
print("Testing CREATE operation...")
try:
    user_controller.add_user(1, "john_doe", "john@example.com", "hashed_password")
    print("User created successfully!")
except Exception as e:
    print(f"Error creating user: {e}")

# Test READ operation (get_user_by_id)
print("\nTesting READ operation (get_user_by_id)...")
try:
    user = user_controller.get_user(1)
    if user:
        print(f"User found: ID={user.user_id}, Username={user.username}, Email={user.email}")
    else:
        print("User not found.")
except Exception as e:
    print(f"Error retrieving user: {e}")

# Test READ operation (get_all_users)
print("\nTesting READ operation (get_all_users)...")
try:
    all_users = user_controller.get_all_users()
    if all_users:
        print("All users:")
        for u in all_users:
            print(f"ID={u.user_id}, Username={u.username}, Email={u.email}")
    else:
        print("No users found.")
except Exception as e:
    print(f"Error retrieving all users: {e}")

# Test UPDATE operation
print("\nTesting UPDATE operation...")
try:
    user_controller.update_user(1, username="jane_doe", email="jane@example.com")
    print("User updated successfully!")
except Exception as e:
    print(f"Error updating user: {e}")

# Verify the update
print("\nVerifying UPDATE operation...")
try:
    updated_user = user_controller.get_user(1)
    if updated_user:
        print(f"Updated user: ID={updated_user.user_id}, Username={updated_user.username}, Email={updated_user.email}")
    else:
        print("User not found after update.")
except Exception as e:
    print(f"Error retrieving updated user: {e}")

# Test DELETE operation
print("\nTesting DELETE operation...")
try:
    user_controller.delete_user(1)
    print("User deleted successfully!")
except Exception as e:
    print(f"Error deleting user: {e}")

# Verify the deletion
print("\nVerifying DELETE operation...")
try:
    deleted_user = user_controller.get_user(1)
    if deleted_user:
        print("User still exists after deletion.")
    else:
        print("User successfully deleted.")
except Exception as e:
    print(f"Error verifying deletion: {e}")"""
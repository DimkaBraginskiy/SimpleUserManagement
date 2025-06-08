import json

from user import User
import re
import os

class UserService:

    def __init__(self, filename="data.json"):
        self.filename = filename
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                try:
                    data = json.load(f)
                    return {u["username"]: User(**u) for u in data}
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from {self.filename}. Starting with an empty user list.")
                    return {}
        return {}

    def create_user(self, username, name, email, phone, age):

        user = User(username, name, email, phone, age)
        self.users[username] = user
        self.save_users()

        return True, "User created successfully."


    def save_users(self):
        with open(self.filename, "w") as f:
            json.dump([user.__dict__ for user in self.users.values()], f, indent=4)


    def view_user(self):
        username = input("Enter username to view: ").strip()

        if username not in self.users:
            print(f"User '{username}' not found.")
            return

        user = self.users[username]
        print(f"\nUser Details:\n"
              f"Username: {user.username}\n"
              f"Name: {user.name}\n"
              f"Email: {user.email}\n"
              f"Phone: {user.phone}\n"
              f"Age: {user.age}\n")

    def view_all_users(self):
        if not self.users:
            print("No users found.")
            return

        print("\nAll Users:")
        for user in self.users.values():
            print(f"Username: {user.username}, Name: {user.name}, Email: {user.email}, Phone: {user.phone}, Age: {user.age}")


    def update_user(self):
        username = input("Enter username to update: ").strip()
        if username == "/cancel":
            print("Operation cancelled.")
            return

        if username not in self.users:
            print(f"User '{username}' not found.")
            return

        user = self.users[username]
        print(f"\nUpdating user '{username}'. Leave field blank to keep current value.\n")


        new_username = input(f"Enter new username [{user.username}]: ").strip()
        if new_username and new_username != username:
            if new_username in self.users:
                print(f"Username '{new_username}' already exists.")
                return
            if not new_username.strip():
                print("Username cannot be empty.")
                return
            # Perform the key update
            self.users[new_username] = user
            del self.users[username]
            user.username = new_username
            username = new_username


        # Prompt each field, allowing skipping with Enter
        new_name = input(f"Enter new name [{user.name}]: ").strip()
        if new_name:
            while not new_name:
                print("Name cannot be empty.")
                new_name = input(f"Enter new name [{user.name}]: ").strip()
            user.name = new_name

        new_email = input(f"Enter new email [{user.email}]: ").strip()
        if new_email:
            while not self.is_valid_email(new_email):
                print("Invalid email format.")
                new_email = input(f"Enter new email [{user.email}]: ").strip()
            user.email = new_email

        new_phone = input(f"Enter new phone [{user.phone}]: ").strip()
        if new_phone:
            while not self.is_valid_phone(new_phone):
                print("Invalid phone format. Use +12345678901")
                new_phone = input(f"Enter new phone [{user.phone}]: ").strip()
            user.phone = new_phone

        new_age = input(f"Enter new age [{user.age}]: ").strip()
        if new_age:
            while not (new_age.isdigit() and int(new_age) > 0):
                print("Age must be a positive integer.")
                new_age = input(f"Enter new age [{user.age}]: ").strip()
            user.age = int(new_age)

        self.users[username] = user
        self.save_users()
        print("User updated successfully.")


    def delete_user(self):
        username = input("Enter username to delete: ").strip()

        if username not in self.users:
            print(f"User '{username}' not found.")
            return

        del self.users[username]
        self.save_users()
        print(f"User '{username}' deleted successfully.")



    def is_valid_email(self, email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

    def is_valid_phone(self, phone):
        phone_regex = r'^\+\d{7,15}$'
        return re.match(phone_regex, phone) is not None

    def is_valid_name(self, name):
        return name.strip() != "" and not name in self.users



    def prompt_valid_username(self):
        while True:
            username = input("Enter username ( /cancel to cancel the operation): ").strip()
            if username == "/cancel":
                print("Operation cancelled.")
                return None

            if not username:
                print("Username cannot be empty.")
            elif username in self.users:
                print(f"Username '{username}' already exists. Please choose a different one.")
            else:
                return username


    def prompt_valid_name(self):
        while True:
            name = input("Enter name ( /cancel to cancel the operation): ").strip()
            if name == "/cancel":
                print("Operation cancelled.")
                return None

            if name:
                return name
            print("Name cannot be empty.")

    def prompt_valid_email(self):
        while True:
            email = input("Enter email( /cancel to cancel the operation): ").strip()
            if email == "/cancel":
                print("Operation cancelled.")
                return None

            if self.is_valid_email(email):
                return email
            print("Invalid email format.")

    def prompt_valid_phone(self):
        while True:
            phone = input("Enter phone number( /cancel to cancel the operation): ").strip()
            if phone == "/cancel":
                print("Operation cancelled.")
                return None

            if self.is_valid_phone(phone):
                return phone
            print("Invalid phone format.")

    def prompt_valid_age(self):
        while True:
            age = input("Enter age( /cancel to cancel the operation): ").strip()
            if age == "/cancel":
                print("Operation cancelled.")
                return None

            if age.isdigit() and int(age) > 0:
                return age
            print("Invalid age. Must be a positive integer.")
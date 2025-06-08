from userService import UserService


def init():

    userService = UserService()

    while True:
        userinput = input("--- User CRUD Menu ---\n"
                            "1. Create User\n"
                            "2. View User\n"
                            "3. Update User\n"
                            "4. Delete User\n"  
                            "5. Show All Users\n"
                            "0. Exit\n"
                          "Your input: ")

        match userinput:
            case '1':

                username = userService.prompt_valid_username()
                if abort_if_cancelled(username): continue

                name = userService.prompt_valid_name()
                if abort_if_cancelled(name): continue

                email = userService.prompt_valid_email()
                if abort_if_cancelled(email): continue

                phone = userService.prompt_valid_phone()
                if abort_if_cancelled(phone): continue

                age = userService.prompt_valid_age()
                if abort_if_cancelled(age): continue

                success, message = userService.create_user(username, name, email, phone, age)
                print(message)
                print("-" * 50)

            case '2':
                userService.view_user()
                print("-" * 50)
            case '3':
                userService.update_user()
                print("-" * 50)
            case '4':
                userService.delete_user()
                print("-" * 50)
            case '5':
                userService.view_all_users()
                print("-" * 50)
            case '0':
                print("Exiting User Management System. Goodbye!")
                print("-" * 50)
                break
            case _:
                print("Invalid input, please try again.")
                print("-" * 50)

def abort_if_cancelled(value, message="User creation cancelled."):
    if value is None:
        print(message + "\n" + "-" * 50)
        return True
    return False



if __name__ == "__main__":
    init()
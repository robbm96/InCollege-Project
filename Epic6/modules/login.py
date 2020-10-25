import json
import time


LOGGED_IN_USER = {}
# def verify_login(username, password, database="database.json"):
#     with open(database) as db:
#         data = json.load(db)
#         # Checks if there is a matching username and password in database
#         for user in data["users"]:
#             if user["username"] == username and user["password"] == password:
#                 print("You have successfully logged in")
#                 time.sleep(2)
#                 return True
#         print("Incorrect username/password. Try again")
#         return False


def login(username, password, database="database.json"):
    is_logged_in = False
    # while not is_logged_in:
    with open(database) as db:
        data = json.load(db)
        # Checks if there is a matching username and password in database
        for user in data["users"]:
            if user["username"] == username and user["password"] == password:
                print("You have successfully logged in")
                time.sleep(2)
                is_logged_in = True
                break
        if is_logged_in:
            LOGGED_IN_USER["username"] = username
            return True
        else:
            print("Incorrect username/password. Try again")
            return False
        # username = input("Please enter a username: ")
        # password = input("Please enter a password: ")
        # is_logged_in = verify_login(username, password)           
    return True

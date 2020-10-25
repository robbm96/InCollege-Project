import json
import time


def verify_first(first_name, database):
    with open(database) as db:
        data = json.load(db)
        # verfies last_name isnt someone elses
        for user in data["users"]:
            if user["first_name"] == first_name:
                return False
        db.close()
        return True


def verify_last(last_name, database):
    with open(database) as db:
        data = json.load(db)
        # verfies last_name isnt someone elses
        for user in data["users"]:
            if user["last_name"] == last_name:
                return False
        db.close()
        return True


def verify_password(password):
    accept_min = len(password) >= 8  # Checks if password length is at least 8
    # checks if password length doesnt exceed 12
    accept_max = len(password) <= 12
    # checks if password has a capital letter
    has_capital = any(char for char in password if char.isupper())
    # checks if password has a digit
    has_digit = any(char for char in password if char.isdigit())
    has_non_alpha = any(char for char in password if not char.isalnum(
    ) and not char.isspace())  # checks if password has a special character

    # return true if all the above conditions are satisfied. False if not
    return all([accept_min, accept_max, has_capital, has_digit, has_non_alpha])


def verify_username(username, database="database.json"):
    if len(username) == 0 or any(char for char in username if char.isspace()):
        return False
    with open(database) as db:
        data = json.load(db)
        # verfies username isnt someone elses
        for user in data["users"]:
            if user["username"] == username:
                return False
        db.close()
        return True


def verify_register(username, password, first_name, last_name, database="database.json"):
    # validate both password and username
    is_secure_password = verify_password(password)
    is_unique_username = verify_username(username, database)
    is_unique_last = verify_last(last_name, database)
    is_unique_first = verify_first(first_name, database)

    if all([is_secure_password, is_unique_first, is_unique_last, is_unique_username]):
        # get existing data
        with open(database) as db:
            data = json.load(db)
            db.close()

        with open(database, 'w+') as db:
            new_user = {
                "username": username,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "posted_jobs": [],
                "applied_jobs": [],
                "saved_jobs": [],
                # Added settings to be verified with Tahir
                "settings":
                    {
                        # int type possible? And in db?
                        "email": True,
                        "sms": True,
                        "targeted_ads": True,
                        "language": "English"
                }
            }

            # add new user to database
            data["users"].append(new_user)
            json.dump(data, db)
            db.close()
            print("You have successfully registered your account")
            time.sleep(2)
            return True
    else:
        print("Unable to register. Try again")
        return False


def register(database="database.json"):
    is_registered = False
    # Check if database has maximum number of users
    with open(database) as db:
        data = json.load(db)
        if len(data["users"]) == 10:
            print("All permitted accounts have been created, please come back later")
            db.close()
            return False
    while not is_registered:
        first_name = input("Please enter your first name: ")
        last_name = input("Please enter your last name: ")
        username = input("Please enter a username: ")
        password = input(
            "Please enter a password. Passwords must contain a minimum of 8 characters, maximum 12, one capital letter, one digit and one non-alpha character: ")
        is_registered = verify_register(
            username, password, first_name, last_name)
    return True

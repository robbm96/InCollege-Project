import time
import json
from modules.login import *


def get_user_option(limit1, limit2):
    while True:
        try:
            option1 = int(
                input(f"Please enter your option ({limit1}-{limit2}): "))
            return option1
        except ValueError:
            print("Input has to be an integer")


def print_privacy_policy(settings):
    setEmail = "Enabled" if settings["email"] else "Disabled"
    setSms = "Enabled" if settings["sms"] else "Disabled"
    setAd = "Enabled" if settings["targeted_ads"] else "Disabled"
    setLang = settings["language"]

    links = f"""
    --Guest Controls--
    1.) Email: {setEmail}
    2.) SMS: {setSms}
    3.) Targeted Advertising: {setAd}
    4.) Language: {setLang}
    5.) Go back

    """
    print(links)


def important_links(database="database.json"):
    links = """
    --Available Options--
    1.) Copyright Notice
    2.) About
    3.) Accessibility
    4.) User Agreement
    5.) Privacy Policy
    6.) Cookie Policy
    7.) Copyright Policy
    8.) Brand policy
    9.) Go back

    """
    print(links)


def toggle_privacy(username, database="database.json"):
    with open(database, "r") as db:
        data = json.load(db)

    with open(database, "w+") as db:
        count = 0
        for user in data["users"]:
            if user["username"] == username:
                while True:
                    print_privacy_policy(user["settings"])
                    time.sleep(2)
                    print("Which option do you want to toggle?")
                    print(
                        "Toggling language will set English to Spanish and vice versa")
                    choice = get_user_option(1, 5)
                    if choice == 1:
                        data["users"][count]["settings"]["email"] = not user["settings"]["email"]
                    elif choice == 2:
                        data["users"][count]["settings"]["sms"] = not user["settings"]["sms"]
                    elif choice == 3:
                        data["users"][count]["settings"]["targeted_ads"] = not user["settings"]["targeted_ads"]
                    elif choice == 4:
                        data["users"][count]["settings"]["language"] = "English" if user["settings"]["language"] == "Spanish" else "Spanish"
                    else:
                        break
                    print("Setting saved")
                    time.sleep(1)
            count = count + 1
        json.dump(data, db)
        db.close()
        return True


def process_important_link(choice):
    message_1 = """
    inCollege
    (c)2069, Team Oregon
    All rights reserved
    """
    message_2 = """
    inCollege is an application made by Team Oregon
    """
    message_3 = f"Accessibility is updating"
    message_4 = f"User agreement is updating"
    message_6 = f"Cookie Policy is updating..."
    message_7 = f"Copyright Policy is updating..."
    message_8 = f"Brand policy is updating..."

    if choice == 1:
        print(message_1)
    elif choice == 2:
        print(message_2)
    elif choice == 3:
        print(message_3)
    elif choice == 4:
        print(message_4)
    elif choice == 5:
        if not LOGGED_IN_USER.get("username", None):
            print("You have to be logged in to see this content")
            time.sleep(2)
            return True
        success = toggle_privacy(LOGGED_IN_USER["username"])
    elif choice == 6:
        print(message_6)
    elif choice == 7:
        print(message_7)
    elif choice == 8:
        print(message_8)
    elif choice == 9:
        return False
    time.sleep(1)
    return True

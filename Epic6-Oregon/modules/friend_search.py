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


def search_for_friend(database="database.json"):
    friend = str(
        input("Search for people you know by last name, university, or thier major: "))
    people_found = []
    found_friend = False

    # Search db for friend by last name, university, or major
    with open(database) as db:
        data = json.load(db)
        for user in data["users"]:
            if user["username"] == LOGGED_IN_USER["username"]:
                continue
            if user["last_name"] == friend or user["posted_title"]["major"] == friend or user["posted_title"]["university"] == friend:
                people_found.append(user["username"])
                found_friend = True
        db.close()

    if found_friend:
        i = 1
        print("We found " + str(len(people_found)) +
              " person(s) that matched your search. Please select your friend:")
        print("0. Exit")
        # Print all people with matching results
        for name in people_found:
            print(str(i) + ". " + str(name))
            i += 1
        # Let user select friend to add and make pending request for friend
        selection = get_user_option(0, len(people_found))
        if selection == 0:  # If they select exit
            return False
        else:  # If selected a person to add
            selection -= 1
            request_friend(people_found[selection], LOGGED_IN_USER["username"])
            print("You have successfully sent " +
                  str(people_found[selection]) + " a friend request.")
            return True
    else:
        print("Sorry we couldn't find your friend")
        return False


# let a user make a friend request to another user
def request_friend(requested_user, original_user, database="database.json"):
    with open(database) as db:
        data = json.load(db)
    with open(database, 'w+') as db:
        for user in data["users"]:
            if user["username"] == requested_user:
                # If requested_user has no friends create empty array of friends
                if "friends" not in user:
                    user["friends"] = []
                # If user has no pending_requests document create one and add the request
                if "pending_requests" not in user:
                    user["pending_requests"] = [original_user]
                else:  # else add the new request into the list
                    user["pending_requests"].append(original_user)
        json.dump(data, db)
        db.close()


# This function will show a user all their freind requests upon login
def show_requests(database="database.json"):
    with open(database) as db:
        data = json.load(db)
        for user in data["users"]:
            if user["username"] == LOGGED_IN_USER["username"]:
                # If user has no friend requests
                if "pending_requests" not in user or len(user["pending_requests"]) == 0:
                    db.close()
                    return False
                else:  # If user has at least one pending_requests allow user to accept or decline them
                    num_requests = len(user["pending_requests"])
                    break
        db.close()
        print("\nYou have " + str(num_requests) + " new friend request(s)! Would you like to view them?\nEnter 0 for \"Yes\" or 1 for \"No\"")
        view = get_user_option(0, 1)
        if view == 0:  # If they want to accept/decline requests
            edit_requests()  
        return True


# Allows users to accept or decline friend requests
def edit_requests(database="database.json"):
    with open(database) as db:
        data = json.load(db)
    with open(database, 'w+') as db:
        for user in data["users"]:
            if user["username"] == LOGGED_IN_USER["username"]:
                i = 1
                for person in user["pending_requests"]: # go through the list of requests
                    print(str(i) + ". " + str(person) + "\nEnter 0 to Accept or 1 to Decline")
                    action = get_user_option(0, 1)
                    if action == 1: # If decline
                        user["pending_requests"].remove(person) # delete request
                        json.dump(data, db)
                        db.close()
                    else: # If accept
                        user["friends"].append(person) # Add user to list of friends
                        user["pending_requests"].remove(person) # can remove the request since it is now handled
                        json.dump(data, db)
                        db.close()
                        mutual_friend(person) # Let other user add logged in user as a friend

# Creates a mutual friendship between the logged in user and the user who requested a friendship
def mutual_friend(person, database="database.json"):
    with open(database) as db:
        data = json.load(db)
    with open(database, 'w+') as db:
        for user in data["users"]:
            if user["username"] == person: # if is the user who requested friendship
                if "friends" not in user: # if they don't have a list of friends yet
                    user["friends"] = []
                    user["friends"].append(LOGGED_IN_USER["username"]) # add the logged in user as a friend to their list
                else:
                    user["friends"].append(LOGGED_IN_USER["username"])
                break
        json.dump(data, db)
        db.close()

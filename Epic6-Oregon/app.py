# This file contains all the functions and code to run our application
# Refer to test_app file for pytest methods

# import json
# import time
from modules.find import *
from modules.login import *
from modules.register import *
from modules.skills import *
from modules.welcome import *
from modules.jobs import *
from modules.useful_links import *
from modules.importantLinks import *
from modules.profile import *
from modules.profile_view import *
from modules.friend_search import *
from modules.jobs2 import *


def get_user_option(limit1, limit2):
    while True:
        try:
            option1 = int(
                input(f"Please enter your option ({limit1}-{limit2}): "))
            return option1
        except ValueError:
            print("Input has to be an integer")


if __name__ == "__main__":
    string = upper_case('computer science')
    print(string)
    while True:
        print_welcome()
        option = get_user_option(1, 5)
        while option < 1 or option > 5:
            print("Invalid input. Try again")
            option = get_user_option(1, 5)
        if option == 1:  # Login
            if LOGGED_IN_USER.get("username", None):
                break
            username = input("Please enter a username: ")
            password = input("Please enter a password: ")
            logged_in = login(username, password)
            if logged_in:
                # Show pending friend requests and allow user to accept or decline them
                has_requests = show_requests()
                break
            else:
                continue
        elif option == 2:  # Create new account
            registered = register()
            if not registered:
                exit()
            else:
                continue
        elif option == 3:
            print_useful_links()
            continue
        elif option == 4:
            while True:
                important_links()
                option = get_user_option(1, 9)
                process = process_important_link(option)
                if not process:
                    break
        elif option == 5:  # Watch Video
            print("Video is now playing for the next 5 seconds")
            time.sleep(5)
            continue

    while True:
        print_welcome2()
        option = get_user_option(1, 10)
        while option < 1 or option > 10:
            print("Invalid input. Try again")
            option = get_user_option(1, 10)

        if option == 1:  # Post Job
            print("Posting Job")
            title = input(
                "Please enter the title of the job you are posting: ")
            description = input(
                "Please enter the description of the job you are posting: ")
            employer = input(
                "Please enter the name of the employer for this job: ")
            location = input("Please enter the location of this job: ")
            salary = input("Please enter the salary of this job: ")

            job_posted = post_job(title, description,
                                  employer, location, salary, 'database.json')
            continue
        elif option == 2:  # Search for a job
            while True:
                jobs = get_all_jobs()
                print_all_jobs(jobs)
                option = job_options()
                while not validate_job_option(option):
                    option = job_options()

                if option == 'x':
                    print("Going back to main menu")
                    break
                user_choice = get_user_option(1, len(jobs))
                while user_choice < 1 or user_choice > len(jobs):
                    print("Invalid input. Try again")
                    user_choice = get_user_option(1, len(jobs))

                processed_option = process_option(
                    option, jobs[user_choice - 1])
                print("")
                if not processed_option[0]:
                    if processed_option[1] == 'x':
                        print("Going back to main menu")
                    elif processed_option[1] != 'a':
                        print("An error occurred. Going back to main menu")
                        break
                time.sleep(2)
            time.sleep(2)
            continue

        elif option == 3:  # Find user
            first_name = input(
                "Enter the first name of the user you want to find: ")
            last_name = input(
                "Enter the last name of the user you want to find: ")
            userFound = find_user(first_name, last_name, 'database.json')
            if userFound:
                print('1.) Login and contact your friends')
                print('2.) Sign up and join your friends')
                print('Enter 0 to go back to main menu')
                option = int(input("Enter your option: "))
                if option == 0:
                    continue
                elif option == 1:
                    username = input("Please enter a username: ")
                    password = input("Please enter a password: ")
                    logged_in = login(username, password)
                    if logged_in:
                        continue
                elif option == 2:
                    registered = register()
                    if not registered:
                        exit()
                    else:
                        continue
        elif option == 4:  # Learn skill
            option = list_of_skills()
            while option[0] < 1 or option[0] > 6:
                print("Invalid input. Try again")
                option = list_of_skills()
            if option[0] <= 5:
                print("Under Construction")
                time.sleep(1)
            else:
                time.sleep(1)
                continue
        elif option == 5:
            print_useful_links()
        elif option == 6:
            while True:
                important_links()
                option = get_user_option(1, 9)
                process = process_important_link(option)
                if not process:
                    break
        # The following is for Epic 4.
        elif option == 7:
            while True:
                profile_options = """
                --Profiles--
                1.) View profile
                2.) Create profile
                3.) Go back
                """
                print(profile_options)
                option = get_user_option(1, 3)
                # option to view profile or create
                while option < 1 or option > 3:
                    print("Invalid selection")
                    option = get_user_option(1, 3)
                if option == 1:
                    view_profile()
                elif option == 2:
                    profile()
                    continue
                elif option == 3:
                    break
        elif option == 8:
            result = search_for_friend()
        elif option == 9:
            str = ""
            print("You have already connected with:")
            with open('database.json') as db:
                data = json.load(db)
                for user in data["users"]:
                    if user["username"] == LOGGED_IN_USER["username"]:
                        str = LOGGED_IN_USER["username"]
                        print('\n'.join(user["friends"]), )

                    yes_no = prompt(
                        "Would you like to disconnect from any of your friends?(y/n): ")
                    if yes_no == True:
                        deleted_friend = input(
                            "Enter the name of the friend you want to delete from the list above: ")
                        if deleted_friend in user["friends"]:
                            user["friends"].remove(deleted_friend)
                            print(deleted_friend, "was deleted")

                            with open('database.json', 'w+') as db:
                                json.dump(data, db)
                            for user in data["users"]:
                                if user["username"] == deleted_friend:
                                    user["friends"].remove(str)
                                    with open('database.json', 'w+') as db:
                                        json.dump(data, db)
                        else:
                            print(
                                "The username you entered is not part of your friends.")
                    else:
                        print("Going back to the main menu.")
                        break
        elif option == 10:  # Logout
            exit()

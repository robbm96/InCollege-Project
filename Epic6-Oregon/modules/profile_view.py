import json
import array
import time
from modules.login import LOGGED_IN_USER


def get_user_option(limit1, limit2):
    while True:
        try:
            option1 = int(
                input(f"Please enter your option ({limit1}-{limit2}): "))
            return option1
        except ValueError:
            print("Input has to be an integer")


# This function is solely for displaying the profile that suits the username given to it
def display_user(user_name, database='database.json'):
    with open(database, 'r') as db:
        data = json.load(db)
        temp = data
        db.close()

    for user in data["users"]:
        if user_name == user["username"]:
            out_name = user["first_name"] + " " + user["last_name"]
            # out_name = user["first_name"], " ", user["last_name"]
            # at least 1 of them should work to put the full name to out_name
            arr_friend = user["friends"]
            # Get friend list to arr_friend array
            out_title = user["posted_title"]["title"]
            out_major = user["posted_title"]["major"]
            out_university = user["posted_title"]["university"]
            out_about = user["posted_title"]["about"]
            edu_school = ""
            edu_degree = ""
            edu_year = ""
            count_exp = 0
            for edu in user["posted_title"]["education"]:
                edu_school = edu["school"]
                edu_degree = edu["degree"]
                edu_year = edu["years_att"]

                output = f"""
                --Profile--
                Name: {out_name}
                {out_title}
                Major: {out_major}
                University: {out_university} 
                
                About: {out_about}
                
                --Education--
                School: {edu_school}
                Degree: {edu_degree}
                Year attended: {edu_year}
                
                --Experience-- """
                print(output)

                # This block prints experience if there's any
                if not user["posted_title"]["experience"]:
                    print("No past experience")
                else:
                    for exp in user["posted_title"]["experience"]:
                        count_exp += 1
                        exp_title = exp["title"]
                        exp_emp = exp["employer"]
                        exp_start = exp["date_started"]
                        exp_end = exp["date_ended"]
                        exp_loc = exp["location"]
                        exp_des = exp["description"]
                        out_exp = f"""
                Job {count_exp}:
                    Title: {exp_title}
                    Employer: {exp_emp}
                    Start date: {exp_start}
                    End date: {exp_end}
                    Location: {exp_loc}
                    Description: {exp_des}
                        """
                        print(out_exp)

            # Below to print friend list
            if user_name != LOGGED_IN_USER["username"]:
                return 0
            # If the profile displaying is not the current logged in user then dont display friend list
            if not arr_friend:
                print("No friends")
                return
            # If arr_friend is empty => user has no friend
            else:
                # Execute when the user is displaying their own profile and has friends
                print("""
                --Friends--""")
                count = 0
                for friend in arr_friend:
                    # Go through the arr_friend array by each element
                    for user_friend in temp["users"]:
                        # Go through each username in the database again
                        if user_friend["username"] == friend:
                            # Compare if the username in
                            count += 1
                            tmp = user_friend["first_name"] + \
                                " " + user_friend["last_name"]
                            print(f"""
                {count}.) {tmp}
                            """)
                return count
            # Return "friend's ID" for the chosen one in view_profile()


# Displaying options after displaying profile
def friend_option():
    option = """
    --Profile options--
    1.) View friend's profile: 
    2.) Go back
    """

    print(option)


# The main one that processes everything
def view_profile(database='database.json'):
    with open(database, 'r') as db:
        data = json.load(db)
        db.close()

    if not LOGGED_IN_USER.get("username", None):
        print("You have to be logged in to see this content")
        time.sleep(2)
        return True
    # Verify if user is logged in or not

    friend_id = display_user(LOGGED_IN_USER["username"])
    # Calls the function to display the profile and also get number of friends
    if friend_id == 0:
        conf = input("Enter anything to go back:")
        return True
    # Get any input from user and go back if no friends #relatable #sedlyfe
    while True:
        friend_option()
        # display options
        sel = get_user_option(1, 2)
        while sel < 1 or sel > 2:
            print("Invalid input. Please try again")
            sel = get_user_option(1, 2)
        # Get and verify input
        if sel == 1:
            print("Please choose a friend from the list above")
            opt = get_user_option(1, friend_id)
            while opt < 1 or opt > friend_id:
                print("Invalid input. Please try again")
                opt = get_user_option(1, friend_id)
            count = 0
            for user in data["users"]:
                if count == opt:
                    tmp = display_user(user["username"])
                    continue
                # When the correct ID reached then display the profile and run the options again
                count += 1
                # If not the correct ID then increment by 1
                # NOT efficient for a big database so working on a better way

        elif sel == 2:
            break
    return True

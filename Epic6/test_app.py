# This file contains all our pytest

# Import every method/variable from our app file
from app import *
import json


print("Starting test")

def test_user_option():
    option = get_user_option(1, 3)
    assert isinstance(option, int)
    assert option <= 5 and option >= 1


def test_verify_password():
    acceptable_passwords = [
        "tahirMon@1",
        "hoanGngu@12",
        "joRgo(76"
    ]
    invalid_passwords = [
        "tahirMo",
        "hoangnguy@",
        "jorgoK76",
        "invalid",
        "inV#lid"
    ]

    for password in acceptable_passwords:
        assert verify_password(password) == True

    for password in invalid_passwords:
        assert verify_password(password) == False


# initializes empty database
with open("test_database.json", 'w+') as db:
    init_db = {
        "users": []
    }
    json.dump(init_db, db)
    db.close()


def test_login_and_register():
    valid_fake_users = [
        {"username": "newUser46", "password": "tahirMon@1",
            "first_name": "John", "last_name": "Cena"},
        {"username": "newUser47", "password": "hoanGngu@12",
            "first_name": "The", "last_name": "Rock"},
        {"username": "newUser48",
            "password": "joRgo(76", "first_name": "Elon", "last_name": "Musk"},
        {"username": "newUser49", "password": "newUser4@",
            "first_name": "Steve", "last_name": "Jobs"},
        {"username": "newUser50", "password": "newUser4$",
            "first_name": "Bill", "last_name": "Gates"},
    ]

    for user in valid_fake_users:
        assert verify_register(user["username"], user["password"], user["first_name"],
                               user["last_name"], database="test_database.json") == True
        assert login(user["username"], user["password"],
                     database="test_database.json") == True  # verify_login

    # lets now delete user and test that we can't register a user that doesnt have unique username and first/last name
    with open("test_database.json", 'r') as db:
        data = json.load(db)
        db.close()

    with open("test_database.json", 'w+') as db:
        data["users"].pop()
        json.dump(data, db)
        db.close()

    for i in range(4):
        assert verify_register(valid_fake_users[i]["username"], valid_fake_users[i]["password"], valid_fake_users[i]
                               ["first_name"], valid_fake_users[i]["last_name"], database="test_database.json") == False

    # Insert the user that was deleted so it is full again
    assert verify_register(valid_fake_users[4]["username"], valid_fake_users[4]["password"], valid_fake_users[4]
                           ["first_name"], valid_fake_users[4]["last_name"], database="test_database.json") == True


def test_skills_options():
    options = list_of_skills()
    assert options[0] <= 6 and options[0] >= 1
    if options[0] == 1:
        assert options[1] == "1.) Programming"
    if options[0] == 2:
        assert options[1] == "2.) Carpentry"
    if options[0] == 3:
        assert options[1] == "3.) Photography"
    if options[0] == 4:
        assert options[1] == "4.) Microsoft Excel"
    if options[0] == 5:
        assert options[1] == "5.) Learn Spanish"
    if options[0] == 6:
        assert options[1] == "6.) Exit"


def test_post_job():
    valid_fake_jobs = [
        ["", "", "", "", ""],
        ["Mover", "Help clients move to new house",
            "Bulls Moving Co.", "Tampa, FL", 10],
        ["Developer", "Develop new state of the art software at our company!",
            "Apple", "San Francisco, CA", "hudred thousand dollars"],
        ["Professor", "None", "USF", "Tampa, FL", 80000],
    ]
    new_job = ["Janitor", "Clean the mess of the future generation of engineers",
               "USF", "Tampa, FL", "25 dollars an hours"]

    invalid_fake_jobs = [
        [None, "Help clients move to new house",
            "Bulls Moving Co.", "Tampa, Fl", 10],
        ["Professor", None, "USF", "Tampa, Fl", 80000],
        [None, "Clean the mess of the future generation of engineers",
            "USF", "Tampa, FL", None],
    ]

    # Test invalid jobs
    for i in range(len(invalid_fake_jobs)):
        assert post_job(invalid_fake_jobs[i][0], invalid_fake_jobs[i][1], invalid_fake_jobs[i][2],
                        invalid_fake_jobs[i][3], invalid_fake_jobs[i][4], database="test_database.json") == [False, 500]

    # Login each user to Test valid job postings
    with open("test_database.json", "r") as db:
        data = json.load(db)
        db.close()

    i = 0
    for user in data["users"]:
        login(user["username"], user["password"],
              database="test_database.json")

        if i == 4:  # Test limit of 4 jobs
            assert post_job(new_job[0], new_job[1], new_job[2], new_job[3],
                            new_job[4], database="test_database.json") == [False, 404]
        else:  # Test valid jobs
            assert post_job(valid_fake_jobs[i][0], valid_fake_jobs[i][1], valid_fake_jobs[i][2],
                            valid_fake_jobs[i][3], valid_fake_jobs[i][4], database="test_database.json") == [True, 200]
        i += 1


def test_find_user():
    valid_fake_users = [
        {"username": "newUser46", "password": "tahirMon@1",
            "first_name": "John", "last_name": "Cena"},
        {"username": "newUser47", "password": "hoanGngu@12",
            "first_name": "The", "last_name": "Rock"},
        {"username": "newUser48",
            "password": "joRgo(76", "first_name": "Elon", "last_name": "Musk"},
        {"username": "newUser49", "password": "newUser4@",
            "first_name": "Steve", "last_name": "Jobs"},
        {"username": "newUser50", "password": "newUser4$",
            "first_name": "Bill", "last_name": "Gates"},
    ]

    invalid_fake_users = [
        {"username": "newUser44", "password": "tahirM3on@1",
            "first_name": "Johns", "last_name": "Qen"},
        {"username": "newUser42", "password": "hoanGn3gu@12",
            "first_name": "Thes", "last_name": "Rocky"},
        {"username": "newUser41",
            "password": "joRgo2(76", "first_name": "Elona", "last_name": "Musq"},
        {"username": "newUser4", "password": "newUser14@",
            "first_name": "Steven", "last_name": "Job"},
        {"username": "newUser510", "password": "newU1ser4$",
            "first_name": "Billy", "last_name": "Gate"},
    ]

    for user in invalid_fake_users:
        assert find_user(user["first_name"], user["last_name"],
                         database="test_database.json") == False

    with open("test_database.json", "r") as db:
        data = json.load(db)
        db.close()

    for user in data["users"]:
        assert find_user(user["first_name"], user["last_name"],
                         database="test_database.json") == True


def test_useful_links():
    ### CANNOT TEST SIGNUP OPTION, WILL FAIL BECAUSE OF EXTRA NEEDED INPUT ###

    # Delete a user if database is full to test the sign up option
    # with open("database.json", 'r') as db:
    #         data = json.load(db)
    #         db.close()

    # with open("database.json", 'w+') as db:
    #         data["users"].pop()
    #         json.dump(data, db)
    #         db.close()

    options = print_useful_links()
    if options == 1:
        assert options == """
                            --Available Options--
                            1.) Sign Up
                            2.) Help Center
                            3.) About
                            4.) Press
                            5.) Blog
                            6.) Careers
                            7.) Developers
                            8.) Go Back
                            """
        # Not sure how to test the signup option
        # if options == 1:
        #     assert options == True
        if options == 2:
            assert options == "We're here to help"
        if options == 3:
            assert options == "InCollege: Welcome to InCollege, the world's largest college student network with many users in many countries and territories worldwide"
        if options == 4:
            assert options == "InCollege Pressroom: Stay on top of the latest news, updates, and reports"
        if options == 5:
            assert options == "Under Construction"
        if options == 6:
            assert options == "Under Construction"
        if options == 7:
            assert options == "Under Construction"
        if options == 8:
            assert options == False  # "Going back to 'Useful Links' Menu"
    if options == 2:
        assert options == "Under Construction"
    if options == 3:
        assert options == "Under Construction"
    if options == 4:
        assert options == "Under Construction"
    if options == 5:
        assert options == False

    # Tried to test automatic input for signup but tests kept failing, tried nested mocks but still failed
    # with mock.patch.object(builtins, 'input', lambda _: 1):
    #      assert print_useful_links()
    # with mock.patch.object(builtins, 'input', lambda _: '1'):
    #     assert print_useful_links()
    # with mock.patch.object(builtins, 'input', lambda _: 'Bernie'):
    #     assert print_useful_links()
    # with mock.patch.object(builtins, 'input', lambda _: 'Sanders'):
    #     assert print_useful_links()
    # with mock.patch.object(builtins, 'input', lambda _: 'Sandman'):
    #     assert print_useful_links()
    # with mock.patch.object(builtins, 'input', lambda _: "S@ndm@n69*"):
    #     assert print_useful_links()
    # with mock.patch.object(builtins, 'input', lambda _: '8'):
    #     assert print_useful_links()
    # with mock.patch.object(builtins, 'input', lambda _: '5'):
    #     assert print_useful_links() == False


def test_privacy_policy():
    # empty the database
    with open("test_database.json", 'w+') as db:
        init_db = {
            "users": []
        }
        json.dump(init_db, db)
        db.close()
    fake_user = {"username": "newUser46", "password": "tahirMon@1",
                 "first_name": "John", "last_name": "Cena"}
    assert verify_register(fake_user["username"], fake_user["password"],
                           fake_user["first_name"], fake_user["last_name"], "test_database.json") == True
    LOGGED_IN_USER
    assert login(fake_user["username"],
                 fake_user["password"], "test_database.json") == True
    assert toggle_privacy(
        LOGGED_IN_USER["username"], "test_database.json") == True
    with open("test_database.json", "r") as db:
        data = json.load(db)
        for user in data["users"]:
            if user["username"] == LOGGED_IN_USER["username"]:
                assert isinstance(user["settings"]["email"], bool)
                assert isinstance(user["settings"]["sms"], bool)
                assert isinstance(user["settings"]["targeted_ads"], bool)
                assert isinstance(user["settings"]["language"], str)

                assert user["settings"]["email"] == False or user["settings"]["email"] == True
                assert user["settings"]["sms"] == False or user["settings"]["sms"] == True
                assert user["settings"]["targeted_ads"] == False or user["settings"]["targeted_ads"] == True
                assert user["settings"]["language"] == "English" or user["settings"]["language"] == "Spanish"
        db.close()


def test_upper_case_func():
    lowercase_majors = [
        "Computer science",
        "computer engineering",
        "biology",
        "chemical engineering",
        "fake major with five words"
    ]
    assert upper_case(lowercase_majors[0]) == "Computer Science"
    assert upper_case(lowercase_majors[1]) == "Computer Engineering"
    assert upper_case(lowercase_majors[2]) == "Biology"
    assert upper_case(lowercase_majors[3]) == "Chemical Engineering"
    assert upper_case(lowercase_majors[4]) == "Fake Major With Five Words"


def test_creating_profile():
    with open("test_database.json", 'w+') as db:
        init_db = {
            "users": []
        }
        json.dump(init_db, db)
        db.close()
    profile_1 = {
        "title": "Senior",
        "major": upper_case("computer science"),
        "university": upper_case("university of south florida"),
        "about": "test friend",
        "experience": [
            {
                "title": "Customer relation director",
                "employer": "Burgerking",
                "date_started": "6/9/2006",
                "date_ended": "6/9/2009",
                "location": "Tampa",
                "description": "Handle and fulfill customer's request"
            }
        ],
        "education": [
            {
                "school": "USF",
                "degree": "Undergrad",
                "years_att": "2069"
            }
        ]
    }
    fake_user = {"username": "newUser46", "password": "tahirMon@1",
                 "first_name": "John", "last_name": "Cena"}
    assert verify_register(fake_user["username"], fake_user["password"],
                           fake_user["first_name"], fake_user["last_name"], "test_database.json") == True
    LOGGED_IN_USER
    assert login(fake_user["username"],
                 fake_user["password"], "test_database.json") == True
    assert post_title(profile_1["title"], profile_1["major"], profile_1["university"], profile_1["about"],
                      profile_1["experience"], profile_1["education"], "test_database.json")[0] == True
    with open("test_database.json", 'r') as db:
        data = json.load(db)
        for user in data["users"]:
            if user.get("posted_title"):  # Only verify is user has created a profile
                # Verify major is capitalized
                major = user["posted_title"]["major"].split()
                assert (x.isupper() for x in major)

                # Verify university is capatilized
                university = user["posted_title"]["university"].split()
                assert (x.isupper() for x in university)

                # Verify experience is more than 3
                experience_length = len(user["posted_title"]["experience"])
                assert experience_length >= 0 and experience_length <= 3

def test_profile_view():
    with open("test_database.json", 'w+') as db:
        init_db = {
            "users": []
        }
        json.dump(init_db, db)
        db.close()
    profile_1 = {
        "title": "Senior",
        "major": "Computer Science",
        "university": "USF",
        "about": "test 2",
        "experience": [
            {
                "title": "Customer relation director",
                "employer": "McDonald's",
                "date_started": "6/9/2006",
                "date_ended": "6/9/2009",
                "location": "Tampa",
                "description": "Handle and fulfill customer's request"
            }
        ],
        "education": [
            {
                "school": "USF",
                "degree": "Undergrad",
                "years_att": "2020"
            }
        ]
    }
    profile_2 = {
        "title": "Senior",
        "major": "Computer Science",
        "university": "USF",
        "about": "test 2",
        "experience": [
            {
                "title": "Customer relation director",
                "employer": "McDonald's",
                "date_started": "6/9/2006",
                "date_ended": "6/9/2009",
                "location": "Tampa",
                "description": "Handle and fulfill customer's request"
            }
        ],
        "education": [
            {
                "school": "USF",
                "degree": "Undergrad",
                "years_att": "2020"
            }
        ]
    }
    fake_user = {"username": "alexm", "password": "Alex123!",
                 "first_name": "Alex", "last_name": "Miller"}
    fake_friend = {"username": "ayman", "password": "Ayman123!",
                 "first_name": "Ayman", "last_name": "Nagi"}
    assert verify_register(fake_user["username"], fake_user["password"],
                           fake_user["first_name"], fake_user["last_name"], "test_database.json") == True

    display_user(fake_user["username"])

    friend_option()

    options = get_user_option(1,2)
    if options == 1:
        print("No friends listed")
    if options == 2:
        assert options == 2


def test_friend_list():
    with open("test_database.json", 'w+') as db:
        init_db = {
            "users": []
        }
        json.dump(init_db, db)
        db.close()
    fake_user = {"username": "alexm", "password": "Alex123!",
                 "first_name": "Alex", "last_name": "Miller"}
    assert verify_register(fake_user["username"], fake_user["password"],
                           fake_user["first_name"], fake_user["last_name"], "test_database.json") == True
    str = ""
    print("You have already connected with:")
    with open('test_database.json') as db:
        data = json.load(db)
        for user in data["users"]:
            if user["username"] == LOGGED_IN_USER["username"]:
                str = LOGGED_IN_USER["username"]
                print('\n'.join(user["friends"]), )

            yes_no = prompt("Would you like to disconnect from any of your friends?(y/n): ")
            if yes_no:
                deleted_friend = input("Enter the name of the friend you want to delete from the list above: ")
                if deleted_friend in user["friends"]:
                    user["friends"].remove(deleted_friend)
                    print(deleted_friend, "was deleted")

                    with open('test_database.json', 'w+') as db:
                        json.dump(data, db)
                    for user in data["users"]:
                        if user["username"] == deleted_friend:
                            user["friends"].remove(str)
                            with open('test_database.json', 'w+') as db:
                                json.dump(data, db)
                else:
                    print("The username you entered is not part of your friends.")
            else:
                break

def test_friend_search():
    username = input("Please enter a username (type in 'alexm' for test): ")
    password = input("Please enter a password (type in 'Alexm123!' for test) : ")
    logged_in = login(username, password)

    friend = str(
        input("Search for people you know by last name, university, or thier major (type in last name 'Nagi' for test case): "))
    people_found = []
    found_friend = False

    # Search db for friend by last name, university, or major
    with open("database.json", 'r') as db:
        data = json.load(db)
        for user in data["users"]:
            if user["username"] == LOGGED_IN_USER["username"]:
                continue
            if user["last_name"] == friend:
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


def test_del_job():
    with open("test_database.json", 'w+') as db:
        init_db = {
            "users": []
        }
        json.dump(init_db, db)
        data = json.load(db)
        db.close()
    fake_user = {"username": "alexm", "password": "Alex123!",
                 "first_name": "Alex", "last_name": "Miller"}
    assert verify_register(fake_user["username"], fake_user["password"],
                           fake_user["first_name"], fake_user["last_name"], "test_database.json") == True
    logged_in = login("alexm", "Alexm123!")
    while True:
        time.sleep(1)
        print_manage_jobs()
        user_choice = get_user_option(1, 5)
        while user_choice < 1 or user_choice > 5:
            print("Invalid input. Try again")
            user_choice = get_user_option(1, 5)
        if user_choice == 1:  # Delete a job
            deleted = delete_job()
            assert deleted == True
            return True
        elif user_choice == 2:  # View saved jobs
            edit_saved = edit_saved_jobs()
            assert edit_saved == True
            return True
        elif user_choice == 3:  # View applied jobs
            printApplied = print_applied_jobs()
            assert printApplied == True
            return True
        elif user_choice == 4:  # View jobs not applied for
            notApplied = print_not_applied()
            assert notApplied == True
            return True
        else:
            break


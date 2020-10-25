import time
from modules.register import *

def get_user_option(limit1, limit2):
    while True:
        try:
            option1 = int(
                input(f"Please enter your option ({limit1}-{limit2}): "))
            return option1
        except ValueError:
            print("Input has to be an integer")


def print_general_links():
    links = """
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
    print(links)


def print_useful_links():
    links = """
    
    --Available Options--
    1.) General
    2.) Browse InCollege
    3.) Business Solutions
    4.) Directories
    5.) Go Back
    
    """

    while True:
        print(links)
        option = get_user_option(1, 5)
        while option < 1 or option > 5:
            print("Invalid input. Try again")
            option = get_user_option(1, 5)
        if option == 1:
            while True:
                print_general_links()
                options = get_user_option(1,8)
                while options < 1 or options > 8:
                    print("Invalid input. Try again")
                    options = get_user_option(1, 8)
                if options == 1:
                    registered = register()
                    if not registered:
                        exit()
                    else:
                        continue
                elif options == 2:
                    print("We're here to help")
                    time.sleep(2)
                    continue
                elif options == 3:
                    print("InCollege: Welcome to InCollege, the world's largest college student network with many users in many countries and territories worldwide")
                    time.sleep(2)
                    continue
                elif options == 4:
                    print("InCollege Pressroom: Stay on top of the latest news, updates, and reports")
                    time.sleep(2)
                    continue
                elif options == 5:
                    print("Under Construction")
                    time.sleep(2)
                    continue
                elif options == 6:
                    print("Under Construction")
                    time.sleep(2)
                    continue
                elif options == 7:
                    print("Under Construction")
                    time.sleep(2)
                    continue
                elif options == 8:
                    print("Going back to 'Useful Links' Menu")
                    time.sleep(2)
                    print_useful_links()
                    return False
        elif option == 2:
            print("Under construction")
            time.sleep(2)
            continue
        elif option == 3:
            print("Under construction")
            time.sleep(2)
            continue
        elif option == 4:
            print("Under construction")
            time.sleep(2)
            continue
        elif option == 5:
            print("Going back to the Main Menu")
            time.sleep(2)
            return False
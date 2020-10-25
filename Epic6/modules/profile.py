import json
import string
from modules.login import LOGGED_IN_USER


def upper_case(str1):
    return string.capwords(str1)


def experience():
    job = {}
    title = input("Title: ")
    job["title"] = title
    employer = input("Employer: ")
    job["employer"] = employer
    date_started = input("Date Started: ")
    job["date_started"] = date_started
    date_ended = input("Date Ended: ")
    job["date_ended"] = date_ended
    location = input("Location: ")
    job["location"] = location
    description = input("Description: ")
    job["description"] = description
    return job


def prompt(message):
    while True:
        choice = input(message).lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        else:
            print("Please enter y or n")


def post_title(title, major, university, about, experience, education, database):
    with open(database) as db:
        data = json.load(db)
    with open(database, 'w+') as db:
        new_title = {
            "title": title,
            "major": major,
            "university": university,
            "about": about,
            "experience": experience,
            "education": education
        }
        for user in data["users"]:
            if user["username"] == LOGGED_IN_USER["username"]:
                # user["posted_title"] = []  # I added this
                user["posted_title"] = new_title
        json.dump(data, db)
        db.close()
        return [True, 200]


def profile():
    title = input("Title: ")
    major = input("Major: ")
    major = upper_case(major)
    university = input("University: ")
    university = upper_case(university)
    about_info = input("About Info: ")
    print("Experience Section:")
    #print("You can enter information for up to 3 past jobs.Do you wish to continue?(y/n)")
    yes_no = prompt(
        "You can enter information for up to 3 past jobs.Do you wish to continue?(y/n)")
    total_experience = []

    if yes_no == True:
        job1 = experience()
        yes_no = prompt("Do you wish to enter another job?(y/n) ")
        if yes_no == True:
            job2 = experience()
            yes_no = prompt("Do you wish to enter another job?(y/n)")
            if yes_no == True:
                job3 = experience()
                print("All 3 Jobs were Registered.")
                total_experience.append(job3)
            else:
                print("2 Jobs Was Registered.")
                total_experience.append(job2)
        else:
            print("1 Job Was Registered.")
            total_experience.append(job1)

    else:
        print("No Job Was Registered.")
    print("Education Section.")
    school = input("School name: ")
    degree = input("Degree: ")
    years_attended = input("Years attended: ")
    education = {
        "school": school,
        "degree": degree,
        "years_att": years_attended
    }
    print(title, major, university, about_info, total_experience, education)
    a = post_title(title, major, university, about_info,
                   total_experience, education, 'database.json')

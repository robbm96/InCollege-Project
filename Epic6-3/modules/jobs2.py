import json
import uuid
import time
import string
from modules.login import LOGGED_IN_USER


def load_db(database="database.json"):
    try:
        with open(database, 'r+') as db:
            return json.load(db)
    except Exception as e:
        raise e


# helper function that adds "job_id" attribute to all existing jobs
def add_id_to_all_jobs(database="database.json"):
    data = load_db(database)
    for user in data["users"]:
        for job in user["posted_jobs"]:
            if not job.get("job_id", None):
                job["job_id"] = str(uuid.uuid1())
    with open(database, 'w+') as db:
        json.dump(data, db)


# Returns the logged in users information
def get_logged_in_users_data(username, database="database.json"):
    return [user for user in load_db(
        database)["users"] if user["username"] == username][0]


# Returns all the jobs from the database. Includes whether they applied or not
def get_all_jobs(database="database.json"):
    # load the database
    add_id_to_all_jobs(database)
    data = load_db(database)
    all_jobs = []
    # Add all the jobs in database to an array
    for user in data["users"]:
        for job in user["posted_jobs"]:
            all_jobs.append(job)

    # iterate through jobs array and check if user has applied to job
    user_info = get_logged_in_users_data(LOGGED_IN_USER["username"], database)
    for job in all_jobs:
        job["has_applied"] = False
        for jobs in user_info["applied_jobs"]:
            has_applied = True if jobs == job["job_id"] else False
            job["has_applied"] = has_applied
    return all_jobs


# Print all jobs
def print_all_jobs(jobs):
    print(f"Gathering List of Jobs")
    print(
        "Jobs that you have applied to are indicated with a '\N{check mark}'")
    time.sleep(2)
    for index, job in enumerate(jobs):
        has_applied = '\N{check mark}' if job["has_applied"] else ""
        title = job["title"]
        print(f"{index + 1}.) Job Title: {title} {has_applied} ")


# Print job info
def print_job_info(job):
    job_description = f"""
    Job Title: {job["title"]}
    Description: {job["description"]}
    Employer: {job["employer"]}
    Location: {job["location"]}
    Salary: {job["salary"]}
    """
    print(job_description)


def check_applied_jobs(username, job_id, database="database.json"):
    user_info = get_logged_in_users_data(username, database)
    for job in user_info["applied_jobs"]:
        if job == job_id:
            return True
    return False


def validate_date_input(date):
    new_date = date.split('/')
    try:
        if len(new_date) == 3 and len(new_date[0]) == 2 and len(new_date[1]) == 2 and len(new_date[2]) == 4:
            return True
    except Exception as e:
        print("Invalid date format")
        return False
    print("Invalid date format")

    return False


def apply_to_job(job, database):
    has_user_applied = check_applied_jobs(
        LOGGED_IN_USER["username"], job["job_id"], database)
    if has_user_applied:
        print("Job has already been applied to. Please select a different job")
        return [False, 'a']
    grad_date = input("Enter your graduation date in mm/dd/yyyy format: ")
    valid = validate_date_input(grad_date)
    if not valid:
        return [False, 'a']

    work_date = input(
        "Enter a date that you can start working in mm/dd/yyyy format: ")
    valid = validate_date_input(work_date)
    if not valid:
        return [False, 'a']

    user_text = input("Explain why you are a good fit for this job: ")

    with open(database, 'r+') as db:
        data = json.load(db)
        for user in data["users"]:
            if user["username"] == LOGGED_IN_USER["username"]:
                user["applied_jobs"].append(job["job_id"])
    with open(database, 'w+') as db:
        json.dump(data, db)
    print("You successfully applied to the job!")
    return [True, 'a']


def save_job(job, database="database.json"):
    with open(database, 'r+') as db:
        data = json.load(db)
        for user in data["users"]:
            if user["username"] == LOGGED_IN_USER["username"]:
                user["saved_jobs"].append(job["job_id"])
                unique_saved = set(user["saved_jobs"])
                user["saved_jobs"] = list(unique_saved)
    with open(database, 'w+') as db:
        json.dump(data, db)
    print("Job successfully saved")
    return [True, 's']


def job_options():
    print("Would you like to view a job, apply for a job, or add a job to your saved jobs?")
    option = input(
        "Enter v for view, a for apply, s for save, x to go back to main menu: ")
    return option


# Validates job option
def validate_job_option(option):
    if option.lower() in ['v', 'a', 's', 'x']:
        return True
    else:
        print("Invalid input. Please try again")
        return False


def process_option(option, job, database="database.json"):
    option = option.lower()
    success = []
    if option == 'v':
        print_job_info(job)
        success = [True, 'v']
    elif option == 'a':
        success = apply_to_job(job, database)
    elif option == 's':
        success = save_job(job, database)
    elif option == 'x':
        success = [False, 'x']
    return success

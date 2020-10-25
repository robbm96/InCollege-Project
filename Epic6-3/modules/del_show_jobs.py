import time
import json
from modules.login import *
from modules.jobs2 import *


def get_user_option(limit1, limit2):
    while True:
        try:
            option1 = int(
                input(f"Please enter your option ({limit1}-{limit2}): "))
            return option1
        except ValueError:
            print("Input has to be an integer")


def print_jobs(all_jobs):
    for index, job in enumerate(all_jobs):
        title = job["title"]
        print(f"{index + 1}.) Job Title: {title}")


# Person who posted job can delete it
def delete_job(database="database.json"):
    with open(database) as db:
        data = json.load(db)
    with open(database, 'w+') as db:
        for user in data["users"]:
            if user["username"] == LOGGED_IN_USER["username"]:
                users_jobs = []
                for job in user["posted_jobs"]:  # Get all user's posted jobs
                    users_jobs.append(job)

                if len(users_jobs) == 0:
                    print("You have no jobs posted.")
                    json.dump(data, db)
                    db.close()
                    return True
                else:
                    print("Which job would you like to delete?")
                    print_jobs(users_jobs)

                    # for index, job in enumerate(users_jobs):
                    #     title = job["title"]
                    #     print(f"{index + 1}.) Job Title: {title}")

                    toDelete = get_user_option(1, len(users_jobs))
                    toDelete -= 1

                    deletedJob = user["posted_jobs"][toDelete]
                    del user["posted_jobs"][toDelete]
                    json.dump(data, db)
                    db.close()
                    remove_from_applied(deletedJob)
                    remove_from_saved(deletedJob)
                    break

    print("Job has been successfully deleted")
    time.sleep(2)
    return True


# Removes the deleted job from all users[applied jobs] section if they have applied for it
def remove_from_applied(deletedJob, database="database.json"):
    with open(database) as db:
        data = json.load(db)
    with open(database, 'w+') as db:
        for user in data["users"]:
            if "applied_jobs" not in user:  # Create applied_jobs section if not created yet
                    user["applied_jobs"] = []
                    continue
            for job in user["applied_jobs"]:
                if deletedJob["job_id"] == job:
                    user["applied_jobs"].remove(job)
        json.dump(data, db)
        db.close()


# Removes the deleted job from all users[saved] section if they have saved for it
def remove_from_saved(deletedJob, database="database.json"):
    with open(database) as db:
        data = json.load(db)
    with open(database, 'w+') as db:
        for user in data["users"]:
            if "saved_jobs" not in user:  # Create "saved_jobs" section if not created yet
                    user["saved_jobs"] = []
                    continue
            for job in user["saved_jobs"]:
                if deletedJob["job_id"] == job:
                    user["saved_jobs"].remove(job)
        json.dump(data, db)
        db.close()


def print_applied_jobs(database="database.json"):
    with open(database) as db:
        data = json.load(db)
        for user in data["users"]:
            if user["username"] == LOGGED_IN_USER["username"]:
                if "applied_jobs" not in user:  # Create "applied_jobs" section if not created yet
                    user["applied_jobs"] = []
                    print("You have not applied for any jobs yet.")
                    return False

                applied_jobs = []
                for ID in user["applied_jobs"]:  # Get all user's applied jobs
                    applied_jobs.append(ID)
                
                if len(applied_jobs) == 0:
                    print("You have not applied for any jobs yet.")
                    db.close()
                    return True
                
                else:
                    # Use job_ID to find corresponding job
                    all_jobs = []
                    for user in data["users"]:
                        for job in user["posted_jobs"]:
                            if job["job_id"] in applied_jobs:
                                all_jobs.append(job)
                    
                    print("\nHere are the jobs you have applied for:")
                    for index, job in enumerate(all_jobs):
                        title = job["title"]
                        print(f"{index + 1}.) Job Title: {title}")
                    db.close()
                    time.sleep(2)
                    return True


def print_not_applied(database="database.json"):
    with open(database) as db:
        data = json.load(db)
        # Get all jobs
        all_jobs = []
        for user in data["users"]:
            if "posted_jobs" not in user:  # Create posted_jobs section if not created yet
                    user["posted_jobs"] = []
                    continue
            for job in user["posted_jobs"]:
                all_jobs.append(job)
        
        for user in data["users"]:
            if user["username"] == LOGGED_IN_USER["username"]:
                if "applied_jobs" not in user:  # Create "applied_jobs" section if not created yet
                    user["applied_jobs"] = []
                    # User has not applied for any job so print them all
                    print("\nHere are the jobs you have not applied for:")
                    print_jobs(all_jobs)
                    db.close()
                    time.sleep(2)
                    return True

                else:
                    applied_jobs = []
                    for ID in user["applied_jobs"]:  # Get all user's applied jobs
                        applied_jobs.append(ID)
                    
                    if len(applied_jobs) == 0:
                        print("\nHere are the jobs you have not applied for:")
                        print_jobs(all_jobs)
                        db.close()
                        time.sleep(3)
                        return True
            
                    else:
                        # Use job_ID to find if user has applied or not, remove all jobs applied for 
                        for job in all_jobs:
                            if job["job_id"] in applied_jobs:
                                all_jobs.remove(job)
                        
                        print("\nHere are the jobs you have not applied for:")
                        print_jobs(all_jobs)
                        db.close()
                        time.sleep(2)
                        return True


def edit_saved_jobs(database="database.json"):
    with open(database) as db:
        data = json.load(db)
    with open(database, 'w+') as db:
        # # Get all jobs
        # all_jobs = []
        # for user in data["users"]:
        #     if "posted_jobs" not in user:  # Create posted_jobs section if not created yet
        #             user["posted_jobs"] = []
        #             continue
        #     for job in user["posted_jobs"]:
        #         all_jobs.append(job)
        
        for user in data["users"]:
            if user["username"] == LOGGED_IN_USER["username"]:
                if "saved_jobs" not in user:  # Create "saved_jobs" section if not created yet
                    user["saved_jobs"] = []
                    # User has not saved any jobs
                    print("\nYou have not saved any jobs\n")
                    json.dump(data, db)
                    db.close()
                    time.sleep(1)
                    return False
                else:
                    saved_jobs = []
                    for ID in user["saved_jobs"]:  # Get all user's saved jobs
                        saved_jobs.append(ID)

                    # Get all saved jobs
                    all_jobs = []
                    for user in data["users"]:
                        for job in user["posted_jobs"]:
                            if job["job_id"] in saved_jobs:
                                all_jobs.append(job)
                    
                    print("Here are your saved jobs:")
                    print_jobs(all_jobs)

                    # Give option to delete a saved job
                    contin = True
                    while contin:
                        unsave = str(input("Would you like to un-save any? (y/n): "))
                        if unsave[0].lower() in ['y', 'n']:
                            contin = False
                        else:
                            print("Invalid input. Please try again")
                    
                    if unsave[0] == 'n':
                        json.dump(data, db)
                        db.close()
                        return True
                    else:
                        print("Which job would you like to un-save?")
                        toDelete = get_user_option(1, len(all_jobs))
                        toDelete -= 1

                        for i in range(len(saved_jobs)):
                            if saved_jobs[i] == all_jobs[toDelete]["job_id"]:
                                del user["saved_jobs"][i]
                                break
                        
                        json.dump(data, db)
                        db.close()
                        print("Job successfully un-saved.\n")
                        time.sleep(2)
                        return True

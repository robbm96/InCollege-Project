import json
import uuid
from modules.login import LOGGED_IN_USER


def post_job(title, description, employer, location, salary, database):
    if title is None or description is None or employer is None or location is None or salary is None:
        print("Missing key values. Please enter all required fields")
        return [False, 500]
    with open(database) as db:
        data = json.load(db)
        job_count = 0
        for user in data["users"]:
            if user.get("posted_jobs"):
                job_count = job_count + len(user["posted_jobs"])

        if job_count == 10:
            print("All permitted jobs have been created. Try again later")
            return [False, 404]
        db.close()

    with open(database, 'w+') as db:
        new_job = {
            "job_id": str(uuid.uuid1()),
            "title": title,
            "description": description,
            "employer": employer,
            "location": location,
            "salary": salary
        }
        for user in data["users"]:
            if user["username"] == LOGGED_IN_USER["username"]:
                user["posted_jobs"].append(new_job)
        json.dump(data, db)
        db.close()
        print("You have successfully posted a job")
        return [True, 200]

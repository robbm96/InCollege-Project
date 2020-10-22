import json
import time

def find_user(first_name, last_name, database):
    with open(database) as db:
        data = json.load(db)
        for user in data["users"]:
            if user["first_name"] == first_name and user["last_name"] == last_name:
                print("They are a part of the InCollege system")
                return True

        print("They are not yet part of the InCollege system")
        time.sleep(2)
        return False
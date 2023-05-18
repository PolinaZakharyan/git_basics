from system_helpers import get_data_from_file, write_to_file

USERS_FILE_PATH = "database/users.json"


def save_user(first_name, last_name, email):
    data = get_data_from_file(USERS_FILE_PATH)
    new_obj = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email
    }
    if len(data) >= 1:
        new_obj["id"] = len(data) + 1
    else:
        new_obj["id"] = 1
    data.append(new_obj)
    write_to_file(USERS_FILE_PATH)


def get_all_users():
    data = get_data_from_file(USERS_FILE_PATH)
    for obj in data:
        print(obj["id"])
        print(obj["first_name"])
        print(obj["last_name"])
        print(obj["email"])
        print("================================")


def get_user_by_id(id):
    data = get_data_from_file(USERS_FILE_PATH)
    for obj in data:
        if id == obj["id"]:
            print(obj["id"])
            print(obj["first_name"])
            print(obj["last_name"])
            print(obj["email"])


def delete_user(id):
    data = get_data_from_file(USERS_FILE_PATH)
    for i in range(len(data)):
        if data[i]["id"] == id:
            del data[i]
            break
    write_to_file(USERS_FILE_PATH, data)


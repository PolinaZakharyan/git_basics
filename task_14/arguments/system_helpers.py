import json


def get_data_from_file(file_path):
    file = open(file_path, "r")
    data = json.loads(file.read())
    file.close()
    return data


def write_to_file(file_path, data):
    file = open(file_path, "w")
    file.write(json.dumps(data))
    file.close()
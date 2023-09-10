import json


def read_credentials_from_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        access_key = data['access_key']
        secret_key = data['secret_key']
        bucket = data['bucket']
    return access_key, secret_key, bucket

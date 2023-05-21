from pathlib import Path

import boto3
import json


def delete_file_from_s3(bucket_name, file_name, access_key, secret_key):
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    try:
        s3.delete_object(Bucket=bucket_name, Key=file_name)
        print(f'Successfully deleted {file_name} from {bucket_name}')
    except Exception as e:
        print(f'Error deleting file: {str(e)}')


def download_file_from_s3(bucket_name, file_name, destination_path, access_key, secret_key):
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    try:
        file_path = destination_path / file_name
        s3.download_file(bucket_name, file_name, file_path)
        print(f'Successfully downloaded {file_name} from {bucket_name} to {destination_path}')
    except Exception as e:
        print(f'Error downloading file: {str(e)}')


def upload_file_to_s3(file_path, bucket_name, access_key, secret_key):
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    file_name = file_path.split('/')[-1]  # Extract file name from file path

    try:
        s3.upload_file(file_path, bucket_name, file_name)
        print(f'Successfully uploaded {file_path} to {bucket_name}/{file_name}')
    except Exception as e:
        print(f'Error uploading file: {str(e)}')


# Read access key and secret key from a JSON file
def read_credentials_from_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        access_key = data['access_key']
        secret_key = data['secret_key']
        bucket = data['bucket']
    return access_key, secret_key, bucket


# Example usage
def upload():
    envs_folder = Path(__file__).parent.parent.parent / '.envs'
    json_file_path = envs_folder / 'invoice-user-aws-config.json'  # Path to the JSON file containing access key and secret key
    file_to_upload = '/home/luiscberrocal/PycharmProjects/invoicing_tools/output/Scanned_20230514-1153.pdf'  # Path to the file you want to upload

    access_key, secret_key, bucket = read_credentials_from_json(json_file_path)
    upload_file_to_s3(file_to_upload, bucket, access_key, secret_key)


def download():
    envs_folder = Path(__file__).parent.parent.parent / '.envs'
    json_file_path = envs_folder / 'invoice-user-aws-config.json'  # Path to the JSON file containing access key and secret key
    download_folder = Path(
        '/home/luiscberrocal/PycharmProjects/invoicing_tools/output/download')  # Path to the file you want to upload
    filename = 'Scanned_20230514-1153.pdf'

    access_key, secret_key, bucket = read_credentials_from_json(json_file_path)
    download_file_from_s3(bucket, filename, download_folder, access_key, secret_key)


def delete():
    envs_folder = Path(__file__).parent.parent.parent / '.envs'
    json_file_path = envs_folder / 'invoice-user-aws-config.json'  # Path to the JSON file containing access key and secret key
    filename = 'Scanned_20230514-1153.pdf'

    access_key, secret_key, bucket = read_credentials_from_json(json_file_path)

    delete_file_from_s3(bucket, filename, access_key, secret_key)

if __name__ == '__main__':
    # upload()
    # download()
    delete()

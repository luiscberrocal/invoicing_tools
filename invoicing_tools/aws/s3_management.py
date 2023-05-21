from pathlib import Path

import boto3

from invoicing_tools.aws.config import read_credentials_from_json


def list_files_and_folders_in_bucket(bucket_name, access_key, secret_key):
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    try:
        response = s3.list_objects_v2(Bucket=bucket_name)

        if 'Contents' in response:
            for obj in response['Contents']:
                file_name = obj['Key']
                print(f'File: {file_name}')

        if 'CommonPrefixes' in response:
            for folder in response['CommonPrefixes']:
                folder_name = folder['Prefix']
                print(f'Folder: {folder_name}')
    except Exception as e:
        print(f'Error listing files and folders: {str(e)}')


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


def upload_file_to_s3(*, file_path: Path, bucket_name: str, access_key: str, secret_key: str):
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    file_name = file_path.name

    try:
        s3.upload_file(file_path, bucket_name, file_name)
        print(f'Successfully uploaded {file_path} to {bucket_name}/{file_name}')
    except Exception as e:
        print(f'Error uploading file: {str(e)}')


# Example usage
def upload(file_to_upload: Path):
    envs_folder = Path(__file__).parent.parent.parent / '.envs'
    json_file_path = envs_folder / 'invoice-user-aws-config.json'  # Path to the JSON file containing access key and secret key
    access_key, secret_key, bucket = read_credentials_from_json(json_file_path)

    upload_file_to_s3(file_path=file_to_upload, bucket_name=bucket, access_key=access_key, secret_key=secret_key)


def download():
    envs_folder = Path(__file__).parent.parent.parent / '.envs'
    json_file_path = envs_folder / 'invoice-user-aws-config.json'  # Path to the JSON file containing access key and secret key
    download_folder = Path(
        '/home/luiscberrocal/PycharmProjects/invoicing_tools/output/download')  # Path to the file you want to upload
    filename = 'Scanned_20230514-1153.pdf'

    access_key, secret_key, bucket = read_credentials_from_json(json_file_path)
    download_file_from_s3(bucket, filename, download_folder, access_key, secret_key)


def delete(filename: str):
    envs_folder = Path(__file__).parent.parent.parent / '.envs'
    json_file_path = envs_folder / 'invoice-user-aws-config.json'  # Path to the JSON file containing access key and secret key
    # filename = 'Scanned_20230514-1153.pdf'

    access_key, secret_key, bucket = read_credentials_from_json(json_file_path)

    delete_file_from_s3(bucket, filename, access_key, secret_key)


def list_bucket():
    envs_folder = Path(__file__).parent.parent.parent / '.envs'
    json_file_path = envs_folder / 'invoice-user-aws-config.json'  # Path to the JSON file containing access key and secret key

    access_key, secret_key, bucket = read_credentials_from_json(json_file_path)

    list_files_and_folders_in_bucket(bucket_name=bucket, access_key=access_key, secret_key=secret_key)


if __name__ == '__main__':
    doc = 'Scanned_20230514-1153.png'
    library_folder = Path(__file__).parent.parent.parent
    output_folder = library_folder / 'output'
    upload_file = output_folder / doc
    upload(upload_file)
    # download()
    # delete(filename=doc)
    # list_bucket()

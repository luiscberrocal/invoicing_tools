import base64
import json
import os
import pickle
from pathlib import Path
from typing import List

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def create_service(client_secret_file, api_name, api_version, *scopes, prefix=''):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    cred = None
    working_dir = os.getcwd()
    token_dir = 'token files'
    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}{prefix}.pickle'

    ### Check if token dir exists first, if not, create the folder
    if not os.path.exists(os.path.join(working_dir, token_dir)):
        os.mkdir(os.path.join(working_dir, token_dir))

    if os.path.exists(os.path.join(working_dir, token_dir, pickle_file)):
        with open(os.path.join(working_dir, token_dir, pickle_file), 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(os.path.join(working_dir, token_dir, pickle_file), 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, API_VERSION, 'service created successfully')
        return service
    except Exception as e:
        print(e)
        print(f'Failed to create service instance for {API_SERVICE_NAME}')
        os.remove(os.path.join(working_dir, token_dir, pickle_file))
        return None


class GmailException(Exception):
    """gmail base exception class"""


class NoEmailFound(GmailException):
    """no email found"""


def search_emails(query_string: str, label_ids: List = None, max_results: int = 50):
    try:
        message_list_response = service.users().messages().list(
            userId='me',
            labelIds=label_ids,
            maxResults=max_results,
            q=query_string
        ).execute()

        message_items = message_list_response.get('messages')
        next_page_token = message_list_response.get('nextPageToken')
        if len(message_items) >= 50:
            return message_items

        while next_page_token:
            message_list_response = service.users().messages().list(
                userId='me',
                labelIds=label_ids,
                maxResults=max_results,
                q=query_string,
                pageToken=next_page_token
            ).execute()

            message_items.extend(message_list_response.get('messages'))
            next_page_token = message_list_response.get('nextPageToken')
        return message_items
    except Exception as e:
        print(f'{e}')
        raise NoEmailFound('No emails returned')


def get_file_data(message_id, attachment_id, file_name, save_location):
    response = service.users().messages().attachments().get(
        userId='me',
        messageId=message_id,
        id=attachment_id
    ).execute()

    file_data = base64.urlsafe_b64decode(response.get('data').encode('UTF-8'))
    return file_data


def get_message_detail(message_id, msg_format='metadata', metadata_headers: List = None):
    message_detail = service.users().messages().get(
        userId='me',
        id=message_id,
        format=msg_format,
        metadataHeaders=metadata_headers
    ).execute()
    return message_detail


if __name__ == '__main__':
    output_folder = Path('../output')
    CLIENT_FILE = output_folder / 'client_secret_gmail.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']
    service = create_service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)

    query_string = 'has:attachment'

    save_location = os.getcwd()
    email_messages = search_emails(query_string, max_results=5)

    for i, email_message in enumerate(email_messages):
        messageDetail = get_message_detail(email_message['id'], msg_format='full', metadata_headers=['parts'])
        print(f'{i} {messageDetail =}')
        file = output_folder / 'emails' / f'{i}-email-{messageDetail["id"]}.json'
        with open(file, 'w') as json_file:
            json.dump(messageDetail, json_file)
            if i == 10:
                break

        # messageDetailPayload = messageDetail.get('payload')

        # if 'parts' in messageDetailPayload:
        #     for msgPayload in messageDetailPayload['parts']:
        #         file_name = msgPayload['filename']
        #         body = msgPayload['body']
        #         if 'attachmentId' in body:
        #             attachment_id = body['attachmentId']
        #             attachment_content = get_file_data(email_message['id'], attachment_id, file_name, save_location)

        #             with open(os.path.join(save_location, file_name), 'wb') as _f:
        #                 _f.write(attachment_content)
        #                 print(f'File {file_name} is saved at {save_location}')
        # time.sleep(0.5)

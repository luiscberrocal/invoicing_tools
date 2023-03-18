# import the required libraries
import io
import pickle
from pathlib import Path

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from ..exceptions import UploadError


class GDrive:
    SCOPES = ['https://www.googleapis.com/auth/drive']

    def __init__(self, secrets_file: Path):
        self.secrets_file = secrets_file
        token_file = secrets_file.parent / 'token.pickle'
        creds = self.get_g_drive_credentials(token_file)
        self.service = build('drive', 'v3', credentials=creds)
        self.resource = self.service.files()

    def get_g_drive_credentials(self, token_file):
        creds = None
        # The file token.pickle stores the
        # user's access and refresh tokens. It is
        # created automatically when the authorization
        # flow completes for the first time.
        # Check if file token.pickle exists
        if token_file.exists():
            # Read the token from the file and
            # store it in the variable creds
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        # If no valid credentials are available,
        # request the user to log in.
        if not creds or not creds.valid:

            # If token is expired, it will be refreshed,
            # else, we will request a new one.
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(str(self.secrets_file), self.SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the access token in token.pickle
            # file for future usage
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def _get_folders(self, page_size: int = 10, name: str = None, exact: bool = False):
        query = "mimeType = 'application/vnd.google-apps.folder'"
        results = list()
        page_token = None
        params = dict()
        params['pageSize'] = page_size
        params['fields'] = 'nextPageToken, files(id, name, mimeType, kind, parents)'  # type: ignore
        params['q'] = query
        if name is not None:
            if exact:
                params['q'] = f"{query} and name = '{name}'"
            else:
                params['q'] = f"{query} and name contains '{name}'"

        while True:
            if page_token:
                params['pageToken'] = page_token

            result = self.resource.list(**params).execute()
            folders = result.get('files', [])
            results.extend(folders)
            page_token = result.get('nextPageToken')
            if page_token is None:
                break
        return results

    def _download_file(self, file_id: str, filename: str, folder: Path):
        try:
            request = self.resource.get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f'Download {int(status.progress() * 100)}.')

            download_file = folder / filename
            with open(download_file, 'wb') as binary_file:
                binary_file.write(file.getvalue())
            return download_file
        except HttpError as e:
            print(e)

    def get_folder(self, name: str):
        pass

    def list_files(self, folder_name: str, page_size: int = 100):
        folder = self._get_folders(name=folder_name, exact=True)
        folder_id = folder[0].get('id')
        query = f"'{folder_id}' in parents"
        result = self.resource.list(pageSize=page_size,
                                    fields="nextPageToken, files(id, name, mimeType, kind, parents)",
                                    q=query, ).execute()
        files = result.get('files', [])
        return files

    def upload(self, file_to_upload: Path, folder_id: str):
        filename = file_to_upload.name
        mime_type = 'application/octet-stream'
        body = {'name': filename, 'parents': [folder_id], 'mimeType': mime_type}
        try:
            media_body = MediaFileUpload(file_to_upload, mimetype=mime_type, chunksize=10485760, resumable=True)
            request = self.resource.create(body=body, media_body=media_body)  # Modified
            result = request.execute()
            return result
        except Exception as e:
            error_message = f'Upload error. Type {e.__class__.__name__} error {e}'
            raise UploadError(error_message)

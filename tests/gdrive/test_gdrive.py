from invoicing_tools.gdrive.gdrive import GDrive
from invoicing_tools.utils import quick_write


def test_list_folders(google_secrets_file):
    google_drive = GDrive(google_secrets_file)
    folder_list = google_drive.list_folders(name='EMR Facturas Scanned')
    assert len(folder_list['files']) == 1

    # raw_folder = {'raw_folder': folder_list['files'][0]}
    # quick_write(raw_folder, 'gdrive_data.json')


def test_list_files(google_secrets_file, app_configuration):
    folder_name = app_configuration['google_drive']['raw_folder']['name']
    google_drive = GDrive(google_secrets_file)
    file_list = google_drive.list_files(folder_name)
    assert len(file_list) > 0


def test_download_file(google_secrets_file, output_folder, raw_file_list):
    file_data = raw_file_list[0]
    file_id = file_data['id']
    name = file_data['name']
    google_drive = GDrive(google_secrets_file)
    out_file = google_drive._download_file(file_id, name, output_folder)
    assert out_file.exists()

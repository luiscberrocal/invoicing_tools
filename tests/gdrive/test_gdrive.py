from invoicing_tools.gdrive.gdrive import GDrive


def test_list_folders(google_secrets_file):
    google_drive = GDrive(google_secrets_file)
    folder_list = google_drive.list_folders(name='EMR Facturas Scanned')
    assert len(folder_list['files']) == 1
    quick_write

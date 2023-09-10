import json

from invoicing_tools.gdrive.builders import build_folder_db
from invoicing_tools.gdrive.db import FolderDatabase
from invoicing_tools.gdrive.gdrive import GDrive
from invoicing_tools.ocr import ocr_pdf_file


def test_folder_db(output_folder, google_secrets_file):
    file = output_folder / '_folders.json'
    with open(file, 'r') as j_file:
        folders = json.load(j_file)
    db_file = output_folder / '_luis_folder_db.json'
    db_file.unlink(missing_ok=True)

    results = build_folder_db(folders)
    folder_db = FolderDatabase(db_file)
    folder_db.update(results)
    print(folder_db.modified_on)
    # Get folder with raw invoices
    found = folder_db.find('/DGI/Facturas fiscales/Raw')
    assert len(found) == 1
    folder = found[0]

    drive = GDrive(google_secrets_file)
    # Get all files in folder
    files = drive.list_files_from_id(folder.id)
    # Download all files in folder
    downloaded_files = list()
    for f in files:
        file = drive.download_file_from_id(f['id'], f['name'], output_folder)
        # print(f'{file.name} {file.exists()}')
        downloaded_files.append(file)

    #OCR file
    ocr_texts = list()
    for df in downloaded_files:
        text = ocr_pdf_file(df)
        ocr_texts.append(text)
        print(text)

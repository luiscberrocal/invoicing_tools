import json

from invoicing_tools.gdrive.builders import build_folder_db
from invoicing_tools.gdrive.db import FolderDatabase


def test_folder_db(output_folder):
    file = output_folder / '_folders.json'
    with open(file, 'r') as j_file:
        folders = json.load(j_file)
    db_file = output_folder / '_luis_folder_db.json'
    results = build_folder_db(folders)
    folder_db = FolderDatabase(db_file)
    folder_db.update(results)
    old_folder = folder_db.get('/Old')
    print(old_folder)

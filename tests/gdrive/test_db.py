import json

from invoicing_tools.gdrive.builders import build_folder_db
from invoicing_tools.gdrive.db import FolderDatabase


def test_folder_db(output_folder):
    file = output_folder / '_folders.json'
    with open(file, 'r') as j_file:
        folders = json.load(j_file)
    db_file = output_folder / '_luis_folder_db.json'
    db_file.unlink(missing_ok=True)

    results = build_folder_db(folders)
    folder_db = FolderDatabase(db_file)
    folder_db.update(results)
    print(folder_db.modified_on)
    found = folder_db.find('/DGI/Facturas fiscales/Raw')
    for i, folder in enumerate(found):
        print(f'{i} {folder.full_path}')

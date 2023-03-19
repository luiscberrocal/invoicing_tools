import json

from invoicing_tools.gdrive.builders import build_fullpath_dict, build_folder_db


def test_build_fullpath_dict(output_folder):
    file = output_folder / '_folders.json'
    with open(file, 'r') as j_file:
        folders = json.load(j_file)

    results = build_folder_db(folders)
    for k, v in results.items():
        print(f'{k}: {v}')

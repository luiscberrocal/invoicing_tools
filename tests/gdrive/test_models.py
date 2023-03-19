import json

from invoicing_tools.gdrive.models import build_fullpath_dict, build_folder_db


def test_build_fullpath_dict(output_folder):
    file = output_folder / '_folders_smal.json'
    with open(file, 'r') as j_file:
        folders = json.load(j_file)

    results = build_folder_db(folders)
    for i, r in enumerate(results):
        print(r)
        if i > 5:
            break

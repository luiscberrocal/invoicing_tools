from typing import List, Optional, Any, Dict

from pydantic import BaseModel, Field, ValidationError


class GoogleDriveObject(BaseModel):
    kind: str
    mime_type: str = Field(alias='mimeType')
    parents: List[str]
    id: str
    name: str
    parent_folder = Optional['GoogleDriveObject']

    @property
    def is_folder(self):
        return self.mime_type == 'application/vnd.google-apps.folder'

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

def build_folder_objects(folders: List[Dict[str, Any]], ) -> Dict[str, GoogleDriveObject]:
    folder_dict = dict()
    for folder in folders:
        try:
            folder_dict[folder["id"]] = GoogleDriveObject(**folder)
        except ValidationError as e:
            print(f'Ignored forlder {folder["name"]}')
            # raise e
    return folder_dict


def get_ancestry(folder_dict: Dict[str, GoogleDriveObject], folder: GoogleDriveObject | None):
    ancestry = list()
    while True:
        if folder is None:
            ancestry.append('/')
            break
        else:
            ancestry.append(folder.name)
        grand_parent_id = folder.parents[0]
        grand_parent = folder_dict.get(grand_parent_id)
        prev = get_ancestry(folder_dict, grand_parent)
        ancestry.extend(prev)
    return ancestry


def build_fullpath_dict(folder_dict: Dict[str, GoogleDriveObject]) -> Dict[str, GoogleDriveObject]:
    new_folder_dict = dict()
    for id, folder in folder_dict.items():
        parent_id = folder.parents[0]
        parent = folder_dict.get(parent_id)
        folder.parent_folder = parent
        lineage = get_ancestry(folder_dict, folder)
        key = "/".join(lineage.reverse())
        new_folder_dict[key] = folder
    return new_folder_dict


def build_folder_db(folders: List[Dict[str, Any]]):
    folders_obj_dict = build_folder_objects(folders)
    fullpath_dict = build_fullpath_dict(folders_obj_dict)
    return fullpath_dict

import json
from datetime import datetime
from pathlib import Path
from typing import Dict

from invoicing_tools.codec import ModelDecoder, ModelEncoder
from invoicing_tools.gdrive.models import GoogleDriveObject


class FolderDatabase:

    def __init__(self, db_file: Path):
        self.db_file = db_file
        if self.db_file.exists():
            with open(self.db_file, 'r') as json_file:
                self.db = json.load(json_file, cls=ModelDecoder)

            modified = self.db_file.stat().st_mtime
            self.modified_on = datetime.fromtimestamp(modified)


    def get(self, path: str) -> GoogleDriveObject:
        return self.db.get(path)

    def update(self, folders: Dict[str, GoogleDriveObject]):
        with open(self.db_file, 'w') as json_file:
            json.dump(json_file, folders, cls=ModelEncoder)
        self.db = folders

    def exists(self) -> bool:
        return self.db_file.exists()







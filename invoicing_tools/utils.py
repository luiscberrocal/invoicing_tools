import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Union, Dict, Any, List

from invoicing_tools.exceptions import InvoicingToolsException


def quick_json_write(data: Union[Dict[str, Any], List[Dict[str, Any]]], file: str, output_folder: Path,
                     over_write: bool = True):
    def quick_serialize(value):
        return f'{value}'

    filename = output_folder / file

    if (filename.exists() and over_write) or not filename.exists():
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4, default=quick_serialize)
        return filename


def quick_write(data: Union[Dict[str, Any], List[Dict[str, Any]]], file: str, output_subfolder: str = None,
                over_write: bool = True):
    output_folder = Path(__file__).parent.parent / 'output'
    if not output_folder.exists():
        raise Exception(f'Output folder not found {output_folder}')
    if output_subfolder is None:
        folder = output_folder
    else:
        folder = output_folder / output_subfolder
    filename = quick_json_write(data, file, folder, over_write=over_write)
    return filename


def backup_file(filename: Path, backup_folder: Path, add_version: bool = True) -> Path:
    if not backup_folder.is_dir():
        error_message = f'Backup folder has to be a folder.' \
                        f' Supplied: {backup_folder}. Type: {type(backup_folder)}'
        raise InvoicingToolsException(error_message)

    datetime_format = '%Y%m%d_%H%M%S'
    if add_version:
        from . import __version__ as current_version
        version_val = f'v{current_version}_'
    else:
        version_val = ''
    timestamp = datetime.now().strftime(datetime_format)
    backup_filename = backup_folder / f'{timestamp}_{version_val}{filename.name}'
    shutil.copy(filename, backup_filename)
    return backup_filename

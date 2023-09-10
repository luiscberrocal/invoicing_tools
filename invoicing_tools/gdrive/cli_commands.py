from datetime import datetime
from pathlib import Path

import click
from rich.pretty import pprint

from invoicing_tools import CONFIGURATION_MANAGER
from invoicing_tools.gdrive.gdrive import GDrive


@click.command()
@click.option('-f', '--folder-id', help='Google drive directory id', required=False)
@click.option('-df', '--date_filter', help='Date filter', required=False)
def list_files(folder_id: str, date_filter: str):
    config = CONFIGURATION_MANAGER.get_configuration()
    # pprint(config)
    secrets_file = Path(config['google']['secrets_file']['filename'])
    if folder_id is None:
        folder_id = config['google']['raw_folder']['id']
    if date_filter is not None and date_filter.lower() == 'today':
        date_filter = datetime.today().strftime('%Y%m%d')
        print(date_filter)

    # pprint(f'{folder_id = }')
    # pprint(secrets_file)
    gdrive = GDrive(secrets_file=secrets_file)
    files = gdrive.list_files_from_id(folder_id=folder_id)
    for i, file in enumerate(files):
        filename = file["name"]
        if date_filter in filename:
            print(f'{i} {filename}')

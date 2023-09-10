import click
from rich.pretty import pprint

from invoicing_tools import CONFIGURATION_MANAGER


@click.command()
@click.option('-f', '--folder-id', help='Google drive directory id', required=False)
def list_files(folder_id: str):
    config = CONFIGURATION_MANAGER.get_configuration()
    if folder_id is None:
        folder_id = config['google']['raw_folder']['id']

    pprint(f'{folder_id = }')

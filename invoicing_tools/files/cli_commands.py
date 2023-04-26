import os
import re
import webbrowser
from pathlib import Path
from typing import List

import click

from invoicing_tools import CONFIGURATION_MANAGER
from invoicing_tools.naming import rename_fiscal_invoice_with_short_name


@click.command()
@click.option('-d', '--directory', help='Folder with the scanned invoices.', type=click.Path(exists=True))
def rename(directory: Path):
    pattern = re.compile(r'Scanned_\d{8}-\d{4}\.(pdf|PDF)')
    # pattern = re.compile(r'Fact.+\.(pdf|PDF)')
    files_to_rename: List[Path] = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if pattern.match(file):
                files_to_rename.append(Path(root) / file)
                # click.secho(f'{file}', fg='blue')
    for idx, r_file in enumerate(files_to_rename, 1):
        click.secho(f'{idx} {r_file.parent}/{r_file.name}', fg='yellow')
    file_num = click.prompt('Select file to rename')
    file_to_rename = files_to_rename[int(file_num) - 1]
    webbrowser.open_new_tab(str(file_to_rename))

    invoice_number = click.prompt('Invoice number', type=int)
    # amount = click.prompt('Amount')
    date_invoiced = click.prompt('Date', type=click.types.DateTime(('%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M')))
    client_short_name = click.prompt('Client short name')
    process_folder = Path(CONFIGURATION_MANAGER.get_configuration()['application']['processed_folder']['folder'])
    # print(f'>>>> {process_folder}')

    taget_file = rename_fiscal_invoice_with_short_name(short_name=client_short_name, invoice_number=invoice_number,
                                                       invoice_date=date_invoiced,
                                                       target_folder=process_folder, pdf_file=file_to_rename)
    click.secho(f'Created new file {taget_file}')

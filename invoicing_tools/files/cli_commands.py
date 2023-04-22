import os
import re
import webbrowser
from pathlib import Path
from typing import List

import click


@click.command()
@click.option('-d', '--directory', help='Folder with the scanned invoices.', type=click.Path(exists=True))
def rename(directory: Path):
    pattern = re.compile(r'Scanned_\d{8}-\d{4}\.(pdf|PDF)')
    files_to_rename: List[Path] = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if pattern.match(file):
                files_to_rename.append(Path(root) / file)
                # click.secho(f'{file}', fg='blue')
    for idx, file in enumerate(files_to_rename, 1):
        click.secho(f'{idx} {file.name}', fg='yellow')
    file_num = click.prompt('Select file to rename')
    file_to_rename = files_to_rename[int(file_num) - 1]
    webbrowser.open_new_tab(str(file_to_rename))

    invoice_number = click.prompt('Invoice number')
    amount = click.prompt('Amount')
    date_invoiced = click.prompt('Date')
    client_short_name = click.prompt('Client short name')


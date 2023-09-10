import os
import webbrowser
from pathlib import Path
from typing import List, Any, Dict

import click
from rich.pretty import pprint

from invoicing_tools.naming import get_invoice_info_from_filename


@click.command()
@click.option('-d', '--directory', type=click.Path(exists=True))
def email(directory: Path):
    files_to_email: List[Dict[str, Any]] = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            short_name, invoice_number = get_invoice_info_from_filename(file)
            if invoice_number != 0:
                invoice_dict = {'file': Path(root) / file,
                                'short_name': short_name,
                                'invoice_number': invoice_number}
                files_to_email.append(invoice_dict)
                # click.secho(f'{file}', fg='blue')
    for idx, r_file in enumerate(files_to_email, 1):
        click.secho(f'{idx} {r_file["file"].parent}/{r_file["file"].name}', fg='yellow')
    file_num = click.prompt('Select file to rename', type=int)
    file_data_to_email = files_to_email[file_num - 1]
    # print(Path(file_to_email))
    fn: Path = file_data_to_email['file']
    webbrowser.open_new_tab(str(fn.absolute()))

import os
import webbrowser
from pathlib import Path
from typing import List, Any, Dict

import click

from invoicing_tools.naming import get_invoice_info


@click.command()
@click.option('-d', '--directory', type=click.Path(exists=True))
def email(directory: Path):
    files_to_email: List[Dict[str, Any]] = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            short_name, invoice_number = get_invoice_info(file)
            if invoice_number != 0:
                invoice_dict = {'file': Path(root) / file,
                                'short_name': short_name,
                                'invoice_number': invoice_number}
                files_to_email.append(invoice_dict)
                # click.secho(f'{file}', fg='blue')
    for idx, r_file in enumerate(files_to_email, 1):
        click.secho(f'{idx} {r_file["file"].parent}/{r_file["file"].name}', fg='yellow')
    file_num = click.prompt('Select file to rename')
    file_to_email = files_to_email[int(file_num) - 1]
    webbrowser.open_new_tab(str(file_to_email))

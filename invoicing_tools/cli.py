"""Console script for invoicing_tools."""
import sys
from pathlib import Path

import click

from invoicing_tools.files.cli_commands import rename
from .invoices import ReportWriter


@click.group()
def main(args=None):
    """Console script for invoicing_tools."""
    pass
    #writer = ReportWriter(Path('./'))
    #data = {'client_name': 'Tesla Motors, Inc.', 'client_ruc': '123-89-0900'}
    #output_file = Path('./output') / 'invoice.html'
    #writer.write('invoice_template.html', output_file, **data)
    #return 0


main.add_command(rename)
if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

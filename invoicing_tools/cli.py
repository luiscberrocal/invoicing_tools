"""Console script for invoicing_tools."""
import sys
from pathlib import Path

import click

from .invoices import ReportWriter


@click.command()
def main(args=None):
    """Console script for invoicing_tools."""
    writer = ReportWriter(Path('./'))
    data = {'client_name': 'Tesla Motors, Inc.', 'client_ruc': '123-89-0900'}
    output_file = Path('./output') / 'invoice.html'
    writer.write('invoice_template.html', output_file, **data)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

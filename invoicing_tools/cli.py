"""Console script for invoicing_tools."""
import sys

import click

from invoicing_tools.email.cli_commands import email
from invoicing_tools.files.cli_commands import rename

from invoicing_tools.gdrive.cli_commands import list_files
@click.group()
def main(args=None):
    """Console script for invoicing_tools."""
    pass
    # writer = ReportWriter(Path('./'))
    # data = {'client_name': 'Tesla Motors, Inc.', 'client_ruc': '123-89-0900'}
    # output_file = Path('./output') / 'invoice.html'
    # writer.write('invoice_template.html', output_file, **data)
    # return 0


main.add_command(rename)
main.add_command(email)
main.add_command(list_files)
if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

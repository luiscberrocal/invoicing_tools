import sys
from pathlib import Path

import click
import jinja2


class ReportWriter:

    def __init__(self, template_path: Path, ):
        template_loader = jinja2.FileSystemLoader(searchpath=template_path)
        self.template_env = jinja2.Environment(loader=template_loader)

    def write(self, template_name: str, output_file: Path, **params):
        template = self.template_env.get_template(template_name)
        output = template.render(**params)
        with open(output_file, 'w') as html_file:
            html_file.write(output)


@click.command()
def main(args=None):
    """Console script for invoicing_tools."""
    writer = ReportWriter(Path('./'))
    data = {'client_name': 'Tesla Motors, Inc.', 'client_ruc': '123-89-0900'}
    output_file = Path('../output') / 'invoice.html'
    writer.write('invoice_template.html', output_file, **data)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

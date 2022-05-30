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
    data = {'client': {'name': 'Tesla Motors, Inc.', 'ruc': '123-89-0900'},
            'invoice': {'number': 1455, 'due_date': '12-may-2022', 'total': 200.00},
            'items': [{'id': 1, 'description': 'Mantenimiento de software en nube Marzo-2022',
                       'quantity': 1, 'unit_price': 200.00, 'total': 200.00}]}
    output_file = Path('../output') / 'invoice.html'
    template_name = 'invoice_template_bs5.html'
    writer.write(template_name, output_file, **data)
    print(f'Template writte: {template_name}')
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

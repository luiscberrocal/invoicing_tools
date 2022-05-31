import sys
from pathlib import Path

import click
import jinja2
import pdfkit


class ReportWriter:

    def __init__(self, template_path: Path, ):
        template_loader = jinja2.FileSystemLoader(searchpath=template_path)
        self.template_env = jinja2.Environment(loader=template_loader)

    def write(self, template_name: str, output_file: Path, **params):
        template = self.template_env.get_template(template_name)
        output = template.render(**params)
        with open(output_file, 'w') as html_file:
            html_file.write(output)


def html2pdf(html_path: Path, pdf_path: Path):
    """
    Convert html to pdf using pdfkit which is a wrapper of wkhtmltopdf
    """
    options = {
        'page-size': 'Letter',
        'margin-top': '0.35in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None
    }
    with open(html_path, 'r') as f:
        pdfkit.from_file(f, pdf_path, options=options)


@click.command()
def main(args=None):
    """Console script for invoicing_tools."""
    writer = ReportWriter(Path('./'))
    data = {'client': {'name': 'Tesla Motors, Inc.', 'ruc': '123-89-0900'},
            'invoice': {'number': 1455, 'due_date': '12-may-2022', 'total': '200.00',
                        'sub_total': '200.00', 'discount': '0.00'},
            'items': [{'id': 1, 'description': 'Mantenimiento de software en nube Marzo-2022',
                       'quantity': 1, 'unit_price': '200.00', 'total': '200.00'}]}
    output_file = Path('../output') / 'invoice.html'
    pdf_output_file = Path('../output') / 'invoice.pdf'
    template_name = 'invoice_template_bs5.html'
    writer.write(template_name, output_file, **data)
    html2pdf(output_file, pdf_output_file)
    print(f'Template written: {template_name}')
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

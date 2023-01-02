from pathlib import Path

from invoicing_tools.models import FiscalInvoice


def rename_fiscal_invoice(invoice: FiscalInvoice, pdf_file: Path, target_folder: Path, prefix: str = 'FFiscal'):
    sep = '-'
    company = ''
    target_filename = f'{prefix}{sep}{invoice.company}'

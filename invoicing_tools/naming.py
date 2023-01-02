import shutil
from pathlib import Path

from invoicing_tools.db.managers import JSONDatabase
from invoicing_tools.models import FiscalInvoice


def rename_fiscal_invoice(invoice: FiscalInvoice, database: JSONDatabase, pdf_file: Path, target_folder: Path,
                          prefix: str = 'FFiscal'):
    sep = '-'
    company = database.get_person(invoice.ruc)
    target_filename = f'{prefix}{sep}{company.short_name}{sep}{invoice.number:04}{sep}{pdf_file.suffix}'
    full_target_file = target_folder / target_filename
    shutil.copy(pdf_file, full_target_file)



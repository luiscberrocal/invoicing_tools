import shutil
from pathlib import Path

from invoicing_tools.db.managers import JSONDatabase
from invoicing_tools.models import FiscalInvoice


def rename_fiscal_invoice(invoice: FiscalInvoice, database: JSONDatabase, pdf_file: Path, target_folder: Path,
                          prefix: str = 'FFiscal') -> Path:
    company = database.get_person(invoice.ruc)
    short_name = company.short_name
    invoice_number = invoice.number
    target_file = rename_fiscal_invoice_with_short_name(short_name=short_name,
                                                        invoice_number=invoice_number, pdf_file=pdf_file,
                                                        target_folder=target_folder,
                                                        prefix=prefix)
    return target_file


def rename_fiscal_invoice_with_short_name(short_name: str, invoice_number: int, pdf_file: Path,
                                          target_folder: Path, prefix: str = 'FFiscal',
                                          delete_original: bool = True) -> Path:
    sep = '-'
    target_filename = f'{prefix}{sep}{short_name}{sep}{invoice_number:04}{sep}{pdf_file.suffix}'
    full_target_file = target_folder / target_filename
    shutil.copy(pdf_file, full_target_file)
    if delete_original:
        pdf_file.unlink()
    return full_target_file

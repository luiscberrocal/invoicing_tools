import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Tuple

from invoicing_tools.db.managers import JSONDatabase
from invoicing_tools.models import FiscalInvoice
import logging

logger = logging.getLogger(__name__)

def rename_fiscal_invoice(invoice: FiscalInvoice, database: JSONDatabase, pdf_file: Path, target_folder: Path,
                          invoice_date: datetime,
                          prefix: str = 'FFiscal') -> Path:
    company = database.get_person(invoice.ruc)
    short_name = company.short_name
    invoice_number = invoice.number
    target_file = rename_fiscal_invoice_with_short_name(short_name=short_name,
                                                        invoice_number=invoice_number, pdf_file=pdf_file,
                                                        invoice_date=invoice_date,
                                                        target_folder=target_folder,
                                                        prefix=prefix)
    return target_file


def rename_fiscal_invoice_with_short_name(*, short_name: str, invoice_number: int, pdf_file: Path,
                                          invoice_date: datetime,
                                          target_folder: Path, prefix: str = 'FFiscal',
                                          delete_original: bool = True) -> Path:
    if not target_folder.exists():
        logger.warning(f'Target folder does not exist {target_folder}. Creating')
        target_folder.mkdir()

    sep = '-'
    timestamp = invoice_date.strftime('%Y%m%d-%H%M')
    target_filename = f'{prefix}{sep}{short_name}{sep}{invoice_number:04}{sep}{timestamp}{pdf_file.suffix}'
    print(target_filename)
    full_target_file = target_folder / target_filename
    shutil.copy(pdf_file, full_target_file)
    if delete_original:
        pdf_file.unlink()
    return full_target_file


def get_invoice_info_from_filename(filename: str) -> Tuple[str, int]:
    regexp = re.compile(r"^FFiscal-(?P<client>[A-Z]+)-(?P<invoice>\d+)-\d{8}-\d{4}\.pdf$")
    match = regexp.match(filename)
    if match:
        return match.group('client'), int(match.group('invoice'))
    else:
        return '', 0

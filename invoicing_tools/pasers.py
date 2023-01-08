import json
import re
import webbrowser
from datetime import datetime
from pathlib import Path
from re import Pattern
from typing import List, Dict, Any, Tuple

from invoicing_tools.models import FiscalInvoice


def parse_for_data(lines: List[str], pattern: Pattern, pattern_names: List[str]) -> Dict[str, Any]:
    for i, line in enumerate(lines, 1):
        match = pattern.match(line)
        if match:
            results = dict()
            for pattern_name in pattern_names:
                results[pattern_name] = match.group(pattern_name)
            results['line_number'] = i
            return results


def fiscal_invoice_line_parser(lines: List[str]) -> Dict[str, Any]:
    invoice_regex = re.compile(r"FACTURA:\s(?P<machine>[A-Z0-9]+)-(?P<invoice>\d+)")
    date_regex = re.compile(r"FECHA:\s(?P<day>\d{2})/(?P<month>\d{2})/(?P<year>\d{4})\s"
                            r"(?P<hour>\d{2}):(?P<minute>\d{2})")
    ruc_regex = re.compile(r"RUC/CIP:\s(?P<ruc>[0-9\-]+)")
    amount_regex = re.compile(r"(?:TOTAL|EFECTIVO)\sB/\.(?P<amount>[\d,\.]+)")
    company_regex = re.compile(r"RAZON\sSOCIAL:\s(?P<company>.+)")

    fiscal_invoice = dict()
    fiscal_invoice['invoice'] = parse_for_data(lines, invoice_regex, ['machine', 'invoice'])
    fiscal_invoice['date'] = parse_for_data(lines, date_regex, ['day', 'month', 'year', 'hour', 'minute'])
    fiscal_invoice['ruc'] = parse_for_data(lines, ruc_regex, ['ruc'])
    fiscal_invoice['company'] = parse_for_data(lines, company_regex, ['company'])
    fiscal_invoice['amount'] = parse_for_data(lines, amount_regex, ['amount'])
    return fiscal_invoice


def parse_invoice_text_file(txt_file: Path) -> Dict[str, Any]:
    with open(txt_file, 'r') as txt:
        lines = txt.readlines()
    fiscal_invoice = fiscal_invoice_line_parser(lines)
    return fiscal_invoice


def save_invoice_data_to_file(txt_file: Path, json_file: Path = None):
    fiscal_invoice = parse_invoice_text_file(txt_file)
    if json_file is None:
        json_file = txt_file.parent / f'{txt_file.stem}.json'
    with open(json_file, 'w') as j_file:
        json.dump(fiscal_invoice, j_file)


def update_missing_invoice_data(folder: Path):
    json_files = folder.glob('**/*.json')
    defaults = {'invoice': {'machine': '', 'invoice': ''}, 'date': {'date': ''},
                'ruc': {'ruc': ''}, 'company': {'company': ''}, 'amount': {'amount': ''}}
    for json_file in json_files:
        with open(json_file, 'r') as j_file:
            invoice_data = json.load(j_file)
        open_image = False
        for data_field in defaults.keys():
            if invoice_data.get(data_field) is None:
                if not open_image:
                    jpeg_file = json_file.parent / f'{json_file.stem}.jpg'
                    print('Opening image in browser')
                    webbrowser.open(str(jpeg_file))
                    open_image = True
                for key, item in defaults[data_field].items():
                    default = item
                    val = input(f'{key} for {json_file.stem}.jpg [{default}]')
                    if invoice_data.get(data_field) is None:
                        invoice_data[data_field] = dict()
                    if val == '':
                        val = item
                    invoice_data[data_field][key] = val
                    if key not in ['date', 'invoice']:
                        defaults[data_field][key] = val

        with open(json_file, 'w') as j_file:
            json.dump(invoice_data, j_file, indent=4)
    defaults_file = folder / '_defaults.json'
    with open(defaults_file, 'w') as j_file:
        json.dump(defaults, j_file)


def parse_date(date_data: Dict[str, Any]) -> datetime:
    if date_data.get('date'):
        date = datetime.strptime(date_data['date'], '%Y-%m-%d %H:%M')
        return date
    else:
        year = int(date_data['year'])
        month = int(date_data['month'])
        day = int(date_data['day'])
        hour = int(date_data['hour'])
        minute = int(date_data['minute'])
        date = datetime(year, month, day, hour, minute)
        return date


def json_file_to_model(json_file: Path) -> FiscalInvoice:
    with open(json_file, 'r') as j_file:
        invoice_data = json.load(j_file)
    invoice_dict = dict()
    invoice_dict['number'] = invoice_data['invoice']['invoice']
    invoice_dict['date'] = parse_date(invoice_data['date'])
    invoice_dict['ruc'] = invoice_data['ruc']['ruc']
    invoice_dict['company'] = invoice_data['company']['company']
    invoice_dict['amount'] = invoice_data['amount']['amount'].replace(',', '')
    fiscal_invoice = FiscalInvoice(**invoice_dict)
    return fiscal_invoice


if __name__ == '__main__':
    mfolder = Path('/home/luiscberrocal/PycharmProjects/invoicing_tools/'
                   'output/invoices_to_process')
    update_missing_invoice_data(mfolder)

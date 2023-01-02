import json
import re

from invoicing_tools.pasers import fiscal_invoice_line_parser, parse_invoice_text_file


def test_parse():
    company_regex = re.compile(r"RAZON\sSOCIAL:\s(?P<company>.+)")
    company = 'RAZON SOCIAL: MULTI-ESPECIALIDAD d2'
    match = company_regex.match(company)
    assert len(match.groups()) == 1


def test_parse_fiscal_invoice(output_folder):
    txt_file = output_folder / 'Fact-007_20220329-1811.txt'
    with open(txt_file, 'r') as txt:
        lines = txt.readlines()
    invoice_data = fiscal_invoice_line_parser(lines)
    assert len(lines) == 1


def test_parse_files(output_folder):
    folder = output_folder / 'invoices_to_process'
    txt_files = folder.glob('**/*.txt')
    for txt_file in txt_files:
        json_file = folder / f'{txt_file.stem}.json'
        invoice_data = parse_invoice_text_file(txt_file)
        with open(json_file, 'w') as j_file:
            json.dump(invoice_data, j_file)


import json
import re

from invoicing_tools.db.managers import JSONDatabase
from invoicing_tools.pasers import fiscal_invoice_line_parser, parse_invoice_text_file, json_file_to_model


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


def test_json_file_to_mode(fixtures_folder):
    json_file = fixtures_folder / 'fiscal_invoice_manual.json'
    fiscal_invoice = json_file_to_model(json_file)
    assert fiscal_invoice.company == 'CMMI'
    assert fiscal_invoice.amount == 200.00
    assert fiscal_invoice.number == 6


def test_json_file_to_model2(fixtures_folder):
    json_file = fixtures_folder / 'fiscal_invoice_ocr_date.json'
    fiscal_invoice = json_file_to_model(json_file)
    assert fiscal_invoice.company == 'CMMI'
    assert fiscal_invoice.amount == 2000.00
    assert fiscal_invoice.number == 1


def test_populate_data(envs_folder, output_folder):
    folder = output_folder / 'invoices_to_process'
    json_files = folder.glob('**/*.json')
    db_file = envs_folder / 'json_db2.json'
    database = JSONDatabase(db_file)
    for json_file in json_files:
        invoice = json_file_to_model(json_file)
        database.add_fiscal_invoice(invoice)
        database.save()

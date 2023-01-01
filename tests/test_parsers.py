import re

from invoicing_tools.pasers import fiscal_invoice_line_parser


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

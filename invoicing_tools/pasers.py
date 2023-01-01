import re
from re import Pattern
from typing import List, Dict, Any, Tuple


def parse_for_data(lines: List[str], pattern: Pattern, pattern_names:List[str]) -> Dict[str, Any]:
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
                            r"(?P<hour>\d{2}:(?P<minute>\d{2}))")
    ruc_regex = re.compile(r"RUC/CIP:\s(?P<ruc>[0-9\-]+)")
    company_regex = re.compile(r"RAZON\sSOCIAL:\s(?P<company>.+)")
    fiscal_invoice = dict()
    fiscal_invoice['invoice'] = parse_for_data(lines, invoice_regex, ['machine', 'invoice'])
    fiscal_invoice['date'] = parse_for_data(lines, date_regex, ['day', 'month', 'year', 'hour', 'minute'])
    fiscal_invoice['ruc'] = parse_for_data(lines, ruc_regex, ['ruc'])
    fiscal_invoice['company'] = parse_for_data(lines, company_regex, ['company'])
    return fiscal_invoice

import json
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel

from invoicing_tools.models import JurisPerson, FiscalInvoice


class ModelEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, BaseModel):
            object_data = obj.dict()
            object_data['__extended_json_type__'] = obj.__class__.__name__
            return object_data
        elif isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M')
        else:
            return json.JSONEncoder.default(obj)


class JSONDatabase:
    PERSON_TABLE = 'persons'
    INVOICE_TABLE = 'invoices'

    def __init__(self, db_file: Path):
        self.db_file = db_file
        self.database = dict()

    def load_data(self):
        with open(self.db_file, 'r') as json_file:
            self.database = json.load(json_file)

    def get_person(self, ruc: str):
        return self.database[self.PERSON_TABLE].get(ruc)

    def get_invoices(self, number: str):
        return self.database[self.INVOICE_TABLE].get(number)

    def add_person(self, person: JurisPerson):
        if not self.database.get(self.PERSON_TABLE):
            self.database[self.PERSON_TABLE] = dict()

        person_in_db = self.database[self.PERSON_TABLE].get(person.ruc)
        if person_in_db is None:
            self.database[self.PERSON_TABLE][person.ruc] = person
        else:
            raise Exception(f'Person with ruc {person.ruc} already exists {person.name}')

    def add_fiscal_invoice(self, invoice: FiscalInvoice):
        if not self.database.get(self.INVOICE_TABLE):
            self.database[self.INVOICE_TABLE] = dict()

        in_db = self.database[self.INVOICE_TABLE].get(invoice.number)
        if in_db is None:
            self.database[self.INVOICE_TABLE][invoice.number] = invoice
        else:
            raise Exception(f'There is an existing invoice with number {invoice.number}')

    def save(self):
        with open(self.db_file, 'w') as json_file:
            json.dump(self.database, json_file, cls=ModelEncoder)

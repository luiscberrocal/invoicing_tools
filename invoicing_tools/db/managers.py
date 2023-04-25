import json
from json import JSONDecodeError
from pathlib import Path

from sqlmodel import create_engine, SQLModel

from invoicing_tools.codec import ModelEncoder, ModelDecoder
from invoicing_tools.models import JurisPerson, FiscalInvoice


class JSONDatabase:
    PERSON_TABLE = 'persons'
    INVOICE_TABLE = 'invoices'

    def __init__(self, db_file: Path):
        self.db_file = db_file
        self.database = dict()
        self.load_data()
        if not self.database.get(self.PERSON_TABLE):
            self.database[self.PERSON_TABLE] = dict()
        if not self.database.get(self.INVOICE_TABLE):
            self.database[self.INVOICE_TABLE] = dict()

    def load_data(self):
        try:
            with open(self.db_file, 'r') as json_file:
                self.database = json.load(json_file, cls=ModelDecoder)
        except JSONDecodeError:
            pass

    def get_person(self, ruc: str):
        return self.database[self.PERSON_TABLE].get(ruc)

    def get_invoices(self, number: str):
        return self.database[self.INVOICE_TABLE].get(number)

    def list_persons(self):
        object_list = list()
        for key, item in self.database[self.PERSON_TABLE].items():
            object_list.append(item)
        return object_list

    def add_person(self, person: JurisPerson):
        person_in_db = self.database[self.PERSON_TABLE].get(person.ruc)
        if person_in_db is None:
            self.database[self.PERSON_TABLE][person.ruc] = person
        else:
            raise Exception(f'Person with ruc {person.ruc} already exists {person.name}')

    def add_fiscal_invoice(self, invoice: FiscalInvoice):

        in_db = self.database[self.INVOICE_TABLE].get(invoice.number)
        if in_db is None:
            self.database[self.INVOICE_TABLE][invoice.number] = invoice
        else:
            raise Exception(f'There is an existing invoice with number {invoice.number}')

    def save(self):
        with open(self.db_file, 'w') as json_file:
            json.dump(self.database, json_file, cls=ModelEncoder)


class InvoiceDatabase:

    def __init__(self, source_file: Path):
        sqlite_url = f"sqlite:///{source_file}"

        self.engine = create_engine(sqlite_url, echo=True)
        SQLModel.metadata.create_all(self.engine)




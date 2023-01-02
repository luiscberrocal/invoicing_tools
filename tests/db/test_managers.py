import json
from datetime import datetime

from pydantic import BaseModel

from invoicing_tools.db.managers import JSONDatabase
from invoicing_tools.models import JurisPerson, FiscalInvoice




class TestJSONDatabase:

    def test_add_person(self, output_folder):
        db_file = output_folder / '_json_db.json'
        person = JurisPerson(short_name='CMMA', name='Super company', ruc='855-888-888', dv='66')
        database = JSONDatabase(db_file)
        database.add_person(person)
        database.save()
        assert db_file.exists()

    def test_add_invoice(self, output_folder):
        db_file = output_folder / '_json_db.json'
        invoice = FiscalInvoice(number=1, date=datetime.now(), ruc='555-888-999',
                                company='Super company', amount=200.25)
        database = JSONDatabase(db_file)
        database.add_fiscal_invoice(invoice)
        database.save()
        assert db_file.exists()

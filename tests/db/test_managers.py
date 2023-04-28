from datetime import datetime
from pathlib import Path

from sqlmodel import Session

from invoicing_tools.db.managers import JSONDatabase, InvoiceDatabase
from invoicing_tools.db.models import Client
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

    def test_add_all(self, output_folder):
        db_file = output_folder / '_json_db2.json'
        person = JurisPerson(short_name='CMMA', name='Super company', ruc='855-888-888', dv='66')
        person2 = JurisPerson(short_name='MGI', name='Acountants', ruc='4444-888-888', dv='66')
        invoice = FiscalInvoice(number=1, date=datetime.now(), ruc=person.ruc,
                                company=person.name, amount=200.25)
        database = JSONDatabase(db_file)
        database.add_person(person)
        database.add_person(person2)
        database.add_fiscal_invoice(invoice)
        database.save()
        assert db_file.exists()

    def test_list_person(self, output_folder):
        db_file = output_folder / '_json_db2.json'
        database = JSONDatabase(db_file)
        persons = database.list_persons()
        assert len(persons) == 2
        assert persons[0].short_name == 'CMMA'

    def test_empty_db(self, fixtures_folder):
        db_file = fixtures_folder / 'empty_db.json'
        database = JSONDatabase(db_file)
        assert len(database.list_persons()) == 0

    def test_configuration(self, app_config):
        database_file = Path(app_config['database']['db_file']['filename'])
        assert database_file.exists()


class TestInvoiceDatabase:

    def test_create_table(self, output_folder):
        client = Client(short_name='JEDI', name='Jedi Council', ruc='1554-55-445-5555',
                        dv='45', emails="['obiwan@jedi.org']")
        db_file = output_folder / 'test_db.sqlite'
        db = InvoiceDatabase(db_file)

        with Session(db.engine) as session:
            session.add(client)
            session.commit()

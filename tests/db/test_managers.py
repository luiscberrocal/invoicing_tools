from invoicing_tools.db.managers import JSONDatabase
from invoicing_tools.models import JurisPerson


class TestJSONDatabase:

    def test_add_person(self, output_folder):
        db_file = output_folder / '_json_db.json'
        person = JurisPerson(short_name='CMMA', name='Super company', ruc='855-888-888', dv='66')
        database = JSONDatabase(db_file)
        database.add_person(person)
        database.save()
        assert db_file.exists()

import json
from pathlib import Path

from invoicing_tools.models import JurisPerson


class JSONDatabase:
    PERSON_TABLE = 'persons'

    def __init__(self, db_file: Path):
        self.db_file = db_file
        self.database = dict()

    def add_person(self, person: JurisPerson):
        if not self.database.get(self.PERSON_TABLE):
            self.database[self.PERSON_TABLE] = dict()

        person_in_db = self.database[self.PERSON_TABLE].get(person.ruc)
        if person_in_db is None:
            self.database[self.PERSON_TABLE][person.ruc] = person
        else:
            raise Exception(f'Person with ruc {person.ruc} already exists {person.company}')

    def save(self):
        with open(self.db_file, 'w') as json_file:
            json.dump(self.database, json_file, default=lambda x: x.dict())


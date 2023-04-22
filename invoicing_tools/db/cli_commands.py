import click

from invoicing_tools.db.managers import JSONDatabase

OBJECT_TYPE_OPTIONS = [JSONDatabase.PERSON_TABLE, JSONDatabase.INVOICE_TABLE]


def database():
    pass


@click.command()
@click.option('-ot', '--object-type', help='Type of object to add', required=False,
              type=click.Choice(OBJECT_TYPE_OPTIONS))
def add(object_type: str):
    if object_type == JSONDatabase.INVOICE_TABLE:
        pass
    else:
        raise Exception('Unsupported')

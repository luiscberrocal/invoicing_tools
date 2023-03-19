import json
from datetime import datetime

from pydantic import BaseModel

from invoicing_tools.gdrive.models import GoogleDriveObject
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


class ModelDecoder(json.JSONDecoder):
    def __init__(self, **kwargs):
        kwargs["object_hook"] = self.object_hook
        super().__init__(**kwargs)

    def object_hook(self, obj):
        if isinstance(obj, dict):
            json_type = obj.get('__extended_json_type__')
            if json_type == 'JurisPerson':
                new_obj = JurisPerson(**obj)
                return new_obj
            elif json_type == 'FiscalInvoice':
                new_obj = FiscalInvoice(**obj)
                return new_obj
            elif json_type == 'GoogleDriveObject':
                new_obj = GoogleDriveObject(**obj)
                return new_obj
            else:
                return obj
        else:
            return obj

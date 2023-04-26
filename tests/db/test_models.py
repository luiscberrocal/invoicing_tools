
def test_write_schemas(output_folder):
    import json
    from csv import DictWriter
    import importlib
    import re

    package_name = 'invoicing_tools.db.models'
    obj_name = 'Client'

    mymodule = importlib.import_module(package_name)
    obj = getattr(mymodule, obj_name)  # eval(obj_name)
    use_alias = False
    schema_str = obj.schema_json(indent=4, by_alias=use_alias)
    class_fields = obj.__fields__
    filename = output_folder / f'_{obj_name}_use_alias_{use_alias}.json'
    with open(filename, 'w') as f:
        f.write(schema_str)

    schema_dict = json.loads(schema_str)

    ref_regex = re.compile("#/definitions/(?P<reference>\w+)")
    property_list = []
    for name, attr in schema_dict['properties'].items():
        property_dict = {'name': name}
        alias = class_fields.get(name).alias
        property_dict['alias'] = alias
        if attr.get('$ref'):
            match = ref_regex.match(attr.get('$ref'))
            if match:
                reference = match.group('reference')
                definition = schema_dict['definitions'][reference]
                property_dict['title'] = definition.get('title')
                property_dict['type'] = definition.get('type')
                if definition.get('enum'):
                    desc = definition.get('description')
                    property_dict['description'] = f'{desc}. Valid values {", ".join(definition["enum"])}'
                    property_dict['type'] = f'Enum({definition.get("type")})'
                else:
                    property_dict['type'] = definition.get('type')

                    property_dict['description'] = definition.get('description')
        else:
            property_dict['title'] = attr.get('title')
            property_dict['type'] = attr.get('type')
            property_dict['description'] = attr.get('description')
            if attr.get('maxLength'):
                property_dict['type'] = f'{attr["type"]}({attr["maxLength"]})'
        property_dict['required'] = name in schema_dict['required']

        property_list.append(property_dict)

    csv_file = output_folder / f'_{obj_name}.csv'
    with open(csv_file, 'w') as f:
        writer = DictWriter(f, fieldnames=list(property_list[0].keys()))
        writer.writeheader()
        writer.writerows(property_list)

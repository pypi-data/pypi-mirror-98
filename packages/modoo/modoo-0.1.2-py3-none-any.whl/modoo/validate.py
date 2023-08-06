# built-ins
import json
import sys
import os
# third-parties
from jsonschema import Draft7Validator


def run(input_json_path, schema_path):

    with open(input_json_path, 'r', encoding='utf8') as file:
        data = json.load(file)

    with open(schema_path, 'r', encoding='utf8') as file:
        schema = json.load(file)

    os.makedirs('./out', exist_ok=True)
    ext_removed = os.path.splitext(os.path.normpath(input_json_path))[0]
    file_name = ext_removed.split(os.path.sep)[-1]

    v = Draft7Validator(schema)

    errors = sorted(v.iter_errors(data), key=lambda e: e.path)

    with open(f'./out/{file_name}.vallog.txt', 'w', encoding='utf8') as file:
        sys.stdout = file
        for error in errors:
            print(error)
            print('-----------------------')

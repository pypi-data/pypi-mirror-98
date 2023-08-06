# built-ins
import json
import sys
# third-parties
from jsonschema import Draft7Validator


def run(input_json_path, schema_path, log_path):

    with open(input_json_path, 'r', encoding='utf8') as file:
        data = json.load(file)

    with open(schema_path, 'r', encoding='utf8') as file:
        schema = json.load(file)

    v = Draft7Validator(schema)

    errors = sorted(v.iter_errors(data), key=lambda e: e.path)

    with open(log_path, 'w', encoding='utf8') as file:
        sys.stdout = file
        for error in errors:
            print(error)
            print('-----------------------')

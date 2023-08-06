# built-ins
from functools import reduce
import json
import re
import os


def run(input_json_path, id_map_file_path):

    def reducer(acc, curr):
        id_pattern = r'(.+)\t(.+)'
        key, value = re.match(id_pattern, curr).groups()
        acc[key] = value
        return acc

    with open(id_map_file_path, 'r', encoding='utf8') as file:
        dp_rw_id_map = reduce(reducer, file.read().strip().split('\n'), {})

    def fix_id(id):
        return dp_rw_id_map[id]

    def fix_snt(snt):
        return {**snt, 'id': fix_id(snt['id'])}

    def fix_snts(snts):
        return [*map(fix_snt, snts)]

    def fix_doc(doc):
        return {**doc, 'sentence': fix_snts(doc['sentence'])}

    def fix_docs(docs):
        return [*map(fix_doc, docs)]

    def fix_data(data):
        return {**data, 'document': fix_docs(data['document'])}

    with open(input_json_path, 'r', encoding='utf8') as file:
        data = json.load(file)

    fixed_data = fix_data(data)

    os.makedirs('./out', exist_ok=True)
    ext_removed = os.path.splitext(os.path.normpath(input_json_path))[0]
    file_name = ext_removed.split(os.path.sep)[-1]

    with open(f'./out/{file_name}.idfix.json', 'w', encoding='utf8') as file:
        json.dump(fixed_data, file, indent=4, ensure_ascii=False)

# built-ins
from functools import reduce
from os import listdir, path, makedirs
import json
# customs
from modoo.idfuncs import jsons_from_dir


def run(input_json_path, rw_dir_path, annotation_level):

    rw_file_names = listdir(rw_dir_path)
    rw_data = map(jsons_from_dir(rw_dir_path), rw_file_names)

    def by_meta(acc, curr):
        _id = curr['id']
        meta = curr['metadata']
        acc[_id] = meta
        return acc

    rw_meta_map = reduce(by_meta, rw_data, {})

    def add_meta(doc):
        _id = doc['id']
        metadata = {**rw_meta_map[_id], 'annotation_level': [annotation_level]}
        return {**doc, 'metadata': metadata}

    def add_to_docs(docs):
        return [*map(add_meta, docs)]

    def add_to_data(data):
        return {**data, 'document': add_to_docs(data['document'])}

    with open(input_json_path, 'r', encoding='utf8') as file:
        data = json.load(file)

    added_data = add_to_data(data)

    makedirs('./out', exist_ok=True)
    ext_removed = path.splitext(path.normpath(input_json_path))[0]
    file_name = ext_removed.split(path.sep)[-1]

    with open(f'./out/{file_name}.docmeta.json', 'w', encoding='utf8') as file:
        json.dump(added_data, file, indent=4, ensure_ascii=False)

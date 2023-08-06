# built-ins
from functools import reduce
from os import listdir, path, makedirs
import json


def run(input_json_path, rw_dir_path):

    def get_meta(doc_record):
        return (doc_record['id'], doc_record['metadata'])

    def by_doc_reducer(rw_dir_path):
        def aux(acc, file_path):
            print(f'read: {file_path}')
            with open(path.join(rw_dir_path, file_path), 'r', encoding='utf8') as file:
                json_item = json.load(file)

            acc = {**acc,
                   **dict(map(get_meta, json_item['document']))}
            return acc
        return aux

    def add_meta(meta_by_doc):
        def aux(doc):
            _id = doc['id']
            metadata = meta_by_doc[_id] if _id in meta_by_doc else {}
            return {**doc, 'metadata': metadata}
        return aux

    def add_to_docs(meta_by_doc, docs):
        return [*map(add_meta(meta_by_doc), docs)]

    def add_to_data(meta_by_doc, data):
        return {**data, 'document': add_to_docs(meta_by_doc, data['document'])}

    with open(input_json_path, 'r', encoding='utf8') as file:
        data = json.load(file)

    json_paths = filter(lambda x: x.endswith('.json'), listdir(rw_dir_path))
    meta_by_doc = reduce(by_doc_reducer(rw_dir_path), json_paths, {})

    added_data = add_to_data(meta_by_doc, data)

    makedirs('./out', exist_ok=True)
    ext_removed = path.splitext(path.normpath(input_json_path))[0]
    file_name = ext_removed.split(path.sep)[-1]

    out_path = f'./out/{file_name}.docmeta.json'

    print(f'write: {out_path}')
    with open(out_path, 'w', encoding='utf8') as file:
        json.dump(added_data, file, indent=4, ensure_ascii=False)

    print('DONE!!')

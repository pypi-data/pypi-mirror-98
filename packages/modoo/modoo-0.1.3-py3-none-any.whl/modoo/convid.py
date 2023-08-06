# built-ins
import json
import re
import os


def run(input_json_path):

    def conv_id(_id):
        id_pattern = r'^(\w+).+?(\w+)$'
        matched = re.match(id_pattern, _id)
        if matched:
            doc_id, order = matched.groups()
            return f'{doc_id}.1.1.{order}'
        else:
            return _id

    def fix_snt(snt):
        return {**snt, 'id': conv_id(snt['id'])}

    def fix_snts(snts):
        return [*map(fix_snt, snts)]

    def fix_ant_pred(ant_pred):
        return {**ant_pred, 'sentence_id': conv_id(ant_pred['sentence_id'])}

    def fix_ants(ants):
        return [*map(fix_ant_pred, ants)]

    def fix_za_pair(pair):
        return {**pair, 'predicate': fix_ant_pred(pair['predicate']), 'antecedent': fix_ants(pair['antecedent'])}

    def fix_za_pairs(pairs):
        return [*map(fix_za_pair, pairs)]

    def conv_doc_id(_id):
        return f'{_id}.1'

    def fix_doc(doc):
        _id = conv_doc_id(doc['id'])
        print(f'process: {_id}')
        return {**doc,
                'id': _id,
                'sentence': fix_snts(doc['sentence']),
                'ZA': fix_za_pairs(doc['ZA'])}

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

    out_path = f'./out/{file_name}.idconv.json'

    print(f'write: {out_path}')

    with open(out_path, 'w', encoding='utf8') as file:
        json.dump(fixed_data, file, indent=4, ensure_ascii=False)

    print('DONE!!')

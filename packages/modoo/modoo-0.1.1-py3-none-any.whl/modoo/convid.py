# built-ins
import json
import re


def run(input_json_path, output_json_path):

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

    def fix_doc(doc):
        return {**doc, 'sentence': fix_snts(doc['sentence']), 'ZA': fix_za_pairs(doc['ZA'])}

    def fix_docs(docs):
        return [*map(fix_doc, docs)]

    def fix_data(data):
        return {**data, 'document': fix_docs(data['document'])}

    with open(input_json_path, 'r', encoding='utf8') as file:
        data = json.load(file)

    fixed_data = fix_data(data)

    with open(output_json_path, 'w', encoding='utf8') as file:
        json.dump(fixed_data, file, indent=4, ensure_ascii=False)

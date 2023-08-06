# built-ins
from functools import reduce
from operator import itemgetter
from copy import deepcopy


def merge_docs(zas_docs, zao_docs):
    def by_id_reducer(acc, curr):
        _id = curr['id']
        acc[_id] = curr
        return acc

    def merge_reducer(acc, curr):
        _id = curr['id']
        zas = curr['ZA']
        zao = acc[_id]['ZA']
        acc[_id]['ZA'] = [*zas, *zao]
        return acc
    zao_docs_by_id = reduce(by_id_reducer, deepcopy(zao_docs), {})
    return [*reduce(merge_reducer, zas_docs, zao_docs_by_id).values()]


def shake_docs(docs):
    def by_pred_reducer(acc, curr):
        pred = curr['predicate']
        snt_id, begin, end = itemgetter(
            'sentence_id', 'begin', 'end')(pred)
        key = f'{snt_id}-{begin}-{end}'

        if key in acc:
            acc[key]['antecedent'] = [
                *acc[key]['antecedent'],
                *curr['antecedent']
            ]
        else:
            acc[key] = curr

        return acc

    def shake_za(za):
        pred_za_hash = reduce(by_pred_reducer, za, {})
        return [*pred_za_hash.values()]

    def shake_za_mapper(doc):
        za = doc['ZA']
        return {**doc, 'ZA': shake_za(za)}

    return [*map(shake_za_mapper, docs)]


def compare_num_za(zas_docs, zao_docs, zaso_docs, za_docs):
    def mapper(elem):
        _id, za = itemgetter('id', 'ZA')(elem)
        return [_id, len(za)]

    zas_check = map(mapper, zas_docs)
    zao_check = map(mapper, zao_docs)
    zaso_check = map(mapper, zaso_docs)
    za_check = map(mapper, za_docs)

    def by_id_reducer(acc, curr):
        _id = curr[0]
        acc[_id] = curr
        return acc

    def append_reducer(acc, curr):
        _id, num_za = curr
        acc[_id] = [*acc[_id], num_za]
        return acc

    zas_hash = reduce(by_id_reducer, zas_check, {})
    zao_hash = reduce(append_reducer, zao_check, zas_hash)
    zaso_hash = reduce(append_reducer, zaso_check, zao_hash)
    za_hash = reduce(append_reducer, za_check, zaso_hash)
    header = ['id', 'num_za_s', 'num_za_o', 'num_za_s+o', 'num_za_merged']
    return [header, *za_hash.values()]

# built-ins
from operator import itemgetter
from functools import reduce
from os import path
import json
import re


def jsons_from_dir(dir_name: str):
    def json_read_mapper(file_names: str):
        with open(path.join(dir_name, file_names), 'r', encoding='utf8') as file:
            json_item = json.load(file)
        return json_item

    return json_read_mapper


def parse_id(_id):
    is_spoken = _id.startswith('S')
    id_pattern = r'^(\w+)(.+?)(\w+)$' if is_spoken else r'^(.+)\.(\w+)\.(\w+)$'
    doc_id, para_id, snt_id = re.match(id_pattern, _id).groups()
    order = int(snt_id) if is_spoken else int(para_id) * 1000 + int(snt_id)
    return (doc_id, int(order))


def get_id_form(record):
    _id, form = itemgetter('id', 'form')(record)
    doc_id, order = parse_id(_id)
    return dict(id=_id, form=form, doc_id=doc_id, order=order, mark=True)


def by_doc_id(acc, record):
    doc_id = record['doc_id']
    acc[doc_id] = [*acc[doc_id], record]
    return acc


def get_record_by_form(records, form):
    for record in records:
        if record['form'] == form:
            return record
    return False


def index_of_order(records, order):
    for index, record in enumerate(records):
        if record['order'] == order:
            return index
    return -1


def get_record_by_order(records, order):
    for record in records:
        if record['order'] == order:
            return record
    return {'form': 'check result: has no matched'}


def id_map_reducer(acc, dp_record):
    rw_records, last_order, delay = itemgetter(
        'rw_records', 'last_order', 'delay')(acc)
    dp_id, dp_form, dp_order = itemgetter('id', 'form', 'order')(dp_record)

    curr_order = dp_order + delay
    rw_record = get_record_by_order(rw_records, curr_order)

    if dp_form != rw_record['form']:

        start = curr_order - 2
        end = curr_order + 5

        def target_filter(record):
            order = record['order']
            mark = record['mark']
            return order >= start and order < end and mark

        targets = [*filter(target_filter, rw_records)]
        target_record = get_record_by_form(targets, dp_form)

        rw_record = target_record if target_record else rw_record

        if not target_record:
            print(dp_order, rw_record['order'])

    rw_id, rw_form, rw_order = itemgetter('id', 'form', 'order')(rw_record)
    id_delay = rw_order - dp_order
    id_step = rw_order - last_order
    exact_form = True if dp_form == rw_form else False

    mapRecord = dict(dp_id=dp_id, rw_id=rw_id, dp_form=dp_form, rw_form=rw_form,
                     id_delay=id_delay, id_step=id_step, exact_form=exact_form)

    acc['last_order'] = rw_order
    acc['delay'] = id_delay
    acc['mapRecord'] = [*acc['mapRecord'], mapRecord]

    if dp_form == rw_form:
        mark_index = index_of_order(rw_records, rw_order)
        acc['rw_records'][mark_index]['mark'] = False

    return acc


def get_id_map(rw_records, dp_records):

    rw_sample = sorted(rw_records, key=lambda x: x['order'])
    dp_sample = sorted(dp_records, key=lambda x: x['order'])

    id_map = reduce(id_map_reducer, dp_sample, {
                    'rw_records': rw_sample,
                    'last_order': 0,
                    'delay': 0,
                    'mapRecord': []})

    return id_map['mapRecord']

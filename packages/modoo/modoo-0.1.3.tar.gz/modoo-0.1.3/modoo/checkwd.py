# built-ins
import json
import os
import re
from operator import itemgetter
from functools import reduce


def run(input_json_path):

    def check_word(snt_form, snt_id):
        def aux(w_record):
            w_id, w_form, w_begin, w_end = itemgetter(
                'id', 'form', 'begin', 'end')(w_record)

            wds = re.split(r'\s+', snt_form)
            wd_test = 'fail'

            check_ids = isinstance(w_id, int) and isinstance(
                w_begin, int) and isinstance(w_end, int)
            if check_ids and w_form == snt_form[w_begin:w_end] and w_form == wds[w_id - 1]:
                wd_test = 'pass'

            return dict(check_type='wd', snt_id=str(snt_id), w_id=str(w_id),
                        w_form=w_form, w_begin=str(w_begin), w_end=str(w_end), wd_test=wd_test)
        return aux

    def check_dpwd(snt_form, snt_id):
        def aux(w_record):
            w_id, w_form = itemgetter('word_id', 'word_form')(w_record)
            wds = re.split(r'\s+', snt_form)
            wd_test = 'fail'

            check_ids = isinstance(w_id, int)
            if check_ids and w_form == wds[w_id - 1]:
                wd_test = 'pass'

            return dict(check_type='dpwd', snt_id=str(snt_id), w_id=str(w_id),
                        w_form=w_form, w_begin='NA', w_end='NA', wd_test=wd_test)
        return aux

    def check_wds(snt_form, snt_id, wds):
        return map(check_word(snt_form, snt_id), wds)

    def check_dpwds(snt_form, snt_id, dpwds):
        return map(check_dpwd(snt_form, snt_id), dpwds)

    def check_snt(snt_record):
        snt_id, snt_form, wds, dpwsds = itemgetter(
            'id', 'form', 'word', 'DP')(snt_record)

        return [*check_wds(snt_form, snt_id, wds),
                *check_dpwds(snt_form, snt_id, dpwsds)]

    def check_snts(snts):
        def reducer(acc, curr):
            return [*acc, *check_snt(curr)]
        return reduce(reducer, snts, [])

    def check_doc(doc):
        _id = doc['id']
        print(f'process: {_id}')
        return check_snts(doc['sentence'])

    def check_docs(docs):
        def reducer(acc, curr):
            return [*acc, *check_doc(curr)]
        return reduce(reducer, docs, [])

    with open(input_json_path, 'r', encoding='utf8') as file:
        data = json.load(file)

    wd_check_logs = check_docs(data['document'])

    os.makedirs('./out', exist_ok=True)
    ext_removed = os.path.splitext(os.path.normpath(input_json_path))[0]
    file_name = ext_removed.split(os.path.sep)[-1]

    out_path = f'./out/{file_name}.wdcheck.txt'

    print(f'write: {out_path}')
    with open(out_path, 'w', encoding='utf8') as file:
        file.write('check_type\tsnt_id\tw_id\tw_form\tw_begin\tw_end\twd_test')
        file.write('\n')
        for log in wd_check_logs:
            file.write('\t'.join([*log.values()]))
            file.write('\n')

    print('DONE!!')

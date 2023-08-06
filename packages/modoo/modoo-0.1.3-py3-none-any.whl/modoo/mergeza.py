# built-ins
import json
import os
# third-parties
from openpyxl import Workbook
# customs
from modoo.zafuncs import compare_num_za, merge_docs, shake_docs


def run(zas_file_path, zao_file_path, new_file_id):

    title_map = {'N': '신문', 'S': '구어'}
    title_type = title_map[new_file_id[0]]
    new_file_title = f'국립국어원 {title_type} 말뭉치 추출 {new_file_id}'
    merged_file_name = f'./out/{new_file_id}.json'
    num_check_file_name = f'./out/{new_file_id}.za_num.xlsx'

    print('read files')
    with open(zas_file_path, 'r', encoding='utf8') as file:
        zas_data = json.load(file)

    with open(zao_file_path, 'r', encoding='utf8') as file:
        zao_data = json.load(file)

    zas_docs = zas_data['document']
    zao_docs = zao_data['document']

    print('merge ZA')
    zaso_docs = merge_docs(zas_docs, zao_docs)

    print('shake ZA')
    za_docs = shake_docs(zaso_docs)

    metadata = {**zao_data['metadata'], 'title': new_file_title}

    merged = {'id': new_file_id, 'metadata': metadata, 'document': za_docs}

    os.makedirs('./out', exist_ok=True)

    print(f'write: {merged_file_name}')

    with open(merged_file_name, 'w', encoding='utf8') as file:
        json.dump(merged, file, indent=4, ensure_ascii=False)

    wb = Workbook()
    ws = wb.active

    for row in compare_num_za(zas_docs, zao_docs, zaso_docs, za_docs):
        ws.append(row)

    print(f'write: {num_check_file_name}')

    wb.save(num_check_file_name)
    print('DONE!!')

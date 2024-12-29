import re
import time

from until.sql_tools import mysql_db_conn, getStrAsMD5, freeRepeat, mongo_client
from until.config import he

from lxml import etree
from urllib.parse import unquote
import random
import requests
import json
import os

conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
mongo_db = mongo_client('cg')

select_ = 'select id,title,author_info_path from openalex_author_detail where is_download =1 and is_ava=0'

cur.execute(select_)

data = cur.fetchall()
# print(data)   #((1, 'Michael Graetzel', 'cg_expert_data/html/openalex/author_info/0/0/1.json'),

for item in data:
    ids, title, author_info_path = item
    excel_sql = 'select inst_name from elsevier_author_career where id=%s'
    cur.execute(excel_sql, (ids,))
    excel_data = cur.fetchone()
    inst_name, = excel_data
    # print(inst_name)
    # print(type(inst_name))
    author_info_path = 'Y:/' + author_info_path
    # print(author_info_path)
    with open(author_info_path, 'r', encoding='utf8') as f:
        json_data = json.load(f)

    count = json_data['meta']['count']
    results = json_data['results']
    is_true = False
    for i in results:

        inst_name = inst_name.replace(", ", ' ')
        inst_name = re.sub(r'[(].*?[)]', '', inst_name, re.S)
        inst_name = inst_name.strip().replace(" ", ' ')
        last_known_institutions = i['last_known_institutions']
        if inst_name in str(last_known_institutions):
            is_true = True
            is_ava = 1
            detail_json = json.dumps(i)
            break
    if not is_true:
        is_ava = -1
        detail_json = None

    update_sql = 'update openalex_author_detail set is_ava=%s,detail_json=%s where id=%s '
    cur.execute(update_sql, (is_ava, detail_json, ids))
    conn.commit()

import re
import time

from until.sql_tools import mysql_db_conn, getStrAsMD5
from until.config import he

from lxml import etree
from urllib.parse import unquote
import random

import json
import os
from until.sql_tools import mysql_db_conn, getStrAsMD5
from pymongo import MongoClient
from datetime import datetime


path_html = r'Y:/cg_expert_data/html/aminer_lw/0/0'

conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
# sql = 'select id,name_en,inst_name_en from paln_list_people where is_ava=1 and is_oa_lw_path_download=1 and oa_id is null   order by id asc   '
sql = 'select id,name_en,oa_lw_path from paln_list_people where id=8 '
cur.execute(sql)
data = cur.fetchall()

for item in data:
    in_id, name_en, oa_lw_path = item
    # print(in_id)
    # if '-' in name_en:
    #     name_en_d = name_en.replace('-', '')
    if ",," in oa_lw_path:
        oa_lw_path = oa_lw_path.split(",,")[0]
    with open(f"Z:/{oa_lw_path}", 'r', encoding='utf8') as f:
        data = json.load(f)
        results=data['results'][0]
        authorships=results['authorships']

        for author_list in authorships:

            display_name=author_list['author']['display_name']
            raw_author_name=author_list['raw_author_name']
            print(name_en,'--',display_name,raw_author_name)
            if name_en in display_name or name_en in raw_author_name:
                author_id=author_list['author']['id']
                print(author_id)
                # author_id_q=author_id.replace('https://openalex.org/', '')
                # print(author_id_q)
                # update_ = 'update paln_list_people set oa_id=%swhere id =%s'
                # cur.execute(update_, (author_id_q,  in_id,))
                # conn.commit()

            # if name_en.lower().replace(" ", "") == display_name.lower().replace(" ", ""):
            #     author_id=author['id']
            #     author_id_q=author_id.replace('https://openalex.org/', '')
            #     print(author_id_q)
            #     # update_ = 'update paln_list_people set oa_id=%swhere id =%s'
            #     # cur.execute(update_, (author_id_q,  in_id,))
            #     # conn.commit()
            # if '-' in name_en:
            #     name_en_d = name_en.replace('-', '')
            #     if name_en_d.lower().replace(" ", "") == display_name.lower().replace(" ", ""):
            #         author_id = author['id']
            #         author_id_q = author_id.replace('https://openalex.org/', '')
            #         print(author_id_q)
            #         # update_ = 'update paln_list_people set oa_id=%swhere id =%s'
            #         # cur.execute(update_, (author_id_q, in_id,))
            #         # conn.commit()
            #
            #     break







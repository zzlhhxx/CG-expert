import re
import time

import pypinyin
from pypinyin import pinyin, Style

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

proxy={
    "https":"192.168.5.21:41091",
    "http":'192.168.5.21:41091',
}


select_sql='select id,name,name_en,inst_name,aminer_id,oa_id from paln_list_people where is_ids=1 and oa_id is not null order by id asc '
cur.execute(select_sql)
data=cur.fetchall()
for item in data:
    ids, author, name_en, org, aminer_id, oa_id = item
    # json_oa = json.loads(author_info_json)
    # oa_id = json_oa["id"].split("/")[-1]
    sql_aminer = f'select id,aminer_id from zjwl_author  where aminer_id=%s'
    cur.execute(sql_aminer, (aminer_id,))
    data_1 = cur.fetchone()
    print(data_1)
    if data_1:
        update_sql = f"update zjwl_author  set is_paln=%s where aminer_id=%s"
        cur.execute(update_sql, (1, aminer_id))
        conn.commit()
    else:
        add_data = ("INSERT INTO zjwl_author (source_id,name,name_zh,inst_name,aminer_id,oa_id,is_paln) VALUES (%s, %s, %s, %s, %s, %s,%s)")
        data_to_insert = (ids,name_en,author,org,aminer_id,oa_id,1)
        cur.execute(add_data, data_to_insert)
        conn.commit()
        print(ids,"已插入")
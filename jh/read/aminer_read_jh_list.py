import time
from until.sql_tools import mysql_db_conn, getStrAsMD5
from until.config import he
from lxml import etree
from urllib.parse import unquote
import random
import requests
import json
import os

path = r'Y:/'
conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
sql = 'select id,name,inst_name,list_json_path,is_ids from paln_list_people  where  list_json is null and is_ava=0 and is_ids=1 order by  id asc '

cur.execute(sql)
data = cur.fetchall()

for item in data:
    in_id,name,inst_name,list_json_path,is_d = item
    path_json = path + list_json_path
    data_str = open(path_json, 'r', encoding='utf-8').read()
    data_json = json.loads(data_str)
    try:
        d=data_json['data']
        hitsTotal = d['hitsTotal']

        if hitsTotal >0:
            hitList = d['hitList']
            for hit in hitList:
                if not hit:
                    continue
                if hit:
                    aminer_id=hit['id']
                    print(aminer_id)
                    update_sql = f"update paln_list_people  set list_json=%s,aminer_id=%s,is_ids=%s,is_ava=%s where id = %s"
                    cur.execute(update_sql, (hit, aminer_id,1,is_d, in_id))
                    conn.commit()
                    break
    except Exception as e:
        print(e)
        print(data_json)
        continue



























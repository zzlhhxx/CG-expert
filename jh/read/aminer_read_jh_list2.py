import time
from until.sql_tools import mysql_db_conn, getStrAsMD5
from until.config import he
from lxml import etree
from urllib.parse import unquote
import random
import requests
import json
import re
import os

path = r'Y:/'
conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
# sql = 'select id,name,inst_name,list_json_path,is_ids from paln_list_people  where  list_json is null and is_ava=1 and is_ids=0 order by  id asc '
sql = 'select id,name,inst_name,list_json_path,is_ids from paln_list_people  where  list_json is null and id=1837 '
cur.execute(sql)
data = cur.fetchall()

for item in data:
    in_id,name,inst_name,list_json_path,is_d = item
    path_json = path + list_json_path    #Y:/cg_expert_data/html/aminer_paln_list_people2/0/0/11.json
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
                if not hit.get("contact"):
                    continue
                print(hit['contact'],inst_name)
                print('***********')
                affiliationZh=hit['contact']['affiliationZh']if hit['contact'].get('affiliationZh') else ''
                bioZh=hit['contact']['bioZh'] if hit['contact'].get('bioZh') else ''
                eduZh=hit['contact']['eduZh'] if hit['contact'].get('eduZh') else ''
                workZh=hit['contact']['workZh'] if hit['contact'].get('workZh') else ''

                if inst_name:
                    inst_name = inst_name.replace(", ", ' ')
                    inst_name = re.sub(r'[(].*?[)]', '', inst_name, re.S)
                    inst_name = inst_name.strip().replace(" ", ' ')
                if affiliationZh:
                    affiliation=affiliationZh.replace(" ", ' ')
                if bioZh:
                    bioZh=bioZh.replace(" ", ' ')
                if eduZh:
                    eduZh=eduZh.replace(" ", ' ')
                if workZh:
                    workZh=workZh.replace(" ", ' ')

                if inst_name in affiliationZh or inst_name in bioZh or inst_name in eduZh or inst_name in workZh:
                    print('cunzai')
                    aminer_id = hit['id']
                    print(aminer_id)
                    update_sql = f"update paln_list_people  set list_json=%s,aminer_id=%s,is_ids=%s where id = %s"
                    cur.execute(update_sql, (hit, aminer_id,1, in_id))
                    conn.commit()
                    break

                # if hit:
                #     aminer_id=hit['id']
                #     print(aminer_id)
                #     update_sql = f"update paln_list_people  set list_json=%s,aminer_id=%s,is_ids=%s,is_ava=%s where id = %s"
                #     cur.execute(update_sql, (hit, aminer_id,1,is_d, in_id))
                #     conn.commit()
                #     break
    except Exception as e:
        print(e)
        print(data_json)
        continue

























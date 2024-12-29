import time
from until.sql_tools import mysql_db_conn,freeRepeat
from lxml import etree
from urllib.parse import unquote
import random
import requests
import json
import os

path_html = r'D:/cg_expert_data/html/aminer/'

conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
sql = 'select id,aminer_id,lw_path,source_id from aminer where  is_ava=1 and char_length(lw_path)>1 and lw_ids is null and is_to_mongo=1 order by id asc limit 1000'
# sql = 'select id,hitsTotal,authfull,inst_name,aminer_path from elsevier_author_career where id =2 '
cur.execute(sql)
data = cur.fetchall() #mysql查詢數據

for item in data:
    ids, aminer_id, lw_path,source_id = item #mysql字段
    # print(lw_path)    #cg_expert_data/html/aminer_lw/0/0/23_0.json,,cg_expert_data/html/aminer_lw/0/0/23_1.json,,cg_expert_data/html/aminer_lw/0/0/23_2.json,,cg_expert_data/html/aminer_lw/0/0/23_3.json
    lw_path_qs=lw_path.split(',,')
    list_id=[]
    for lw_path_q in lw_path_qs:
        print(lw_path_q)
        lw_path = 'Y:\\' + lw_path_q.replace("/","\\")
        # print(lw_path)
        with open(lw_path, 'r', encoding='utf8') as f:
            json_data = json.load(f)
        data_item = json_data['data']
        # print(data_item[0])
        # print(type(data_item[0]))  #<class 'dict'>
        data=data_item[0]['data']
        # print(data)
        # print(type(data))
        hitList=data['hitList']
        # print(hitList)
        # print(type(hitList))  #<class 'list'>
        for hit in hitList:
            # print(hit)
            # print(type(hit))
            id=hit['id']
            list_id.append(id)
    # print(list_id)  #['66ec821701d2a3fbfc6b90ea', '64ec376c3fda6d7f063f3453', '66594d7901d2a3fbfc13b49d',**]
    str_id=',,'.join(list_id)
    # print(str_id)  #<class 'str'>
    update_sql = f"update aminer  set lw_ids=%s where id=%s"
    cur.execute(update_sql, (str_id, ids))
    conn.commit()
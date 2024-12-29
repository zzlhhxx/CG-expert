from until.sql_tools import mysql_db_conn, getStrAsMD5,freeRepeat
import json
import os
from pymongo import MongoClient
from datetime import datetime

# 详情页面
# 连接到MongoDB
client = MongoClient("192.168.5.21", 27017)



path_html = r'Y:/cg_expert_data/html/aminer_lw/0/0'

conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
sql = 'select id,aminer_id,lw_path from paln_list_people where  is_lw=1 and is_ava=1 and is_ids=1 order by id asc '
cur.execute(sql)
data = cur.fetchall()

for item in data:
    in_id, aminer_id, lw_paths = item

    lw_path_list = lw_paths.split(',,')  # 字符串切割，化为列表
    for lw_path in lw_path_list:
        if not lw_path:
            continue
        address = 'E:/' + lw_path
        data = open(address, 'r', encoding='utf-8').read()
        json_data = json.loads(data)
        if not json_data['data'][0]['data'].get("hitList"):
            print(json_data)
        else:
            data_lists = json_data['data'][0]['data']['hitList']
            for data_list in data_lists:  # 循环
                lw_id = data_list['id']
                repeat_result = freeRepeat('aminer_lw', "lw_id", lw_id, conn)
                # print(aminer_id)
                if repeat_result:
                    insert_sql = 'insert into aminer_lw(lw_id,detail_json) value(%s,%s)'
                    cur.execute(insert_sql, (lw_id, json.dumps(data_list,ensure_ascii=False)),)
                    conn.commit()


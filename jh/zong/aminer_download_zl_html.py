import time

from until.sql_tools import mysql_db_conn, getStrAsMD5,freeRepeat
from until.config import he

from lxml import etree
from urllib.parse import unquote
import random
import requests
import json
import os

# 详情页面
#


# path_html = r'E:/html/aminer_html/'

conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
sql = ('select id,aminer_id,zl_path from paln_list_people where  is_ava=1 and zl_ids is null and  is_ids=1 and is_zl=1  order by id asc ')
cur.execute(sql)
data = cur.fetchall()


for item in data:
    ids, aminer_id, zl_path = item
    zl_path=zl_path.strip()
    zl_ids=''
    zl_list_id = []

    if  zl_path:
        zl_path_list = zl_path.split(',,')
        for zl_path_q in zl_path_list:
            # zl_path = 'Y:/' + zl_path_q.replace("cg_expert_data/", '')
            zl_path = 'Y:/' + zl_path_q
            # print(zl_path)
            with open(zl_path, 'r', encoding='utf8') as f:
                json_data = json.load(f)

            data_item = json_data['data']
            if data_item.get("hitList"):
                hitList = data_item['hitList']
                for hit in hitList:
                    if not hit:
                        continue
                    zl_id = hit['id']
                    zl_list_id.append(zl_id)
                    repeat_result = freeRepeat('aminer_zl', "zl_id", zl_id, conn)
                    # print(aminer_id)
                    if repeat_result:
                        insert_sql = 'insert into aminer_zl(f_id,zl_id,paln_list_people) value(%s,%s,%s)'
                        cur.execute(insert_sql, (ids, zl_id,1))
                        conn.commit()
                    else:
                        print(ids, zl_id)
                # list_id.append(zl_id)
        zl_ids=',,'.join(list(set(zl_list_id)))


    update_='update paln_list_people set zl_ids=%s where id=%s'
    cur.execute(update_,(zl_ids,ids))
    conn.commit()


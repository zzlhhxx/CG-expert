import json

import requests




# 论文      post
# https://apiv2.aminer.cn/n

#
# a = [{"action": "person.SearchPersonPaper", "parameters": {"person_id": "5631e77645cedb3399f52483",
#                                                            "search_param": {"needDetails": False, "page": 1, "size": 10,
#                                                                             "sort": [
#                                                                                 {"field": "year", "asc": False}]}}}]
# path_html = r'Z:/html/aminer_lunwen/'


import time

from until.sql_tools import mysql_db_conn, getStrAsMD5
from until.config import he

from lxml import etree
from urllib.parse import unquote
import random
import requests
import json
import os

# 详情页面
#

#Y:\cg_expert_data\html
path_html = r'Y:/cg_expert_data/html/aminer_lw/'

conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
sql = 'select id,source_id,aminer_id,profilePubsTotal,lw_path from aminer where is_ava=1 and is_lw =0 order by  id asc limit 1000'
cur.execute(sql)
data = cur.fetchall()

for item in data:
    in_id, source_id,aminer_id,profilePubsTotal,lw_path = item
    url = 'https://apiv2.aminer.cn/n'
    a = [{"action": "person.SearchPersonPaper", "parameters": {"person_id": f"{aminer_id}",
                                                               "search_param": {"needDetails": False, "page": 1,
                                                                                "size": profilePubsTotal,
                                                                                "sort": [
                                                                                    {"field": "year", "asc": False}]}}}]
    res = requests.post(url, headers=he, timeout=20,data=json.dumps(a))

    print(res.json())
    if res.status_code == 200:
        path = path_html + str(in_id // 10000) + '/' + str(in_id // 100) + '/'
        if os.path.exists(path) is False:
            os.makedirs(path)
        dest_dir = os.path.join(path, str(in_id) + ".json")
        with open(dest_dir, 'w', encoding='utf-8') as ff:
            ff.write(res.text)
            html_path = dest_dir.replace(path_html[0:1] + ":/", "")
            print(html_path)
            update_sql = f"update aminer  set lw_path=%s,is_lw=%s where id = %s"
            cur.execute(update_sql, (html_path, 1, in_id))
            conn.commit()
    else:
        print(res.text)
    time.sleep(1)





#
# if resp.status_code ==200:
#
#     data = json.loads(resp.text)
#     # print(data)
#     hitList=data['data'][0]['data']['hitList']
#
#     for item in hitList:
#         print(item)
#
#
# # data1=dict(data)
# print(data['data'][0].get)
# print(data)
# # data=dict(response.text)
# # hit_list = data.get('data', {}).get('hitList', [])
# # print(hit.list)


# with open('Z:/html/aminer_html/0/0/28.html', 'r', encoding='utf-8')as f:
#     data = json.load(f)
#     print(data)
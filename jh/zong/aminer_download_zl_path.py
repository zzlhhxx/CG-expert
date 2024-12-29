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

# Y:\cg_expert_data\html
path_html = r'Y:/cg_expert_data/html/aminer_zl_paln_list_people/'

conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
# sql = 'select id,source_id,aminer_id,profilePubsTotal from aminer where is_ava=1 and is_lw =0  order by  id asc '
sql = 'select id,aminer_id from paln_list_people where is_ava=1 and is_ids=1  and is_zl=1 order by id asc limit 500'
# sql = 'select id,source_id,aminer_id,profilePubsTotal,lw_path from aminer where id=23'
cur.execute(sql)
data = cur.fetchall()

for item in data:
    # try:
    in_id, aminer_id= item
    print(in_id)
    html_path_list = []
    # if profilePubsTotal == 0:
    #     pass
    # else:
    page = 0
    size = 100
    count = 0
    while 1:
        url = 'https://searchtest.aminer.cn/aminer-search/search/patent'
        b = {"filters": [
            {"boolOperator": 3, "field": "inventor.person_id", "type": "term",
             "value": f"{aminer_id}"}],
            "sort": [{"field": "pub_date", "asc": False}],
            "needDetails": True, "query": "", "page": page,
            "size": 100}

        t1 = time.time()
        he['Content-Type'] = 'application/json;charset=utf-8'
        res = requests.post(url, headers=he, timeout=20, data=json.dumps(b))
        #
        data = res.json()
        if res.status_code == 200:
            hitList = data['data']['hitList']
            hitsTotal = data['data']['hitsTotal']
            path = path_html + str(in_id // 10000) + '/' + str(in_id // 100) + '/'
            if os.path.exists(path) is False:
                os.makedirs(path)
            dest_dir = os.path.join(path, str(in_id) +f'_{page}'+ ".json")
            with open(dest_dir, 'w', encoding='utf-8') as ff:
                json.dump(data, ff,  ensure_ascii=False)
            html_path = dest_dir.replace(path_html[0:1] + ":/", "")
            html_path_list.append(html_path)
            t2 = time.time()
            print(f'采集：{len(hitList)}，花费时间 {int(t2 - t1)}')

            if hitsTotal > size:
                size += 100
                page += 1
            else:
                break
        else:
            print(res.text)
        time.sleep(2)

    update_sql = f"update paln_list_people  set zl_path=%s,is_zl=%s where id = %s"
    cur.execute(update_sql, (",,".join(html_path_list), 1, in_id))
    conn.commit()




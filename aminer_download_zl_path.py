import time
from until.sql_tools import mysql_db_conn, getStrAsMD5
from until.config import he
import random
import requests
import json
import os

# 详情页面
#

# Y:\cg_expert_data\html
path_html = r'Y:/cg_expert_data/html/aminer_zl_1000/'

conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
# sql = 'select id,source_id,aminer_id,profilePubsTotal,lw_path from aminer where is_ava=1 and is_lw =0  order by  id asc '
sql = 'select id,source_id,aminer_id,profilePubsTotal,lw_path from aminer where is_ava=1 and is_zl =0  order by  id asc'
# sql = 'select id,source_id,aminer_id,profilePubsTotal,lw_path from aminer where id=23'
cur.execute(sql)
data = cur.fetchall()

for item in data:
    # try:
    in_id, source_id, aminer_id, profilePubsTotal, lw_path = item
    print(in_id, profilePubsTotal)
    html_path_list = []
    if profilePubsTotal == 0:
        pass
    else:
        page = 0
        size = 100
        count = 0
        while 1:

            url = 'https://searchtest.aminer.cn/aminer-search/search/patent'
            #value:aminer_id
            b = {"filters": [
                {"boolOperator": 3, "field": "inventor.person_id", "type": "term",
                 "value": f"{aminer_id}"}],
                "sort": [{"field": "pub_date", "asc": False}],
                "needDetails": True, "query": "", "page": page,
                "size": 100}

            t1 = time.time()
            he['Content-Type'] = 'application/json;charset=utf-8'
            res = requests.post(url, headers=he, timeout=20, data=json.dumps(b))

            data = res.json()
            print(data)
            if res.status_code == 200:
                hitList = data['data']['hitList'] if data['data'].get("hitList") else ""
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

    print(html_path_list)
    update_sql = f"update aminer  set zl_path=%s,is_zl=%s where id = %s"
    cur.execute(update_sql, (",,".join(html_path_list), 1, in_id))
    conn.commit()


# except Exception as e:
#     print(e)
#     print(e.__traceback__.tb_lineno)
#     time.sleep(10)
#     continue

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
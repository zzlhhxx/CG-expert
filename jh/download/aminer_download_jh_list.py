import time

from until.sql_tools import mysql_db_conn, getStrAsMD5
from until.config import he

from lxml import etree
from urllib.parse import unquote
import random
import requests
import json
import os

path_html = r'Y:/cg_expert_data/html/aminer_paln_list_people/'
conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
sql = 'select id,name,inst_name from paln_list_people where  is_ava=0 order by  id asc '
cur.execute(sql)
data = cur.fetchall()

for item in data:
    in_id,name,inst_name = item  #1   郑南峰  厦门大学
    url = 'https://searchtest.aminer.cn/aminer-search/search/person'

    query = {"query": "", "needDetails": True, "page": 0, "size": 20, "aggregations": [{"field": "h_index",
                                                                                        "rangeList": [
                                                                                            {"from": 0, "to": 10},
                                                                                            {"from": 10,
                                                                                             "to": 20},
                                                                                            {"from": 20,
                                                                                             "to": 30},
                                                                                            {"from": 30,
                                                                                             "to": 40},
                                                                                            {"from": 40,
                                                                                             "to": 50},
                                                                                            {"from": 50,
                                                                                             "to": 60},
                                                                                            {"from": 60,
                                                                                             "to": 99999}],
                                                                                        "size": 0, "type": "range"},
                                                                                       {"field": "lang", "size": 10,
                                                                                        "type": "terms"},
                                                                                       {"field": "nation", "size": 10,
                                                                                        "type": "terms"},
                                                                                       {"field": "gender", "size": 10,
                                                                                        "type": "terms"},
                                                                                       {"field": "contact.position",
                                                                                        "size": 20, "type": "terms"},
                                                                                       {"field": "org_id", "size": 200,
                                                                                        "type": "terms"}],
             "filters": [],
             "searchKeyWordList": [
                 {"advanced": True, "keyword": f"{name}", "operate": "0", "wordType": 4, "segmentationWord": "True",
                  "needTranslate": True},
                 {"advanced": True, "keyword": f"{inst_name}", "operate": "0", "wordType": 5,
                  "segmentationWord": "True",
                  "needTranslate": True}], "usingSemanticRetrieval": True}

    headers = {
        "content-type": "application/json;charset=UTF-8"
    }
    res = requests.post(url=url, data=json.dumps(query), headers=headers)
    list_json_text=res.text


    if res.status_code == 200:
        data = res.json()
        if data['code'] == 200:
            hitsTotal = data['data']['hitsTotal']

            print(hitsTotal)
            path = path_html + str(in_id // 10000) + r'/' + str(in_id // 100) + '/'
            if os.path.exists(path) is False:
                os.makedirs(path)
            dest_dir = os.path.join(path, str(in_id) + ".json")
            with open(dest_dir, 'w', encoding='utf-8') as ff:
                json.dump(data, ff, indent=1, ensure_ascii=False)
            html_path = dest_dir.replace(path_html[0:1] + ":/", "")
            update_sql = f"update paln_list_people  set list_json_path=%s,is_ava=%s where id = %s"
            cur.execute(update_sql, (html_path,1, in_id))
            conn.commit()
        else:
            print("失败",in_id)
            update_sql = f"update paln_list_people  set is_ava=%s where id = %s"
            cur.execute(update_sql, (-1))
            conn.commit()
            time.sleep(10)
    else:
        print(res.text)
        print("网页获取失败",in_id)
    time.sleep(2)


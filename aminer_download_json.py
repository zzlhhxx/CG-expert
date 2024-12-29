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


path_html = r'Z:/html/aminer_html/'

conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
sql = 'select id,source_id,aminer_id from aminer where is_ava=1 and is_download_html =0 order by  id asc limit 1000'
cur.execute(sql)
data = cur.fetchall()

for item in data:
    in_id, source_id, aminer_id = item
    url = f'https://www.aminer.cn/profile/neal-stuart-young-neal-s-young/{aminer_id}'
    res = requests.get(url, headers=he, timeout=20)
    if res.status_code == 200:
        path = path_html + str(in_id // 10000) + '/' + str(in_id // 100) + '/'
        if os.path.exists(path) is False:
            os.makedirs(path)
        dest_dir = os.path.join(path, str(in_id) + ".html")
        with open(dest_dir, 'w', encoding='utf-8') as ff:
            ff.write(res.text)
            html_path = 'cg_expert_data/'+dest_dir.replace(path_html[0:1] + ":/", "")
            update_sql = f"update aminer  set html_path=%s,is_download_html=%s where id = %s"
            cur.execute(update_sql, (html_path, 1, in_id))
            conn.commit()
    else:
        print(res.text)
    time.sleep(1)

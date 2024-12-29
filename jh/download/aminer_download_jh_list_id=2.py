import time

from until.sql_tools import mysql_db_conn, getStrAsMD5
from until.config import he

from lxml import etree
from urllib.parse import unquote
import random
import requests
import json
import os

path_html = r'Y:/cg_expert_data/html/aminer_paln_list_people2/'
conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
# sql = 'select id,name,inst_name from paln_list_people where  is_ava=0 and is_ids=0 order by  id asc '
sql = 'select id,name,inst_name,list_json_path from paln_list_people where is_ids=2 '
cur.execute(sql)
data = cur.fetchall()

for item in data:
    in_id,name,inst_name,list_json_path = item  #1   郑南峰  厦门大学
    p = 1
    path_html=r'Y:/'+list_json_path
    print(path_html)
    # dest_dir = os.path.join(path_html, str(in_id) + ".json")

    # with open(dest_dir, 'w', encoding='utf-8') as ff:
    #     json.dump(data, ff, indent=1, ensure_ascii=False)
    # html_path = dest_dir.replace(path_html[0:1] + ":/", "")
    # update_sql = f"update paln_list_people  set list_json_path=%s,is_ava=%s where id = %s"
    # cur.execute(update_sql, (html_path,p, in_id))
    # conn.commit()

    time.sleep(2)


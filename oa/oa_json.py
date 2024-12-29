import time

from until.sql_tools import mysql_db_conn, getStrAsMD5

import json




conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
sql = 'select id,inst_name_en,oa_path from paln_list_people where is_ava=1 and is_ids=1 and  is_oa_download=1 order  by id asc limit 1 '
cur.execute(sql)
data = cur.fetchall()

for item in data:
    ids,inst_name_en,oa_path = item
    print(oa_path)
    with open(f"Z:/{oa_path}", 'r', encoding='utf8') as f:
        data = json.load(f)
        results=data['results']
        print(results)


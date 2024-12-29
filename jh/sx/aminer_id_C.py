import time
from until.sql_tools import mysql_db_conn, getStrAsMD5
from until.config import he
from lxml import etree
from urllib.parse import unquote
import random
import requests
import json
import os


conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
sql = 'select id,name,inst_name,is_ids,aminer_id from paln_list_people  where  is_ava=1 and is_ids=1 order by  id asc '

cur.execute(sql)
data = cur.fetchall()

for item in data:
    in_id,name,inst_name,is_ids,aminer_id_1= item

    sql_aminer = f'select id,aminer_id from aminer  where aminer_id=%s '
    cur.execute(sql_aminer, (aminer_id_1,))
    data_1 = cur.fetchall()
    print(data_1)
    if data_1:
        update_sql = f"update paln_list_people  set is_qc=%s where id = %s"
        cur.execute(update_sql, (1,in_id))
        conn.commit()
    else:
        print("空")

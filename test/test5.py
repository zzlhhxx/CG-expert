from until.sql_tools import mysql_db_conn, getStrAsMD5
import random
import requests
import json



conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
sql = 'select id,source_id,zl_ids,aminer_id from aminer where  is_ava=1 and char_length(zl_ids)>1  order by id asc'
cur.execute(sql)
data = cur.fetchall()

for item in data:
    ids,source_id,zl_ids,aminer_id= item
    zl_ids_lists=zl_ids.split(",,")
    for zl_idd in zl_ids_lists:
        sql = f'select id from aminer_zl where zl_id="{zl_idd}"'
        cur.execute(sql)
        data_zl = cur.fetchall()
        if not data_zl:
            print (data_zl)

#通过zl_id 找到aimenr表中的问题
#nstl 找到法律信息。并且写好代码，我这边已更新入nstl，你这边自己可以开始update

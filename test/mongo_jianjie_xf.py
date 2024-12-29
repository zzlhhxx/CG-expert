
# -*- coding: utf-8 -*-
from until.sql_tools import mongo_client, mysql_db_conn
import re
import json
from until.time_tool import timestamp_to_date_str
import datetime
conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()

mongo_db = mongo_client('cg')
c = mongo_db['zjwl_author']
filter = {
        "_id": { "$gt": 10000000 }
    }
documents=c.find(filter)
for document in documents:
    ids=document["_id"]
    au_resume=document['au_resume']
    if not au_resume:
        continue
    print(au_resume)
    # au_resume_str=r"au_resume"
    sql_ = f'insert into awards_xunfei(ids,jianjie) values(%s,%s)'
    cur.execute(sql_,(ids,au_resume))
    conn.commit()

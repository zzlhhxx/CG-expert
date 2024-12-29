import time

from until.sql_tools import mysql_db_conn, getStrAsMD5,freeRepeat
from until.config import he

from lxml import etree
from urllib.parse import unquote
import random
import requests
import json
import os

# 详情页面
#
conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()

def parse_id_url():
    sql = 'select id,xm_ids from paln_list_people where is_ava=1 and  char_length(xm_ids)>1  and is_xm=1 and is_ids=1 order by  id asc  '
    # sql = 'select id,source_id,aminer_id from aminer where id=28  order by  id asc '
    cur.execute(sql)
    data = cur.fetchall()
    print(len(data))
    for i in data:
        ids,xm_ids=i
        if xm_ids:
            xm_id_list=xm_ids.split(",,")
            xm_id_list=list(set(xm_id_list))
            for xm_id in xm_id_list:
                repeat_result = freeRepeat('aminer_xm', "xm_id", xm_id, conn)
                # print(aminer_id)
                if repeat_result:
                    insert_sql = 'insert into aminer_xm(f_id,xm_id) value(%s,%s)'
                    cur.execute(insert_sql,(ids,xm_id))
                    conn.commit()
                else:
                    print(xm_id)



parse_id_url()



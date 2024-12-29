
import re
import time

from until.sql_tools import mysql_db_conn, getStrAsMD5
from until.config import he

from lxml import etree
from urllib.parse import unquote
import random

import json
import os
from until.sql_tools import mysql_db_conn, getStrAsMD5
from pymongo import MongoClient
from datetime import datetime



conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()




def contrast():
    select_ = 'select id,name,inst_name_en,inst_name_en,oa_path from paln_list_people where is_ids =1 and is_oa_lw_path_download=1 and  oa_id is null  order by id asc'
    # select_ = 'select id,name,inst_name_en,inst_name_en,oa_path from paln_list_people where  id=818'
    cur.execute(select_)
    data = cur.fetchall()
    print(len(data))
    inde  =0
    for item in data:
        inde +=1
        ids,title,inst_name_en,inst_name_en,oa_path = item
        if inst_name_en:
            inst_name_en =inst_name_en.replace(", " ,',').replace(";" ,',').split(",")

            inst_name_en_list  =[x.strip() for x in inst_name_en if x.strip() != '']

            author_info_path = 'Z:/' + oa_path
            # try:
            with open(author_info_path, 'r', encoding='utf8') as f:
                json_data = json.load(f)
            # print(json_data)
            count = json_data['meta']['count']
            results = json_data['results']
            is_true = False
            for i in results:
                oa_id =i["id"].replace("https://openalex.org/",'')
                affiliations =i['affiliations'] if i.get("affiliations") else ''

                last_known_institutions =i['last_known_institutions'] if i.get("last_known_institutions") else ''

                for g in inst_name_en_list:
                    # print(g, )
                    # print(last_known_institutions, )

                    if g in str(last_known_institutions):
                        is_true = True
                        print(g)
                        # print(i)
                        updage_ = 'update paln_list_people set oa_list_json=%s,oa_id=%s where id =%s'
                        print(json.dumps(i, ensure_ascii=False))
                        cur.execute(updage_, (json.dumps(i, ensure_ascii=False), oa_id, ids,))
                        conn.commit()
                        break
                if is_true:
                    break


contrast()


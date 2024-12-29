import re
import time

from until.sql_tools import mysql_db_conn, getStrAsMD5, freeRepeat, mongo_client
from until.config import he

from lxml import etree
from urllib.parse import unquote
import random
import requests
import json
import os

conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
mongo_db = mongo_client('cg')

proxy={
    "https":"192.168.5.21:41091",
    "http":'192.168.5.21:41091',
}

path_html = r'Z:/cg_expert_data/html/openalex_paln_list_people/author_info/'

select_sql='select id,name_en from paln_list_people where is_oa_download=0 and is_ids=1 and is_ava=1 order by id asc   '
cur.execute(select_sql)
data=cur.fetchall()
for item in data:
    ids, name_en=item
    url=f'https://api.openalex.org/authors?filter=display_name.search:{name_en.replace(",", "")}'
    res=requests.get(url,proxies=proxy,timeout=20)
    if res.status_code ==200:
        json_data=res.json()

        # print(json_data)
        if json_data['meta']['count'] >0:
            path = path_html + str(ids // 10000) + '/' + str(ids // 100) + '/'
            if os.path.exists(path) is False:
                os.makedirs(path)
            dest_dir = os.path.join(path, str(ids) +  ".json")
            with open(dest_dir, 'w', encoding='utf-8') as ff:
                json.dump(json_data, ff, ensure_ascii=False)
            html_path = dest_dir.replace(path_html[0:1] + ":/", "")
            is_download=1
        else:
            html_path=''
            is_download=-1
        update_ = 'update paln_list_people set oa_path=%s,is_oa_download=%s where id =%s'
        cur.execute(update_, (html_path, is_download,ids,))
        conn.commit()
        time.sleep(1)
        print(ids)
    else:
        print('其他错误')

        print(res.status_code)
        print(res.text)



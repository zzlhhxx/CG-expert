import re
import time

import pypinyin
from pypinyin import pinyin, Style

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


select_sql='select id,name,oa_lw_path from paln_list_people where is_ava=1 and is_oa_lw_path_download=1 and oa_id is null   order by id asc  '
cur.execute(select_sql)
data=cur.fetchall()
for item in data:
    ids,name_en,oa_lw_path=item
    if "(女)" in name_en:
        name_en = name_en.replace("(女)","")
    name_en = pypinyin.pinyin(name_en, style=pypinyin.NORMAL)
    name_pin=''
    for pin in name_en:
        name_pin+=' '+pin[0]
    nested_str = [', '.join(map(str, sublist)) for sublist in name_en]
    print(name_pin)
    flag = True
    with open(f"Z:/{oa_lw_path}", 'r', encoding='utf8') as f:
        data = json.load(f)
        authorships = data["results"][0]["authorships"]
        for i in range(0,len(authorships)):
            author = authorships[i]["author"]
            display_name = author["display_name"]
            if "-" in name_pin:
                name_pin = name_pin.replace("-","")
            if "-" in display_name or "‐" in display_name:
                display_name = display_name.replace("-","").replace("‐","")
            # print(ids,name_en.lower(),display_name.lower())
            if name_pin.lower().replace(" ","") == display_name.lower().replace(" ",""):
                oa_id = author["id"].split("/")[-1]
                raw_author_name = authorships[i]["raw_author_name"]
                print(oa_id,raw_author_name,ids)

                update_ = 'update paln_list_people set oa_id=%s where id =%s'
                cur.execute(update_, (oa_id,ids,))
                conn.commit()



                # raw_author_name = authorships[i]["raw_author_name"]
                # print(raw_author_name)
    #     results_len = len(data["results"])
    # for i in range(0,results_len):
    #     info = data["results"][i]
    #     long = len(info["affiliations"])
    #     for j in range(0,long):
    #         jigou = info["affiliations"][j]["institution"]["display_name"]
    #         if "Chinese Academy of Engineering" in jigou:
    #             json_info = json.dumps(info)
    #             print(ids,json_info)
    #             update_ = 'update expert_cn set author_info_json=%s,is_json=%s where id =%s'
    #             cur.execute(update_, (json_info, 1, ids,))
    #             conn.commit()
    #             flag = False
    #             break
    #     if flag == False:
    #         break





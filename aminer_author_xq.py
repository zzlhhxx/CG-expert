import time
from until.sql_tools import mysql_db_conn,freeRepeat
from lxml import etree
from urllib.parse import unquote
import random
import requests
import json
import os
import re
from pymongo import MongoClient
import json
from until.sql_tools import mysql_db_conn, getStrAsMD5


# 连接到MongoDB
client = MongoClient("192.168.5.21", 27017)
# 选择数据库
db = client['cg']
# 选择集合（类似于SQL中的表）
collection = db['test']
# 读取数据
# documents = collection.find()

path_html_1 = r'Y:/'

conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
sql = 'select id,aminer_id,html_path,source_id from aminer where  is_ava=1 and source_id>2442 order by id asc limit 3 '
# sql = 'select id,hitsTotal,authfull,inst_name,aminer_path from elsevier_author_career where id =2 '
cur.execute(sql)
data = cur.fetchall() #mysql查詢數據


for item in data:
    ids, aminer_id, html_path,source_id = item #mysql字段
    print(ids)
    print(source_id)
    print(html_path)
    address = path_html_1 + html_path
    # print(address)
    data = open(address, 'r', encoding='utf-8').read()
    json_data = re.findall(r'window.g_initialProps = (.*);', data, )
    # print(json_data[0])
    # print(type(json_data))
    if len(json_data):
        json_data = json_data[0]
        dict_data = json.loads(json_data)
        profile = dict_data['profile']['profile']

        au_name_en= profile['name'] if profile.get('name') else ''  #名字

        au_name_zn=profile['name_zh'] if profile.get('name_zh') else ''


        au_avatar_url= profile['avatar'] if profile.get('avatar') else ''
        print(au_avatar_url)

        au_gender=profile['profile']['gender'] if profile['profile'].get('gender') else ''
        if au_gender=="male":
            au_gender=1
        elif au_gender=="female":
            au_gender=2
        else:
            au_gender=0

        au_dirth_date=profile['au_dirth_date'] if profile.get("au_dirth_date") else ''

        au_resume=profile['profile']['bio'].replace("<br>", '\n').strip() if profile['profile'].get('bio') else ''
        if au_resume=="":
            au_resume=profile['profile']['bio_zh'].replace("<br>", '\n').strip() if profile['profile'].get('bio_zh') else ''

        lang=profile['profile']['lang'] if profile['profile'].get("lang") else ''

        phone=profile['profile']['phone'].strip() if profile['profile'].get("phone") else ''
        email=profile['profile']['email'].strip() if profile['profile'].get("email") else ''
        edu=profile['profile']['edu'] if profile['profile'].get("edu") else ''
        topics=profile['tags'] if profile.get("tags") else []
        last_organs=profile['profile']['affiliation'] if profile['profile'].get("affiliation") else ''
        if last_organs=="":
            last_organs=profile['profile']['affiliation_zh'] if profile['profile'].get("affiliation_zh") else ''

        organs=profile['profile']['edu'] if profile['profile'].get("edu") else ''
        if organs=="":
            organs=profile['profile']['edu_zh'] if profile['profile'].get("edu_zh") else ''
        collection.insert_one({
            "_id": source_id,
            "au_name": au_name_en,
            "au_name_zh": au_name_zn,
            "au_avatar_url": au_avatar_url,
            "au_aliases": '',
            # female 女  male  男 unknown 未知
            "au_gender": au_gender,
            "au_dirth_date":au_dirth_date ,
            "au_country": lang,
            # "lang": profile['profile']['lang'] if profile['profile'].get("lang") else '',
            "au_resume": au_resume,
            "au_phone": phone,
            "au_mail": email,
            "au_edu": edu,
            "au_topics": topics,
            "au_last_organs": last_organs,
            "au_organs": organs,
        })

    else:
        print("无数据")



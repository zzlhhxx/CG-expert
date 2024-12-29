import time

from tools.sql_tools import mysql_db_conn, getStrAsMD5,freeRepeat
import json
import os
from pymongo import MongoClient
from datetime import datetime

# 详情页面
# 连接到MongoDB
client = MongoClient("192.168.5.21", 27017)

# 选择数据库
db = client['cg']

# 选择集合（类似于SQL中的表）
collection = db['zjwl_lw']

# 读取数据
# documents = collection.find()


path_html = r'E:/cg_expert_data/html/aminer_lw/0/0'

conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
while 1:
    t1=time.time()
    sql = 'select id,lw_id,detail_json,is_to_mongo from aminer_lw where  is_to_mongo=0 order by id asc limit 100000 '
    # sql = 'select id,lw_id,detail_json,is_to_mongo from aminer_lw where id =1696  order by id asc limit 1 '
    cur.execute(sql)
    data = cur.fetchall()
    print(len(data))
    if len(data) <1:
        break
    for item in data:
        ids,lw_id,detail_json,is_to_mongo = item
        json_data=json.loads(detail_json)
        # try:
        lw_type=''
        labels=''
        if json_data.get('labels'):
            labels = json_data['labels']
            if labels[0] == 'en_journal' or labels[0] =='cn_journal':
                lw_type='journal'

        title = json_data['title'] if json_data.get('title') else ''  #
        title_zh = json_data['title_zh'] if json_data.get('title_zh') else ''  #
        summary = json_data['abstract'] if json_data.get('abstract') else ''  # 论文 摘要
        keywords = json_data['keywords'] if json_data.get('keywords') else []  # 论文 关键词   String[]
        doi = json_data['doi'] if json_data.get('doi') else ''  # 论文 doi String
        authors = json_data['authors']
        authors_list = []

        for i in authors:
            authors_name = i['name'] if i.get('name') else ''
            authors_organs = i['org'].split(",") if i.get('org') else []
            author_dict = {
                'name': authors_name,
                'organs': authors_organs
            }
            authors_list.append(author_dict)

        pub_date = json_data['year'] if json_data.get('year') else ''  # 论文发表

        cited_count_total = json_data['num_citation']  # 论文引用
        # source="https://www.aminer.cn/pub/"
        lw_id = json_data['id']

        # url_detail=source+lw_id_detail
        lw_location = []
        if json_data.get('urls'):
            for ulr in json_data['urls']:
                lw_location.append(ulr)

        lw_location.append(f'https://www.aminer.cn/pub/{lw_id}')
        source=''
        if json_data.get("venue"):

            venue=json_data['venue']
            if 'info' in str(venue):
                name = venue['info'].get("publisher")
                if name:
                    source = {
                        "name": name,
                        "type": '',
                    }
        insert_dict = {
            '_id': lw_id,
            'title_zn': '',
            'title_en': title,
            'summary': summary,
            'keywords': keywords,
            'doi': doi,
            'type': '',
            'authors': authors_list,
            'source': source,
            'pub_date': pub_date,
            'cited_count_total': cited_count_total,
            'net_address': lw_location,
            '_labels': labels,
        }
        if not collection.find_one({"_id":lw_id}):
            collection.insert_one(insert_dict)
        update_='update aminer_lw set is_to_mongo=1 where id=%s'
        cur.execute(update_,(ids,))
        conn.commit()
        # except Exception as e :
        #     print(e)
        #     print(address)
        #     print(lw_path)
        #     print(in_id)
        #     print("**********")
        #     continue
    t2=time.time()
    print(t2-t1,f'入库数据：{len(data)}')
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



conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
sql = 'select id,aminer_id,lw_path,source_id from oa_lw where is_to_mongo=0 order by id asc '
cur.execute(sql)
data = cur.fetchall()

for item in data:
    in_id, aminer_id, lw_paths, source_id = item

    lw_path_list = lw_paths.split(',,')  # 字符串切割，化为列表
    for lw_path in lw_path_list:
        if not lw_path:
            continue
        address = 'E:/' + lw_path
        try:
            data = open(address, 'r', encoding='utf-8').read()
            json_data = json.loads(data)
            if not json_data['data'][0]['data'].get("hitList"):
                print(json_data)
            else:
                data_lists = json_data['data'][0]['data']['hitList']
                for data_list in data_lists:  # 循环
                    lw_id = data_list['id']
                    repeat_result = freeRepeat('aminer_lw', "lw_id", lw_id, conn)
                    # print(aminer_id)
                    if repeat_result:
                        insert_sql = 'insert into aminer_lw(lw_id,detail_json) value(%s,%s)'
                        cur.execute(insert_sql, (lw_id, json.dumps(data_list,ensure_ascii=False)),)
                        conn.commit()

                labels = data_list['labels'] if data_list.get('labels') else ''  #
                title = data_list['title'] if data_list.get('title') else ''  #
                title_zh = data_list['title_zh'] if data_list.get('title_zh') else ''  #
                summary = data_list['abstract'] if data_list.get('abstract') else ''  # 论文 摘要
                keywords = data_list['keywords'] if data_list.get('keywords') else []  # 论文 关键词   String[]
                doi = data_list['doi'] if data_list.get('doi') else ''  # 论文 doi String
                authors = data_list['authors']
                authors_list = []

                for i in authors:
                    authors_name = i['name'] if i.get('name') else ''
                    authors_organs = i['org'] if i.get('org') else []
                    author_dict = {
                        'name': authors_name,
                        'organs': authors_organs
                    }
                    authors_list.append(author_dict)

                pub_date = data_list['year'] if data_list.get('year') else ''  # 论文发表

                cited_count_total = data_list['num_citation']  # 论文引用
                # source="https://www.aminer.cn/pub/"
                lw_id = data_list['id']

                # url_detail=source+lw_id_detail
                lw_location = []
                if data_list.get('urls'):
                    lw_location.append(data_list['urls'])

                lw_location.append(f'https://www.aminer.cn/pub/{lw_id}')
                source=''
                if data_list.get("venue"):

                    venue=data_list['venue']
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

        except Exception as e :
            print(e)
            print(address)
            print(lw_path)
            print(in_id)
            print("**********")
            continue
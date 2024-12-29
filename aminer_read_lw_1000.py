import re
import time

from until.sql_tools import mysql_db_conn, getStrAsMD5
from until.config import he

from lxml import etree
from urllib.parse import unquote
import random
import requests
import json
import os
from until.sql_tools import mysql_db_conn, getStrAsMD5
from pymongo import MongoClient
from datetime import datetime

# 详情页面
# 连接到MongoDB
client = MongoClient("192.168.5.21", 27017)

# 选择数据库
db = client['cg']

# 选择集合（类似于SQL中的表）
collection = db['zl_table']

# 读取数据
# documents = collection.find()


path_html = r'Y:/cg_expert_data/html/aminer_lw/0/0'

conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
sql = 'select id,aminer_id,lw_path,source_id from aminer where  is_lw=1 and is_ava=1 order by id asc '
cur.execute(sql)
data = cur.fetchall()

for item in data:
    in_id, aminer_id, lw_paths, source_id = item

    lw_path_list = lw_paths.split(',,')  # 字符串切割，化为列表
    for lw_path in lw_path_list:

        address = 'Y:/' + lw_path
        # print(address)
        data = open(address, 'r', encoding='utf-8').read()
        json_data = json.loads(data)

        data_lists = json_data['data'][0]['data']['hitList']

        for i in range(len(data_lists)):  # 循环
            data_list = data_lists[i]
            labels = data_list['labels'] if data_list.get('labels') else ''  #
            title = data_list['title'] if data_list.get('title') else ''  #
            title_zh = data_list['title_zh'] if data_list.get('title_zh') else ''  #
            if title_zh:
                print(title,title_zh)
            summary = data_list['abstract'] if data_list.get('abstract') else ''  # 论文 摘要
            # print(summary)
            # print(type(summary))

            keywords = data_list['keywords'] if data_list.get('keywords') else []  # 论文 关键词   String[]
            # join_keywords=',,'.join(keywords)
            # print(keywords)
            doi = data_list['doi'] if data_list.get('doi') else ''  # 论文 doi String
            # authors_name=data_list['authors']['name'] if data_list.get('name') else ''
            authors = data_list['authors']
            authors_list = []
            for i in authors:
                authors_name = i['name'] if i.get('name') else ''

                authors_organs = i['org'] if i.get('org') else []

                author_dict = {
                    'name': authors_name,
                    'org': authors_organs
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

            insert_dict = {
                'title_zn': '',
                'title_en': title,
                'summary': summary,
                'keywords': keywords,
                'doi': doi,
                'type': '',
                'authors': authors_list,
                'source': [],
                'pub_date': pub_date,
                'cited_count_total': cited_count_total,
                'net_address': lw_location,
                '_labels': labels,
            }

            # collection.insert_one({'_id':})
            # collection.update_one(
            #
            #     {'_id': lw_id_detail},
            #     {'$set': {
            #         'title_zn': '',
            #         'title_en': title,
            #         'summary': summary,
            #         'keywords': keywords,
            #         'doi': doi,
            #         'type':[],
            #         'authors': authors_list,
            #         'source':[],
            #         'pub_date': pub_date,
            #         'cited_count_total': cited_count_total,
            #         'net_address':lw_location,
            #         }
            #     }
            # )

            # num_citation = data_list['num_citation']         # 论文 被引数
            # lang = data_list['lang']
            # data_list = data_list['title']
            # title_zn = data_list['title']
            # abstract = data_list['abstract']                 # 论文 摘要
            # doi = data_list['doi']                           # 论文 doi
            #
            # keywords= data_list['keywords'].get('keywords')                  #论文 关键词
            # join_keywords=',,'.join(keywords)
            #
            # year = data_list['year']                        #论文 发表年份
        #
        #     update_sql = f"insert into  aminer_thesis set source_id,title_en=%s,ttitle_zn=%s,summary=%s,doi=%s,keywords=%s,year=%s  where id=%s"
        #     cur.execute(update_sql, (source_id,title_en,title_zn,abstract,doi,keywords,year,in_id))
        #     conn.commit()

    # tree = etree.HTML(data)
    # print(open(address, 'r', encoding='utf-8').read())
    # json_data=re.findall(r'window.g_initialProps = (.*);',data,)
    # print(json_data)
    # if len([0]):
    #     print('空')
    #     print(in_id,aminer_id)
    #     update_sql = f"update aminer  set profilePubsTotal=%s where id=%s"
    #     cur.execute(update_sql, (0,in_id))
    #     conn.commit()

    # else:
    # 1、读取JSON
    # 2、转化dict

    # formatted_output = json.dumps(dict_data, indent=4, ensure_ascii=False)   #字典 转换为字符串，格式化输出
    # print(formatted_output)
    # profilePubsTotal=dict_data['profile']['profilePubsTotal']   #论文数
    #
    # print(profilePubsTotal)
    #
    # update_sql = f"update aminer_thesis set profilePubsTotal=%s where id=%s"
    # cur.execute(update_sql, (profilePubsTotal, in_id))
    # conn.commit()

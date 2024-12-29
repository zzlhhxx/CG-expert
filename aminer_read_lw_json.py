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

# 详情页面
#


path_html = r'Y:/cg_expert_data/html/aminer_lw/0/0'

conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
sql = 'select id,aminer_id,zl_path,source_id from aminer where  is_zl=1  order by id asc limit 1'
cur.execute(sql)
data = cur.fetchall()

for item in data:
    in_id, source_id, aminer_id,lw_path,profilePubsTotal = item

    # url = f'https://www.aminer.cn/profile/neal-stuart-young-neal-s-young/{aminer_id}'
    # res = requests.get(url, headers=he, timeout=20)
    # if res.status_code == 200:
    #     path = path_html + str(in_id // 10000) + '/' + str(in_id // 100) + '/'
    #     if os.path.exists(path) is False:
    #         os.makedirs(path)
    #     dest_dir = os.path.join(path, str(in_id) + ".html")
    #     with open(dest_dir, 'w', encoding='utf-8') as ff:
    #         ff.write(res.text)
    #         html_path = 'cg_expert_data/'+dest_dir.replace(path_html[0:1] + ":/", "")
    #         update_sql = f"update aminer  set html_path=%s,is_download_html=%s where id = %s"
    #         cur.execute(update_sql, (html_path, 1, in_id))
    #         conn.commit()
    # else:
    #     print(res.text)
    # time.sleep(1)
    # print(html_path)
    address='Y:/'+lw_path

    # print(address)
    print(address)
    data=open(address, 'r', encoding='utf-8').read()
    json_data=json.loads(data)


    data_lists=json_data['data'][0]['data']['hitList']


    # data_list = data_lists[0]
    # keywords = data_list['keywords']
    # join_keywords = ','.join(keywords)
    # print(join_keywords)

    for i in range(len(data_lists)):   #循环
        data_list=data_lists[i]

        num_citation = data_list['num_citation']         # 论文 被引数
        lang = data_list['lang']
        data_list = data_list['title']
        title_zn = data_list['title']
        abstract = data_list['abstract']                 # 论文 摘要
        doi = data_list['doi']                           # 论文 doi

        keywords= data_list['keywords'].get('keywords')                  #论文 关键词
        join_keywords=',,'.join(keywords)

        year = data_list['year']                        #论文 发表年份

        update_sql = f"insert into  aminer_thesis set source_id,title_en=%s,ttitle_zn=%s,summary=%s,doi=%s,keywords=%s,year=%s  where id=%s"
        cur.execute(update_sql, (source_id,title_en,title_zn,abstract,doi,keywords,year,in_id))
        conn.commit()




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
    #1、读取JSON
    #2、转化dict

    # formatted_output = json.dumps(dict_data, indent=4, ensure_ascii=False)   #字典 转换为字符串，格式化输出
    # print(formatted_output)
    # profilePubsTotal=dict_data['profile']['profilePubsTotal']   #论文数
    #
    # print(profilePubsTotal)
    #
        # update_sql = f"update aminer_thesis set profilePubsTotal=%s where id=%s"
        # cur.execute(update_sql, (profilePubsTotal, in_id))
        # conn.commit()
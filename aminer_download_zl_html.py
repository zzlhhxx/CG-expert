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


path_html = r'Z:/html/aminer_html/'

conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
sql = 'select id,aminer_id,zl_path,source_id from aminer where  is_zl=1  order by id asc limit 1'
cur.execute(sql)
data = cur.fetchall()


# for item in data:
#     ids, aminer_id, zl_path,source_id = item #mysql字段
#     zl_path_qs=zl_path.split(',,')
#     for zl_path_q in zl_path_qs:
#
#         # zl_path = 'Y:/' + zl_path_q.replace("cg_expert_data/", '')
#         zl_path = 'Y:\\' + zl_path_q.replace("/","\\")
#         print(zl_path)
#
#         with open(zl_path, 'r', encoding='utf8') as f:
#             json_data = json.load(f)
#         data_item = json_data['data']
#         hitList = data_item['hitList']
#
#         for hit in hitList:
#
#
#             if not hit:
#                 continue
#             abstract_zh=hit['abstract']['zh'] if hit['abstract'].get('zh') else ''
#
#             abstract_en = hit['abstract']['en'] if hit['abstract'].get('en') else ''
#             print(abstract_zh)
#             print(abstract_en)
#             print('*************')







for item in data:
    ids, aminer_id, zl_path,source_id = item
    zl_path_qs = zl_path.split(',,')


    for zl_path_q in zl_path_qs:

            # zl_path = 'Y:/' + zl_path_q.replace("cg_expert_data/", '')
        zl_path = 'Y:\\' + zl_path_q.replace("/", "\\")

        print(zl_path)
        with open(zl_path, 'r', encoding='utf8') as f:
            json_data = json.load(f)

        data_item = json_data['data']
        hitList = data_item['hitList']

        for hit in hitList:

            if not hit:
                continue
            xqy_id = hit['id'] if hit.get('id') else ''
            print(xqy_id)




            # url = f'https://www.aminer.cn/patent/{xqy_id}'
            # res = requests.get(url, headers=he, timeout=20)
            #
            # print(res.text)
            # print(res.status_code )


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


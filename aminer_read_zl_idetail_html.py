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
from pymongo import MongoClient
import json

# 连接到MongoDB
client = MongoClient("192.168.5.21", 27017)

# 选择数据库
db = client['cg']

# 选择集合（类似于SQL中的表）
collection = db['zl_table']

# 读取数据
# documents = collection.find()


path_html = r'Z:/html/aminer_html/'

conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
sql = 'select id,f_id,zl_detail_path,zl_id from aminer_zl where is_donwload_path=1  order by  id asc '
# sql = 'select id,f_id,zl_detail_path,zl_id from aminer_zl where id=48  order by  id asc limit 1000'
cur.execute(sql)
data = cur.fetchall()  # mysql查詢數據

for item in data:
    in_id, f_id, zl_detail_path, zl_id = item

    address = 'Y:/' + zl_detail_path

    # print(address)
    data = open(address, 'r', encoding='utf-8').read()

    json_data = re.findall(r'window.g_initialProps = (.*);', data, )

    # if len([0]):
    #     print('空')
    #     print(in_id,aminer_id)
    #     update_sql = f"update aminer  set profilePubsTotal=%s where id=%s"
    #     cur.execute(update_sql, (0,in_id))
    #     conn.commit()
    #
    # else:

    dict_data = json.loads(json_data[0])
    patents = dict_data['patent']['patent']
    print(patents)

    # list_pub_kind=[]
    # all_kind_versions=patents['pub_kind']   #专利种类
    # print(all_kind_versions)
    # print(type(all_kind_versions))
    # for all_kind_version in all_kind_versions:
    #     # print(type(all_kind_version))   #<class 'dict'>
    #     pub_kind=all_kind_version['pub_kind'] if all_kind_version.get('pub_kind') else ''
    #     print(pub_kind)
    #     print("*********************")
    #     list_pub_kind.append(pub_kind)
    # print(list_pub_kind)
    # str_pub_kind=",,".join(list_pub_kind)
    # print(str_pub_kind)

    # collection.update_one(
    #     {'_id': zl_id},
    #     {'$set': {'kind': all_kind_versions}}
    # )

    abstract = ''
    claims = ''
    title = ''
    for k1, v1 in patents['title'].items():
        title_lang, title = k1, v1[0]

    if patents.get("abstract"):
        for k2, v2 in patents['abstract'].items():
            abstract_lang, abstract = k2, v2[0]

    if patents.get("claims"):
        for k3, v3 in patents['claims'].items():
            claims_lang, claims = k3, v3[0]

    if patents.get("au_last_organs"):
        for k3, v3 in patents['au_last_organs'].items():
            claims_lang, claims = k3, v3[0]

    if patents.get("claims"):
        for k3, v3 in patents['claims'].items():
            claims_lang, claims = k3, v3[0]



    # collection.update_one(
    #
    #     {'_id': zl_id},
    #     {'$set': {
    #         'title': title,
    #         'claim': claims,
    #         'summary': abstract,
    #     },
    #         '$unset': {
    #             'title_zh': "" , # 通过$unset操作符将title_zh字段删除，这里赋空值只是语法要求，实际执行就是删除该字段
    #             'summary_zh': "" , # 通过$unset操作符将title_zh字段删除，这里赋空值只是语法要求，实际执行就是删除该字段
    #             'claim_zh': "" , # 通过$unset操作符将title_zh字段删除，这里赋空值只是语法要求，实际执行就是删除该字段
    #             'title_en': "" , # 通过$unset操作符将title_zh字段删除，这里赋空值只是语法要求，实际执行就是删除该字段
    #             'pub_kind':''
    #         }}
    # )

    # claims_en=patents['claims']['en'] if patents['claims'].get('en') else ''   #权利要求
    # if claims_en != '':
    #     claims_en = "\n".join(claims_en)
    #     # print(claims_en)
    #     # print('********************')
    # claims_zh = patents['claims']['zh'] if patents['claims'].get('zh') else ''
    # if claims_zh != '':
    #     claims_zh = "\n".join(claims_zh)
    #
    # # pub_num = patents['pub_num']        #专利号
    # # pub_kind = patents['pub_kind']     #专利种类
    # # print(pub_kind)
    #
    # # 发明人和发明机构  设置列表append函数放入列表
    # inve_name=[]
    # inve_id=[]
    # inventors = patents['inventor']
    # for inventor in inventors:
    #     inventor_name=inventor['name']
    #     inventor_person_id = inventor['person_id']
    #     appedn_list=inve_name.append(inventor_name)
    #     appedn_list=inve_id.append(inventor_person_id)
    #     # print(inventor_name)
    #     # print(inventor_person_id)
    # inve_name_str=",".join(inve_name)
    # inve_id_str=",".join(inve_id)
    # print(inve_name_str)
    # print(inve_id_str)
    #
    # ipcs = patents['ipc']               #ipc
    # for ipc in ipcs:
    #     ipc_h=ipc['l4']
    #     # print(ipc_h)
    #
    # cpcs = patents['cpc']               #ipc
    # for cpc in cpcs:
    #     cpc_h=cpc['l4']
    #     # print(cpc_h)
    #
    # pub_num = patents['pub_num']  #公开发布号
    # print(pub_num)
    #
    # pub_date = patents['pub_date']['seconds']if patents['pub_date'].get('seconds') else ''
    # print(pub_date)
    #
    # app_num=patents['app_num']      #申请号
    # print(app_num)
    #
    # applicant_names=patents['applicant']        #申请人名
    # for applicant_name in applicant_names:
    #     applicant_name=applicant_name['name']
    #     print(applicant_name)

    # for claims_en in claims_ens:
    #     print(claims_en)
    #     print('********************')

    #
    #     # formatted_output = json.dumps(dict_data, indent=4, ensure_ascii=False)   #字典 转换为字符串，格式化输出
    #
    #     profilePubsTotal=dict_data['profile']['profilePubsTotal']   #论文数
    #
    #     print(profilePubsTotal)
    #
    #     update_sql = f"update aminer  set profilePubsTotal=%s where id=%s"
    #     cur.execute(update_sql, (profilePubsTotal,in_id))
    #     conn.commit()

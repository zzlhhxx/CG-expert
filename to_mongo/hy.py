from tools.sql_tools import mysql_db_conn, getStrAsMD5, freeRepeat
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
collection = db['zjwl_hy']


# 读取数据
# documents = collection.find()


path_html = r'E:/cg_expert_data/html/aminer_lw/0/0'

conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
sql = 'select id,aminer_id,hy_ids_done from nstl_hy where  is_list_dow=1  order by id asc '
cur.execute(sql)
data = cur.fetchall()

for item in data:
    id, aminer_id, hy_ids_done = item
    if hy_ids_done:
        hy_ids_list = hy_ids_done.split(",,")
        for hy_id in hy_ids_list:
            hy_detail_sql = 'select detail_json from ntsl_hy_detail where ntsl_id=%s'
            cur.execute(hy_detail_sql, (hy_id,))
            hy_data = cur.fetchone()
            detail_json, = hy_data
            detail_data = json.loads(detail_json)['data']
            organs=[]
            for v in detail_data:
                # print(v)
                if v['f']=='id':
                    _article_id=v['v']
                if v['f']=='tit':
                    title=v['v'][0]
                if v['f']=='abs':
                    summary=v['v'][0]
                if v['f']=='hasPro':
                    hasprodata=v['v'][0]
                    for haspro in hasprodata:
                        if haspro['f'] =='id':
                            _id=haspro['v']
                        if haspro['f'] =='name':
                            whole_name=haspro['v'][0]
                        if haspro['f'] =='dat':
                            start_date=haspro['v'][0]
                            end_date=haspro['v'][0]
                if v['f']=='hasCrOr':
                    hasdata=v['v']
                    for has in hasdata:
                        for h in has:
                            if h['f'] =='nam':
                                org=h['v'][0]
                                if " & " in org:
                                    org_fuhao_=org.split(" & ")
                                    for fuhao in org_fuhao_:
                                        organs.append(fuhao)
                                else:
                                    organs.append(org)
            au_conference={
                "_id":_article_id,
                "_meeting_id":_id,
                "title":title,
                "summary":summary,
                "keywords":"",
                "whole_name":whole_name,
                "organs":organs,
                "start_date":start_date.replace(" 00:00:00",''),
                "end_date":end_date.replace(" 00:00:00",''),
            }
            if not collection.find_one({"_id":_article_id}):
                collection.insert_one(au_conference)




cc=[{'f': 'id', 'v': '20eeabab4a8607c828f284f585773b09'}, {'f': 'type', 'v': 'ProceedingsPaper'}, {'f': 'score', 'v': 1},
 {'f': 'stpa', 'v': ['253']}, {'f': 'yea', 'v': ['2022']}, {'f': 'syid', 'v': ['20eeabab4a8607c828f284f585773b09']},
 {'f': 'isbn', 'v': ['9781713859741']}, {'f': 'lan', 'v': [{'en': '英语'}]}, {'f': 'acty', 'v': ['nstl']},
 {'f': 'sysuty', 'v': ['C02']}, {'f': 'paid', 'v': ['C20230223001155']}, {'f': 'sysoid', 'v': ['C20230223001155']},
 {'f': 'paco', 'v': ['7']}, {'f': 'syfutefl', 'v': ['0']}, {'f': 'arid', 'v': ['B2ART2023022403030456422K75Y82EL']},
 {'f': 'idse', 'v': ['B2ART2023022403030456422K75Y82EL', 'C20230223001155', '20eeabab4a8607c828f284f585773b09']},
 {'f': 'clco', 'v': [{'TU317': 'TU317'}]}, {'f': 'enpa', 'v': ['259']}, {'f': 'sydotyfl', 'v': ['A70']},
 {'f': 'hasSosysoid', 'v': ['N2023021500017335']}, {'f': 'tit', 'v': [
    'Multifunctional Composite Rebars for Distributed Structural Health Monitoring of Concrete Structures']},
 {'f': 'abs', 'v': [
     'Structural health monitoring (SHM) of reinforced concrete structures is a rapidly developing field with significant advancements over the last decade. Most of the existing SHM systems rely on a large number of point sensors attached to or embedded inside the structures. The sensor network should be densely distributed on the structure or around the potential damage areas for an acceptable damage detection performance. Apparently, this is not an optimal solution for an effective cost. On the other hand, issues such as securing a reliable power supply, cable connections and maintenance costs have remained a major challenge for current distributed SHM systems. To cope with these challenges, we propose a novel concept of multifunctional composite reinforcement rebars with sensing and energy harvesting functionalities for reinforced concrete structures. We develop multifunctional rebars via introducing a triboelectric nanogenerator (TENG) technology into the fabrication process of fiber reinforced polymer (FRP) rebars. The developed rebars with built-in TENG mechanism serve both as nanogenerators and distributed sensing systems under external mechanical vibrations. We perform experiential studies to verify the electrical and mechanical performance of the developed self-powering and self-sensing composite rebars.']},
 {'f': 'hasSo', 'v': [
     [{'f': 'id', 'v': 'N2023021500017335'}, {'f': 'type', 'v': 'Source'}, {'f': 'sysoid', 'v': ['N2023021500017335']},
      {'f': 'tit', 'v': [
          'Structural health monitoring 2021: Enabling next-generation SHM for cyber-physical systems, vol. 1: 13th International Workshop on Structural Health Monitoring (IWSHM), 15-17 March 2022, Stanford, California, USA']}]]},
 {'f': 'hasAut', 'v': [[{'f': 'id', 'v': 'B2CTR20241018041341789XWAM0QTX2X'}, {'f': 'type', 'v': 'People'},
                        {'f': 'nam', 'v': ['QIANYUN ZHANG']}],
                       [{'f': 'id', 'v': 'B2CTR20241018041341789ZNOZVB0VM9'}, {'f': 'type', 'v': 'People'},
                        {'f': 'nam', 'v': ['KAVEH BARRI']}],
                       [{'f': 'id', 'v': 'B2CTR202410180413417892TV3PFYNX7'}, {'f': 'type', 'v': 'People'},
                        {'f': 'nam', 'v': ['ZHONG LIN WANG']}],
                       [{'f': 'id', 'v': 'B2CTR20241018041341789HE1SNQONHR'}, {'f': 'type', 'v': 'People'},
                        {'f': 'nam', 'v': ['AMIR H.ALAVI']}]]},

    {'f': 'hasCrOr', 'v': [

    [{'f': 'id', 'v': 'B2INS20241018041341789NF2L89RTZV'}, {'f': 'type', 'v': 'Organization'}, {'f': 'nam', 'v': [
        'Department of Civil and Environmental Engineering, University of Pittsburgh, Pittsburgh, PA, 15260, USA']}],

    [{'f': 'id', 'v': 'B2INS20241018041341789UJKYTX78AL'}, {'f': 'type', 'v': 'Organization'}, {'f': 'nam', 'v': [
        'School of Materials Science and Engineering, Georgia Institute of Technology, Atlanta, GA 30332, USA & Beijing Institute of Nanoenergy and Nanosystems, Chinese Academy of Sciences, Beijing, 100083, China']}]]},

 {'f': 'hasHol', 'v': [[{'f': 'id', 'v': '95863b5736f11c5db8272243326775ea'}, {'f': 'type', 'v': 'Holding'},
                        {'f': 'lico', 'v': [{'CN111001': '中国科学技术信息研究所'}]}, {'f': 'honu', 'v': ['P2201600']}]]},
 {'f': 'hasPro', 'v': [[{'f': 'id', 'v': 'B2CON2024101804134178938EZZK9JXV'}, {'f': 'type', 'v': 'Proceedings'},
                        {'f': 'dat', 'v': ['2022-03-15 00:00:00']},
                        {'f': 'name', 'v': ['International Workshop on Structural Health Monitoring']},
                        {'f': 'pla', 'v': ['Stanford']}, {'f': 'per', 'v': ['13th']}]]},
 {'f': 'availableOrderType', 'v': '全文申请单'}]

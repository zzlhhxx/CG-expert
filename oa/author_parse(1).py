import re
import time

from tools.sql_tools import mysql_db_conn, getStrAsMD5, freeRepeat, mongo_client
from tools.config import he

from lxml import etree
from urllib.parse import unquote
import random
import requests
import json
import os

conn = mysql_db_conn('12',dbname='cg')
cur = conn.cursor()
mongo_db = mongo_client('cg')



def contrast():
    select_ = 'select id,title,author_info_path from openalex_author_detail where is_download =1 and is_ava=0'
    # select_ = 'select id,title,author_info_path from openalex_author_detail where id=17'
    cur.execute(select_)
    data = cur.fetchall()
    print(len(data))
    index=0
    for item in data:
        index+=1
        ids, title, author_info_path = item

        excel_sql = 'select id,aminer_id,affiliation,affiliationZh from aminer where source_id=%s and is_ava=1'
        cur.execute(excel_sql, (ids,))
        excel_data = cur.fetchone()
        excel_sql_ = 'select id,inst_name from elsevier_author_career where id=%s'
        cur.execute(excel_sql_, (ids,))
        elsevier_data = cur.fetchone()

        aminer_ids,aminer_id,affiliation,affiliationZh = excel_data
        elsevier_id,inst_name = elsevier_data
        inst_name_=inst_name.replace(" University",'').replace(" School of",'').replace(" School",'')
        affiliation_list=affiliation.replace(", ",',').replace(";",',').split(",")
        affiliationZh_list=affiliationZh.replace(", ",';').replace(",",';').split(";")
        affiliation_list=[x.strip() for x in affiliation_list if x.strip() != '']
        affiliationZh_list=[x.strip() for x in affiliationZh_list if x.strip() != '']
        author_info_path = 'Z:/' + author_info_path
        try:
            with open(author_info_path, 'r', encoding='utf8') as f:
                json_data = json.load(f)
            # print(json_data)
            count = json_data['meta']['count']
            results = json_data['results']
            is_true = False
            for i in results:
                oa_id=i["id"]
                affiliations=i['affiliations'] if i.get("affiliations") else ''

                last_known_institutions =i['last_known_institutions'] if  i.get("last_known_institutions") else ''

                # print(affiliations)
                # print('*********')
                # print(last_known_institutions)
                # print('*********')
                # print(affiliation_list)
                # print('*********')
                # print(affiliationZh_list)
                # print('*********')
                if inst_name in str(last_known_institutions):
                    is_true = True
                    print('存在')
                    updage_ = 'update openalex_author_detail set detail_json=%s,is_ava=%s where id =%s'
                    cur.execute(updage_, (json.dumps(i, ensure_ascii=False), 1, ids,))
                    # conn.commit()
                    break
                if inst_name_ in str(last_known_institutions):
                    is_true = True
                    print('存在')
                    updage_ = 'update openalex_author_detail set detail_json=%s,is_ava=%s where id =%s'
                    cur.execute(updage_, (json.dumps(i, ensure_ascii=False), 1, ids,))
                    # conn.commit()
                    break

                for g in affiliation_list:
                    if g in str(last_known_institutions):
                        is_true = True
                        print('存在')
                        updage_ = 'update openalex_author_detail set detail_json=%s,is_ava=%s where id =%s'
                        cur.execute(updage_, (json.dumps(i, ensure_ascii=False), 1, ids,))
                        # conn.commit()
                        break
                if is_true:
                    break
                for t in affiliationZh_list:
                    if  t in str(last_known_institutions):
                        is_true = True
                        print('存在')
                        updage_ = 'update openalex_author_detail set detail_json=%s,is_ava=%s where id =%s'
                        cur.execute(updage_,(json.dumps(i,ensure_ascii=False),1,ids,))
                        # conn.commit()
                        break
                if is_true:
                    break
            if not is_true:
                print(author_info_path)
                print(ids, count, '不在')
        except Exception as e :
            print(e)
            continue
        if index %100==0:
            print('提交实物啦')
            conn.commit()
    conn.commit()








def parse_json():
    #au_last_organs_zh
    #au_organs_zh
    c=mongo_db['author_table']
    data=c.find()

    for item in data:
        _id=item['_id']
        is_synced=item['is_synced']
        # au_resume = item['au_resume']
        # au_resume_cn = item['au_resume_cn']
        # au_organs_zh = item['au_organs_zh']
        # au_organs = item['au_organs']
        # au_last_organs_zh = item['au_last_organs_zh']
        # au_last_organs = item['au_last_organs']


        # if is_synced !=1:
        #
        #     if au_organs_zh:
        #         au_organs=au_organs_zh
        #     if au_last_organs_zh:
        #
        #         au_last_organs=au_last_organs_zh


        # if au_resume_cn:
        #     au_resume=au_resume_cn.replace("\n\n",'\n').replace("\n\t",'\n').replace("\n ",'\n').replace("\t",'')
        # c.update_one(
        #
        #             {'_id': _id},
        #             {'$set': {
        #                 'au_resume': au_resume,
        #                 'au_organs': au_organs,
        #                 'au_last_organs': au_last_organs,
        #             },
        #                 '$unset': {
        #                     'au_resume_cn': "",  # 通过$unset操作符将title_zh字段删除，这里赋空值只是语法要求，实际执行就是删除该字段
        #                     'au_last_organs_zh': "",  # 通过$unset操作符将title_zh字段删除，这里赋空值只是语法要求，实际执行就是删除该字段
        #                     'au_organs_zh': "",  # 通过$unset操作符将title_zh字段删除，这里赋空值只是语法要求，实际执行就是删除该字段
        #                 }}
        #         )

        excel_sql='select cntry from elsevier_author_career where id =%s'

        cur.execute(excel_sql,(_id,))

        cntry,=cur.fetchone()

        conn.commit()

        c.update_one({"_id": _id}, {'$set': {'cntry': cntry}})




        # select_ = 'select id,detail_json,is_ava from openalex_author_detail where  id=%s'
        #
        # cur.execute(select_,(_id,))
        #
        # openalex_data = cur.fetchone()
        # openalex_id, detail_json, is_ava=openalex_data
        # if is_ava==1:
        #     json_data=json.loads(detail_json)
        #     display_name_alternatives = json_data['display_name_alternatives']
        #     h_index = json_data['summary_stats']['h_index']
        #     i10_index = json_data['summary_stats']['i10_index']
        #     affiliations = json_data['affiliations']
        #     last_known_institutions = json_data['last_known_institutions']
        #     au_organs=[]
        #     au_last_organs=[]
        #     for a in affiliations:
        #         name = a['institution']['display_name']
        #         country = a['institution']['country_code']
        #         type = a['institution']['type']
        #         years = a['years']
        #         au_organs.append({
        #             "name": name,
        #             "country": country,
        #             "type": type,
        #             "years": years,
        #             "position": '',
        #         })
        #     for last in last_known_institutions:
        #         name = last['display_name']
        #         au_last_organs.append({
        #             "name": last['display_name'],
        #             "position": ''
        #         })
        #
        #     c.update_one(
        #
        #         {'_id': _id},
        #         {'$set': {
        #             'au_aliases': display_name_alternatives,
        #             'h_index': h_index,
        #             'i10_index': i10_index,
        #             'au_last_organs': au_last_organs,
        #             'au_organs': au_organs,
        #             "is_synced":1,
        #         },
        #             '$unset': {
        #                 'lang': "",  # 通过$unset操作符将title_zh字段删除，这里赋空值只是语法要求，实际执行就是删除该字段
        #             }}
        #     )
        #
        # else:
        #     c.update_one(
        #
        #         {'_id': _id},
        #         {'$set': {
        #             'cntry': cntry,
        #             'h_index': '',
        #             'i10_index': '',
        #             "is_synced": -1,
        #         },
        #             '$unset': {
        #                 'lang': "",  # 通过$unset操作符将title_zh字段删除，这里赋空值只是语法要求，实际执行就是删除该字段
        #             }}
        #     )

contrast()

# parse_json()
a = {"id": "https://openalex.org/A5100376569",
     "ids": {"orcid": "https://orcid.org/0000-0002-5530-0380", "openalex": "https://openalex.org/A5100376569"},
     "orcid": "https://orcid.org/0000-0002-5530-0380", "topics": [{"id": "https://openalex.org/T10338", "count": 1934,
                                                                   "field": {"id": "https://openalex.org/fields/22",
                                                                             "display_name": "Engineering"},
                                                                   "domain": {"id": "https://openalex.org/domains/3",
                                                                              "display_name": "Physical Sciences"},
                                                                   "subfield": {
                                                                       "id": "https://openalex.org/subfields/2204",
                                                                       "display_name": "Biomedical Engineering"},
                                                                   "display_name": "Wearable Nanogenerator Technology"},
                                                                  {"id": "https://openalex.org/T10660", "count": 1199,
                                                                   "field": {"id": "https://openalex.org/fields/25",
                                                                             "display_name": "Materials Science"},
                                                                   "domain": {"id": "https://openalex.org/domains/3",
                                                                              "display_name": "Physical Sciences"},
                                                                   "subfield": {
                                                                       "id": "https://openalex.org/subfields/2507",
                                                                       "display_name": "Polymers and Plastics"},
                                                                   "display_name": "Conducting Polymer Research"},
                                                                  {"id": "https://openalex.org/T11230", "count": 465,
                                                                   "field": {"id": "https://openalex.org/fields/22",
                                                                             "display_name": "Engineering"},
                                                                   "domain": {"id": "https://openalex.org/domains/3",
                                                                              "display_name": "Physical Sciences"},
                                                                   "subfield": {
                                                                       "id": "https://openalex.org/subfields/2210",
                                                                       "display_name": "Mechanical Engineering"},
                                                                   "display_name": "Vibration Energy Harvesting for Microsystems Applications"},
                                                                  {"id": "https://openalex.org/T10179", "count": 378,
                                                                   "field": {"id": "https://openalex.org/fields/25",
                                                                             "display_name": "Materials Science"},
                                                                   "domain": {"id": "https://openalex.org/domains/3",
                                                                              "display_name": "Physical Sciences"},
                                                                   "subfield": {
                                                                       "id": "https://openalex.org/subfields/2504",
                                                                       "display_name": "Electronic, Optical and Magnetic Materials"},
                                                                   "display_name": "Materials for Electrochemical Supercapacitors"},
                                                                  {"id": "https://openalex.org/T10914", "count": 372,
                                                                   "field": {"id": "https://openalex.org/fields/28",
                                                                             "display_name": "Neuroscience"},
                                                                   "domain": {"id": "https://openalex.org/domains/1",
                                                                              "display_name": "Life Sciences"},
                                                                   "subfield": {
                                                                       "id": "https://openalex.org/subfields/2805",
                                                                       "display_name": "Cognitive Neuroscience"},
                                                                   "display_name": "Tactile Perception and Cross-modal Plasticity"},
                                                                  {"id": "https://openalex.org/T10090", "count": 363,
                                                                   "field": {"id": "https://openalex.org/fields/25",
                                                                             "display_name": "Materials Science"},
                                                                   "domain": {"id": "https://openalex.org/domains/3",
                                                                              "display_name": "Physical Sciences"},
                                                                   "subfield": {
                                                                       "id": "https://openalex.org/subfields/2505",
                                                                       "display_name": "Materials Chemistry"},
                                                                   "display_name": "Zinc Oxide Nanostructures"},
                                                                  {"id": "https://openalex.org/T10461", "count": 339,
                                                                   "field": {"id": "https://openalex.org/fields/22",
                                                                             "display_name": "Engineering"},
                                                                   "domain": {"id": "https://openalex.org/domains/3",
                                                                              "display_name": "Physical Sciences"},
                                                                   "subfield": {
                                                                       "id": "https://openalex.org/subfields/2208",
                                                                       "display_name": "Electrical and Electronic Engineering"},
                                                                   "display_name": "Gas Sensing Technology and Materials"},
                                                                  {"id": "https://openalex.org/T11272", "count": 229,
                                                                   "field": {"id": "https://openalex.org/fields/22",
                                                                             "display_name": "Engineering"},
                                                                   "domain": {"id": "https://openalex.org/domains/3",
                                                                              "display_name": "Physical Sciences"},
                                                                   "subfield": {
                                                                       "id": "https://openalex.org/subfields/2204",
                                                                       "display_name": "Biomedical Engineering"},
                                                                   "display_name": "Nanowire Nanosensors for Biomedical and Energy Applications"},
                                                                  {"id": "https://openalex.org/T10321", "count": 132,
                                                                   "field": {"id": "https://openalex.org/fields/25",
                                                                             "display_name": "Materials Science"},
                                                                   "domain": {"id": "https://openalex.org/domains/3",
                                                                              "display_name": "Physical Sciences"},
                                                                   "subfield": {
                                                                       "id": "https://openalex.org/subfields/2505",
                                                                       "display_name": "Materials Chemistry"},
                                                                   "display_name": "Applications of Quantum Dots in Nanotechnology"},
                                                                  {"id": "https://openalex.org/T10247", "count": 130,
                                                                   "field": {"id": "https://openalex.org/fields/22",
                                                                             "display_name": "Engineering"},
                                                                   "domain": {"id": "https://openalex.org/domains/3",
                                                                              "display_name": "Physical Sciences"},
                                                                   "subfield": {
                                                                       "id": "https://openalex.org/subfields/2208",
                                                                       "display_name": "Electrical and Electronic Engineering"},
                                                                   "display_name": "Perovskite Solar Cell Technology"},
                                                                  {"id": "https://openalex.org/T11737", "count": 102,
                                                                   "field": {"id": "https://openalex.org/fields/22",
                                                                             "display_name": "Engineering"},
                                                                   "domain": {"id": "https://openalex.org/domains/3",
                                                                              "display_name": "Physical Sciences"},
                                                                   "subfield": {
                                                                       "id": "https://openalex.org/subfields/2210",
                                                                       "display_name": "Mechanical Engineering"},
                                                                   "display_name": "4D Printing Technologies"},
                                                                  {"id": "https://openalex.org/T11608", "count": 101,
                                                                   "field": {"id": "https://openalex.org/fields/22",
                                                                             "display_name": "Engineering"},
                                                                   "domain": {"id": "https://openalex.org/domains/3",
                                                                              "display_name": "Physical Sciences"},
                                                                   "subfield": {
                                                                       "id": "https://openalex.org/subfields/2204",
                                                                       "display_name": "Biomedical Engineering"},
                                                                   "display_name": "Dielectric Elastomer Materials and Applications"},
                                                                  {"id": "https://openalex.org/T12039", "count": 99,
                                                                   "field": {"id": "https://openalex.org/fields/25",
                                                                             "display_name": "Materials Science"},
                                                                   "domain": {"id": "https://openalex.org/domains/3",
                                                                              "display_name": "Physical Sciences"},
                                                                   "subfield": {
                                                                       "id": "https://openalex.org/subfields/2508",
                                                                       "display_name": "Surfaces, Coatings and Films"},
                                                                   "display_name": "Surface Analysis and Electron Spectroscopy Techniques"},
                                                                  {"id": "https://openalex.org/T11392", "count": 93,
                                                                   "field": {"id": "https://openalex.org/fields/22",
                                                                             "display_name": "Engineering"},
                                                                   "domain": {"id": "https://openalex.org/domains/3",
                                                                              "display_name": "Physical Sciences"},
                                                                   "subfield": {
                                                                       "id": "https://openalex.org/subfields/2208",
                                                                       "display_name": "Electrical and Electronic Engineering"},
                                                                   "display_name": "Wireless Energy Harvesting and Information Transfer"},
                                                                  {"id": "https://openalex.org/T12529", "count": 90,
                                                                   "field": {"id": "https://openalex.org/fields/25",
                                                                             "display_name": "Materials Science"},
                                                                   "domain": {"id": "https://openalex.org/domains/3",
                                                                              "display_name": "Physical Sciences"},
                                                                   "subfield": {
                                                                       "id": "https://openalex.org/subfields/2504",
                                                                       "display_name": "Electronic, Optical and Magnetic Materials"},
                                                                   "display_name": "Gallium Oxide (Ga2O3) Semiconductor Materials and Devices"},
                                                                  {"id": "https://openalex.org/T10099", "count": 90,
                                                                   "field": {"id": "https://openalex.org/fields/31",
                                                                             "display_name": "Physics and Astronomy"},
                                                                   "domain": {"id": "https://openalex.org/domains/3",
                                                                              "display_name": "Physical Sciences"},
                                                                   "subfield": {
                                                                       "id": "https://openalex.org/subfields/3104",
                                                                       "display_name": "Condensed Matter Physics"},
                                                                   "display_name": "First-Principles Calculations for III-Nitride Semiconductors"},
                                                                  {"id": "https://openalex.org/T10784", "count": 77,
                                                                   "field": {"id": "https://openalex.org/fields/22",
                                                                             "display_name": "Engineering"},
                                                                   "domain": {"id": "https://openalex.org/domains/3",
                                                                              "display_name": "Physical Sciences"},
                                                                   "subfield": {
                                                                       "id": "https://openalex.org/subfields/2204",
                                                                       "display_name": "Biomedical Engineering"},
                                                                   "display_name": "Analysis of Electromyography Signal Processing"},
                                                                  {"id": "https://openalex.org/T10074", "count": 74,
                                                                   "field": {"id": "https://openalex.org/fields/25",
                                                                             "display_name": "Materials Science"},
                                                                   "domain": {"id": "https://openalex.org/domains/3",
                                                                              "display_name": "Physical Sciences"},
                                                                   "subfield": {
                                                                       "id": "https://openalex.org/subfields/2505",
                                                                       "display_name": "Materials Chemistry"},
                                                                   "display_name": "Carbon Nanotubes and their Applications"},
                                                                  {"id": "https://openalex.org/T10502", "count": 71,
                                                                   "field": {"id": "https://openalex.org/fields/22",
                                                                             "display_name": "Engineering"},
                                                                   "domain": {"id": "https://openalex.org/domains/3",
                                                                              "display_name": "Physical Sciences"},
                                                                   "subfield": {
                                                                       "id": "https://openalex.org/subfields/2208",
                                                                       "display_name": "Electrical and Electronic Engineering"},
                                                                   "display_name": "Memristive Devices for Neuromorphic Computing"},
                                                                  {"id": "https://openalex.org/T11907", "count": 70,
                                                                   "field": {"id": "https://openalex.org/fields/25",
                                                                             "display_name": "Materials Science"},
                                                                   "domain": {"id": "https://openalex.org/domains/3",
                                                                              "display_name": "Physical Sciences"},
                                                                   "subfield": {
                                                                       "id": "https://openalex.org/subfields/2505",
                                                                       "display_name": "Materials Chemistry"},
                                                                   "display_name": "Formation and Properties of Nanocrystals and Nanostructures"},
                                                                  {"id": "https://openalex.org/T10131", "count": 69,
                                                                   "field": {"id": "https://openalex.org/fields/25",
                                                                             "display_name": "Materials Science"},
                                                                   "domain": {"id": "https://openalex.org/domains/3",
                                                                              "display_name": "Physical Sciences"},
                                                                   "subfield": {
                                                                       "id": "https://openalex.org/subfields/2504",
                                                                       "display_name": "Electronic, Optical and Magnetic Materials"},
                                                                   "display_name": "Plasmonic Nanoparticles: Synthesis, Properties, and Applications"},
                                                                  {"id": "https://openalex.org/T11160", "count": 67,
                                                                   "field": {"id": "https://openalex.org/fields/22",
                                                                             "display_name": "Engineering"},
                                                                   "domain": {"id": "https://openalex.org/domains/3",
                                                                              "display_name": "Physical Sciences"},
                                                                   "subfield": {
                                                                       "id": "https://openalex.org/subfields/2204",
                                                                       "display_name": "Biomedical Engineering"},
                                                                   "display_name": "Acoustic Wave Biosensors and Thin Film Resonators"},
                                                                  {"id": "https://openalex.org/T10857", "count": 66,
                                                                   "field": {"id": "https://openalex.org/fields/13",
                                                                             "display_name": "Biochemistry, Genetics and Molecular Biology"},
                                                                   "domain": {"id": "https://openalex.org/domains/1",
                                                                              "display_name": "Life Sciences"},
                                                                   "subfield": {
                                                                       "id": "https://openalex.org/subfields/1315",
                                                                       "display_name": "Structural Biology"},
                                                                   "display_name": "Cryo-Electron Microscopy Techniques"},
                                                                  {"id": "https://openalex.org/T11449", "count": 62,
                                                                   "field": {"id": "https://openalex.org/fields/31",
                                                                             "display_name": "Physics and Astronomy"},
                                                                   "domain": {"id": "https://openalex.org/domains/3",
                                                                              "display_name": "Physical Sciences"},
                                                                   "subfield": {
                                                                       "id": "https://openalex.org/subfields/3107",
                                                                       "display_name": "Atomic and Molecular Physics, and Optics"},
                                                                   "display_name": "Cavity Optomechanics and Nanomechanical Systems"},
                                                                  {"id": "https://openalex.org/T12588", "count": 61,
                                                                   "field": {"id": "https://openalex.org/fields/25",
                                                                             "display_name": "Materials Science"},
                                                                   "domain": {"id": "https://openalex.org/domains/3",
                                                                              "display_name": "Physical Sciences"},
                                                                   "subfield": {
                                                                       "id": "https://openalex.org/subfields/2505",
                                                                       "display_name": "Materials Chemistry"},
                                                                   "display_name": "Emergent Phenomena at Oxide Interfaces"}],
     "x_concepts": [{"id": "https://openalex.org/C121332964", "level": 0, "score": 89.7,
                     "wikidata": "https://www.wikidata.org/wiki/Q413", "display_name": "Physics"},
                    {"id": "https://openalex.org/C192562407", "level": 0, "score": 86.5,
                     "wikidata": "https://www.wikidata.org/wiki/Q228736", "display_name": "Materials science"},
                    {"id": "https://openalex.org/C62520636", "level": 1, "score": 83.8,
                     "wikidata": "https://www.wikidata.org/wiki/Q944", "display_name": "Quantum mechanics"},
                    {"id": "https://openalex.org/C127413603", "level": 0, "score": 81.1,
                     "wikidata": "https://www.wikidata.org/wiki/Q11023", "display_name": "Engineering"},
                    {"id": "https://openalex.org/C185592680", "level": 0, "score": 78.4,
                     "wikidata": "https://www.wikidata.org/wiki/Q2329", "display_name": "Chemistry"},
                    {"id": "https://openalex.org/C159985019", "level": 1, "score": 66.6,
                     "wikidata": "https://www.wikidata.org/wiki/Q181790", "display_name": "Composite material"},
                    {"id": "https://openalex.org/C171250308", "level": 1, "score": 56.9,
                     "wikidata": "https://www.wikidata.org/wiki/Q11468", "display_name": "Nanotechnology"},
                    {"id": "https://openalex.org/C119599485", "level": 1, "score": 55.9,
                     "wikidata": "https://www.wikidata.org/wiki/Q43035", "display_name": "Electrical engineering"},
                    {"id": "https://openalex.org/C147789679", "level": 1, "score": 48.9,
                     "wikidata": "https://www.wikidata.org/wiki/Q11372", "display_name": "Physical chemistry"},
                    {"id": "https://openalex.org/C49040817", "level": 1, "score": 45.8,
                     "wikidata": "https://www.wikidata.org/wiki/Q193091", "display_name": "Optoelectronics"},
                    {"id": "https://openalex.org/C178790620", "level": 1, "score": 42,
                     "wikidata": "https://www.wikidata.org/wiki/Q11351", "display_name": "Organic chemistry"},
                    {"id": "https://openalex.org/C41008148", "level": 0, "score": 41.2,
                     "wikidata": "https://www.wikidata.org/wiki/Q21198", "display_name": "Computer science"},
                    {"id": "https://openalex.org/C97355855", "level": 1, "score": 41.1,
                     "wikidata": "https://www.wikidata.org/wiki/Q11473", "display_name": "Thermodynamics"},
                    {"id": "https://openalex.org/C24890656", "level": 1, "score": 38.4,
                     "wikidata": "https://www.wikidata.org/wiki/Q82811", "display_name": "Acoustics"},
                    {"id": "https://openalex.org/C165801399", "level": 2, "score": 36.5,
                     "wikidata": "https://www.wikidata.org/wiki/Q25428", "display_name": "Voltage"},
                    {"id": "https://openalex.org/C33923547", "level": 0, "score": 36.3,
                     "wikidata": "https://www.wikidata.org/wiki/Q395", "display_name": "Mathematics"},
                    {"id": "https://openalex.org/C86803240", "level": 0, "score": 36.1,
                     "wikidata": "https://www.wikidata.org/wiki/Q420", "display_name": "Biology"},
                    {"id": "https://openalex.org/C80640880", "level": 2, "score": 35.4,
                     "wikidata": "https://www.wikidata.org/wiki/Q876377", "display_name": "Triboelectric effect"},
                    {"id": "https://openalex.org/C100082104", "level": 2, "score": 34.6,
                     "wikidata": "https://www.wikidata.org/wiki/Q183759", "display_name": "Piezoelectricity"},
                    {"id": "https://openalex.org/C175616097", "level": 3, "score": 29.7,
                     "wikidata": "https://www.wikidata.org/wiki/Q6964048", "display_name": "Nanogenerator"},
                    {"id": "https://openalex.org/C120665830", "level": 1, "score": 27.6,
                     "wikidata": "https://www.wikidata.org/wiki/Q14620", "display_name": "Optics"},
                    {"id": "https://openalex.org/C163258240", "level": 2, "score": 26.8,
                     "wikidata": "https://www.wikidata.org/wiki/Q25342", "display_name": "Power (physics)"},
                    {"id": "https://openalex.org/C42360764", "level": 1, "score": 26.7,
                     "wikidata": "https://www.wikidata.org/wiki/Q83588", "display_name": "Chemical engineering"},
                    {"id": "https://openalex.org/C105795698", "level": 1, "score": 24.5,
                     "wikidata": "https://www.wikidata.org/wiki/Q12483", "display_name": "Statistics"},
                    {"id": "https://openalex.org/C186370098", "level": 2, "score": 20.6,
                     "wikidata": "https://www.wikidata.org/wiki/Q442787",
                     "display_name": "Energy (signal processing)"}], "topic_share": [
        {"id": "https://openalex.org/T11230",
         "field": {"id": "https://openalex.org/fields/22", "display_name": "Engineering"}, "value": 0.0089511,
         "domain": {"id": "https://openalex.org/domains/3", "display_name": "Physical Sciences"},
         "subfield": {"id": "https://openalex.org/subfields/2210", "display_name": "Mechanical Engineering"},
         "display_name": "Vibration Energy Harvesting for Microsystems Applications"},
        {"id": "https://openalex.org/T10338",
         "field": {"id": "https://openalex.org/fields/22", "display_name": "Engineering"}, "value": 0.0070653,
         "domain": {"id": "https://openalex.org/domains/3", "display_name": "Physical Sciences"},
         "subfield": {"id": "https://openalex.org/subfields/2204", "display_name": "Biomedical Engineering"},
         "display_name": "Wearable Nanogenerator Technology"}, {"id": "https://openalex.org/T10660",
                                                                "field": {"id": "https://openalex.org/fields/25",
                                                                          "display_name": "Materials Science"},
                                                                "value": 0.0029876,
                                                                "domain": {"id": "https://openalex.org/domains/3",
                                                                           "display_name": "Physical Sciences"},
                                                                "subfield": {
                                                                    "id": "https://openalex.org/subfields/2507",
                                                                    "display_name": "Polymers and Plastics"},
                                                                "display_name": "Conducting Polymer Research"},
        {"id": "https://openalex.org/T10914",
         "field": {"id": "https://openalex.org/fields/28", "display_name": "Neuroscience"}, "value": 0.0027175,
         "domain": {"id": "https://openalex.org/domains/1", "display_name": "Life Sciences"},
         "subfield": {"id": "https://openalex.org/subfields/2805", "display_name": "Cognitive Neuroscience"},
         "display_name": "Tactile Perception and Cross-modal Plasticity"}, {"id": "https://openalex.org/T11272",
                                                                            "field": {
                                                                                "id": "https://openalex.org/fields/22",
                                                                                "display_name": "Engineering"},
                                                                            "value": 0.0017853, "domain": {
                "id": "https://openalex.org/domains/3", "display_name": "Physical Sciences"}, "subfield": {
                "id": "https://openalex.org/subfields/2204", "display_name": "Biomedical Engineering"},
                                                                            "display_name": "Nanowire Nanosensors for Biomedical and Energy Applications"},
        {"id": "https://openalex.org/T10179",
         "field": {"id": "https://openalex.org/fields/25", "display_name": "Materials Science"}, "value": 0.0017428,
         "domain": {"id": "https://openalex.org/domains/3", "display_name": "Physical Sciences"},
         "subfield": {"id": "https://openalex.org/subfields/2504",
                      "display_name": "Electronic, Optical and Magnetic Materials"},
         "display_name": "Materials for Electrochemical Supercapacitors"}, {"id": "https://openalex.org/T11608",
                                                                            "field": {
                                                                                "id": "https://openalex.org/fields/22",
                                                                                "display_name": "Engineering"},
                                                                            "value": 0.001546, "domain": {
                "id": "https://openalex.org/domains/3", "display_name": "Physical Sciences"}, "subfield": {
                "id": "https://openalex.org/subfields/2204", "display_name": "Biomedical Engineering"},
                                                                            "display_name": "Dielectric Elastomer Materials and Applications"},
        {"id": "https://openalex.org/T10090",
         "field": {"id": "https://openalex.org/fields/25", "display_name": "Materials Science"}, "value": 0.0015097,
         "domain": {"id": "https://openalex.org/domains/3", "display_name": "Physical Sciences"},
         "subfield": {"id": "https://openalex.org/subfields/2505", "display_name": "Materials Chemistry"},
         "display_name": "Zinc Oxide Nanostructures"}, {"id": "https://openalex.org/T11737",
                                                        "field": {"id": "https://openalex.org/fields/22",
                                                                  "display_name": "Engineering"}, "value": 0.0011299,
                                                        "domain": {"id": "https://openalex.org/domains/3",
                                                                   "display_name": "Physical Sciences"},
                                                        "subfield": {"id": "https://openalex.org/subfields/2210",
                                                                     "display_name": "Mechanical Engineering"},
                                                        "display_name": "4D Printing Technologies"},
        {"id": "https://openalex.org/T10461",
         "field": {"id": "https://openalex.org/fields/22", "display_name": "Engineering"}, "value": 0.0010927,
         "domain": {"id": "https://openalex.org/domains/3", "display_name": "Physical Sciences"},
         "subfield": {"id": "https://openalex.org/subfields/2208",
                      "display_name": "Electrical and Electronic Engineering"},
         "display_name": "Gas Sensing Technology and Materials"}, {"id": "https://openalex.org/T12529",
                                                                   "field": {"id": "https://openalex.org/fields/25",
                                                                             "display_name": "Materials Science"},
                                                                   "value": 0.0008807,
                                                                   "domain": {"id": "https://openalex.org/domains/3",
                                                                              "display_name": "Physical Sciences"},
                                                                   "subfield": {
                                                                       "id": "https://openalex.org/subfields/2504",
                                                                       "display_name": "Electronic, Optical and Magnetic Materials"},
                                                                   "display_name": "Gallium Oxide (Ga2O3) Semiconductor Materials and Devices"},
        {"id": "https://openalex.org/T10857", "field": {"id": "https://openalex.org/fields/13",
                                                        "display_name": "Biochemistry, Genetics and Molecular Biology"},
         "value": 0.0007957, "domain": {"id": "https://openalex.org/domains/1", "display_name": "Life Sciences"},
         "subfield": {"id": "https://openalex.org/subfields/1315", "display_name": "Structural Biology"},
         "display_name": "Cryo-Electron Microscopy Techniques"}, {"id": "https://openalex.org/T14318",
                                                                  "field": {"id": "https://openalex.org/fields/16",
                                                                            "display_name": "Chemistry"},
                                                                  "value": 0.0007631,
                                                                  "domain": {"id": "https://openalex.org/domains/3",
                                                                             "display_name": "Physical Sciences"},
                                                                  "subfield": {
                                                                      "id": "https://openalex.org/subfields/1605",
                                                                      "display_name": "Organic Chemistry"},
                                                                  "display_name": "Polydiacetylene Supramolecular Chemosensors"},
        {"id": "https://openalex.org/T10247",
         "field": {"id": "https://openalex.org/fields/22", "display_name": "Engineering"}, "value": 0.0007584,
         "domain": {"id": "https://openalex.org/domains/3", "display_name": "Physical Sciences"},
         "subfield": {"id": "https://openalex.org/subfields/2208",
                      "display_name": "Electrical and Electronic Engineering"},
         "display_name": "Perovskite Solar Cell Technology"}, {"id": "https://openalex.org/T11523",
                                                               "field": {"id": "https://openalex.org/fields/22",
                                                                         "display_name": "Engineering"},
                                                               "value": 0.0005598,
                                                               "domain": {"id": "https://openalex.org/domains/3",
                                                                          "display_name": "Physical Sciences"},
                                                               "subfield": {"id": "https://openalex.org/subfields/2208",
                                                                            "display_name": "Electrical and Electronic Engineering"},
                                                               "display_name": "Emerging Transparent Electrodes for Flexible Electronics"},
        {"id": "https://openalex.org/T10321",
         "field": {"id": "https://openalex.org/fields/25", "display_name": "Materials Science"}, "value": 0.0005194,
         "domain": {"id": "https://openalex.org/domains/3", "display_name": "Physical Sciences"},
         "subfield": {"id": "https://openalex.org/subfields/2505", "display_name": "Materials Chemistry"},
         "display_name": "Applications of Quantum Dots in Nanotechnology"}, {"id": "https://openalex.org/T10275",
                                                                             "field": {
                                                                                 "id": "https://openalex.org/fields/25",
                                                                                 "display_name": "Materials Science"},
                                                                             "value": 0.0005087, "domain": {
                "id": "https://openalex.org/domains/3", "display_name": "Physical Sciences"}, "subfield": {
                "id": "https://openalex.org/subfields/2505", "display_name": "Materials Chemistry"},
                                                                             "display_name": "Two-Dimensional Materials"},
        {"id": "https://openalex.org/T11907",
         "field": {"id": "https://openalex.org/fields/25", "display_name": "Materials Science"}, "value": 0.0005018,
         "domain": {"id": "https://openalex.org/domains/3", "display_name": "Physical Sciences"},
         "subfield": {"id": "https://openalex.org/subfields/2505", "display_name": "Materials Chemistry"},
         "display_name": "Formation and Properties of Nanocrystals and Nanostructures"},
        {"id": "https://openalex.org/T10099",
         "field": {"id": "https://openalex.org/fields/31", "display_name": "Physics and Astronomy"}, "value": 0.0005008,
         "domain": {"id": "https://openalex.org/domains/3", "display_name": "Physical Sciences"},
         "subfield": {"id": "https://openalex.org/subfields/3104", "display_name": "Condensed Matter Physics"},
         "display_name": "First-Principles Calculations for III-Nitride Semiconductors"},
        {"id": "https://openalex.org/T10131",
         "field": {"id": "https://openalex.org/fields/25", "display_name": "Materials Science"}, "value": 0.0004898,
         "domain": {"id": "https://openalex.org/domains/3", "display_name": "Physical Sciences"},
         "subfield": {"id": "https://openalex.org/subfields/2504",
                      "display_name": "Electronic, Optical and Magnetic Materials"},
         "display_name": "Plasmonic Nanoparticles: Synthesis, Properties, and Applications"},
        {"id": "https://openalex.org/T12238",
         "field": {"id": "https://openalex.org/fields/22", "display_name": "Engineering"}, "value": 0.0004825,
         "domain": {"id": "https://openalex.org/domains/3", "display_name": "Physical Sciences"},
         "subfield": {"id": "https://openalex.org/subfields/2208",
                      "display_name": "Electrical and Electronic Engineering"},
         "display_name": "Energy Consumption in Mobile Devices and Networks"}, {"id": "https://openalex.org/T11392",
                                                                                "field": {
                                                                                    "id": "https://openalex.org/fields/22",
                                                                                    "display_name": "Engineering"},
                                                                                "value": 0.0004673, "domain": {
                "id": "https://openalex.org/domains/3", "display_name": "Physical Sciences"}, "subfield": {
                "id": "https://openalex.org/subfields/2208", "display_name": "Electrical and Electronic Engineering"},
                                                                                "display_name": "Wireless Energy Harvesting and Information Transfer"},
        {"id": "https://openalex.org/T11128",
         "field": {"id": "https://openalex.org/fields/25", "display_name": "Materials Science"}, "value": 0.0004653,
         "domain": {"id": "https://openalex.org/domains/3", "display_name": "Physical Sciences"},
         "subfield": {"id": "https://openalex.org/subfields/2507", "display_name": "Polymers and Plastics"},
         "display_name": "Advanced Materials for Smart Windows"}, {"id": "https://openalex.org/T10440",
                                                                   "field": {"id": "https://openalex.org/fields/25",
                                                                             "display_name": "Materials Science"},
                                                                   "value": 0.0004457,
                                                                   "domain": {"id": "https://openalex.org/domains/3",
                                                                              "display_name": "Physical Sciences"},
                                                                   "subfield": {
                                                                       "id": "https://openalex.org/subfields/2505",
                                                                       "display_name": "Materials Chemistry"},
                                                                   "display_name": "Thermoelectric Materials"},
        {"id": "https://openalex.org/T12371",
         "field": {"id": "https://openalex.org/fields/22", "display_name": "Engineering"}, "value": 0.0004367,
         "domain": {"id": "https://openalex.org/domains/3", "display_name": "Physical Sciences"},
         "subfield": {"id": "https://openalex.org/subfields/2210", "display_name": "Mechanical Engineering"},
         "display_name": "Dynamics of Pantograph-Catenary Interaction in Railways"}], "works_count": 3866,
     "affiliations": [{"years": [2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015],
                       "institution": {"id": "https://openalex.org/I130701444", "ror": "https://ror.org/01zkghx44",
                                       "type": "education", "lineage": ["https://openalex.org/I130701444"],
                                       "country_code": "US", "display_name": "Georgia Institute of Technology"}},
                      {"years": [2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015],
                       "institution": {"id": "https://openalex.org/I4210133436", "ror": "https://ror.org/030k21z47",
                                       "type": "facility", "lineage": ["https://openalex.org/I4210133436"],
                                       "country_code": "CN",
                                       "display_name": "Beijing Institute of Nanoenergy and Nanosystems"}},
                      {"years": [2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015],
                       "institution": {"id": "https://openalex.org/I19820366", "ror": "https://ror.org/034t30j35",
                                       "type": "government", "lineage": ["https://openalex.org/I19820366"],
                                       "country_code": "CN", "display_name": "Chinese Academy of Sciences"}},
                      {"years": [2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017],
                       "institution": {"id": "https://openalex.org/I4210165038", "ror": "https://ror.org/05qbk4x57",
                                       "type": "education", "lineage": ["https://openalex.org/I19820366",
                                                                        "https://openalex.org/I4210165038"],
                                       "country_code": "CN",
                                       "display_name": "University of Chinese Academy of Sciences"}},
                      {"years": [2024, 2023, 2022],
                       "institution": {"id": "https://openalex.org/I4210099512", "ror": "https://ror.org/0156rhd17",
                                       "type": "healthcare", "lineage": ["https://openalex.org/I4210099512"],
                                       "country_code": "CN",
                                       "display_name": "Second Affiliated Hospital & Yuying Children's Hospital of Wenzhou Medical University"}},
                      {"years": [2024, 2023, 2022, 2021, 2018],
                       "institution": {"id": "https://openalex.org/I27781120", "ror": "https://ror.org/00rd5t069",
                                       "type": "education", "lineage": ["https://openalex.org/I27781120"],
                                       "country_code": "CN", "display_name": "Wenzhou Medical University"}},
                      {"years": [2024, 2023, 2022, 2021, 2020, 2019, 2018],
                       "institution": {"id": "https://openalex.org/I150807315", "ror": "https://ror.org/02c9qn167",
                                       "type": "education", "lineage": ["https://openalex.org/I150807315"],
                                       "country_code": "CN", "display_name": "Guangxi University"}}, {"years": [2024],
                                                                                                      "institution": {
                                                                                                          "id": "https://openalex.org/I96908189",
                                                                                                          "ror": "https://ror.org/059gw8r13",
                                                                                                          "type": "education",
                                                                                                          "lineage": [
                                                                                                              "https://openalex.org/I96908189"],
                                                                                                          "country_code": "CN",
                                                                                                          "display_name": "Xinjiang University"}},
                      {"years": [2024, 2021, 2020, 2019, 2018, 2016, 2012],
                       "institution": {"id": "https://openalex.org/I24185976", "ror": "https://ror.org/011ashp19",
                                       "type": "education", "lineage": ["https://openalex.org/I24185976"],
                                       "country_code": "CN", "display_name": "Sichuan University"}}, {"years": [2024],
                                                                                                      "institution": {
                                                                                                          "id": "https://openalex.org/I4210122949",
                                                                                                          "ror": "https://ror.org/022s5gm85",
                                                                                                          "type": "healthcare",
                                                                                                          "lineage": [
                                                                                                              "https://openalex.org/I4210122949"],
                                                                                                          "country_code": "CN",
                                                                                                          "display_name": "Dongguan People’s Hospital"}}],
     "created_date": "2024-07-11", "display_name": "Zhong Lin Wang", "updated_date": "2024-12-03T05:41:49.673696",
     "summary_stats": {"h_index": 297, "i10_index": 2533, "2yr_mean_citedness": 18.693430656934307},
     "works_api_url": "https://api.openalex.org/works?filter=author.id:A5100376569", "cited_by_count": 405927,
     "counts_by_year": [{"year": 2024, "works_count": 243, "cited_by_count": 121337},
                        {"year": 2023, "works_count": 311, "cited_by_count": 143972},
                        {"year": 2022, "works_count": 284, "cited_by_count": 130982},
                        {"year": 2021, "works_count": 262, "cited_by_count": 113600},
                        {"year": 2020, "works_count": 223, "cited_by_count": 92477},
                        {"year": 2019, "works_count": 225, "cited_by_count": 70746},
                        {"year": 2018, "works_count": 201, "cited_by_count": 61429},
                        {"year": 2017, "works_count": 145, "cited_by_count": 42875},
                        {"year": 2016, "works_count": 180, "cited_by_count": 34738},
                        {"year": 2015, "works_count": 146, "cited_by_count": 28991},
                        {"year": 2014, "works_count": 133, "cited_by_count": 24662},
                        {"year": 2013, "works_count": 116, "cited_by_count": 18960},
                        {"year": 2012, "works_count": 208, "cited_by_count": 15980}], "relevance_score": 44533.93,
     "last_known_institutions": [
         {"id": "https://openalex.org/I4210128491", "ror": "https://ror.org/047qgg117", "type": "facility",
          "lineage": ["https://openalex.org/I19820366", "https://openalex.org/I4210128491"], "country_code": "CN",
          "display_name": "Guangzhou Institute of Energy Conversion"},
         {"id": "https://openalex.org/I4210133436", "ror": "https://ror.org/030k21z47", "type": "facility",
          "lineage": ["https://openalex.org/I4210133436"], "country_code": "CN",
          "display_name": "Beijing Institute of Nanoenergy and Nanosystems"},
         {"id": "https://openalex.org/I19820366", "ror": "https://ror.org/034t30j35", "type": "government",
          "lineage": ["https://openalex.org/I19820366"], "country_code": "CN",
          "display_name": "Chinese Academy of Sciences"}],
     "display_name_alternatives": ["Zhuo‐Lin Wang", "Zilei Wang", "Zhong L. Wang", "Zhong‐Lin Wang", "Z.‐L. Wang",
                                   "Zhulun Wang", "Z‐l. Wang", "Zhong.L. Wang", "Wang Zhong‐lin", "Zhiling Wang",
                                   "ZL. WANG", "Z. Wang", "Wang Zhonglin", "Zhonglin Wang", "Zhuolin Wang",
                                   "Zhong Wang", "Zhanglei Wang", "Wang Lin", "Z. L. Wang", "Zhonglu Wang", "Z. L Wang",
                                   "Zl Wang", "Wang Zhong Lin", "W. LIN", "Z. Lin Wang", "Zhong Lin Wang"]}




# url='https://datacenter.aminer.cn/gateway/open_platform/api/v3/person/base'
# res=requests.get(url,params={"id":"542ec5bbdabfae498ae3ae6b"})
# print(res.status_code)
# print(res.json())
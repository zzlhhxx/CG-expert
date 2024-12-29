import sre_parse

from until.sql_tools import mysql_db_conn
import re
import requests, json

conn = mysql_db_conn(dbname='cg')

cur = conn.cursor()


def contrast_inst_name():
    # sql='select id,authfull,inst_name from elsevier_author_career where is_parse=1 order by id asc limit 1000'
    # sql = 'select id,authfull,inst_name from elsevier_author_career where is_parse=1  and is_ava=0 order by id asc'
    sql = 'select id,name,inst_name from paln_list_people where is_parse=1  and is_ava=0 order by id asc'
    # sql='select id,authfull,inst_name from elsevier_author_career where id=1'

    cur.execute(sql)

    data = cur.fetchall()

    for item in data:
        elsevier_author_career_ids, authfull, inst_name = item
        print(elsevier_author_career_ids, inst_name)
        authfull_ = authfull.split(", ")
        authfull_ = ' '.join(authfull_[::-1])

        select_sql = 'select id, aminer_id,org, source_id, academicType, affiliation, affiliationZh, bio, bioZh, edu, eduZh, homepage, phone, work, workZh, gender, is_ava from aminer where source_id=%s and is_ava=0 '
        cur.execute(select_sql, (elsevier_author_career_ids,))
        aminer_data_list = cur.fetchall()
        for aminer_data in aminer_data_list:
            try:
                ids, aminer_id, org, source_id, academicType, affiliation, affiliationZh, bio, bioZh, edu, eduZh, homepage, phone, work, workZh, gender, is_ava = aminer_data

                if inst_name:
                    inst_name = inst_name.replace(", ", ' ')
                    inst_name = re.sub(r'[(].*?[)]', '', inst_name, re.S)
                    inst_name = inst_name.strip().replace(" ", ' ')
                if affiliation:
                    affiliation = affiliation.replace(" ", ' ')
                if inst_name:
                    affiliation = inst_name.replace(" ", ' ')
                if bio:
                    bio = bio.replace(" ", ' ')
                if org:
                    org = org.replace(" ", ' ')

                if inst_name in affiliation or inst_name in edu or inst_name or authfull_ in bio or authfull_ in org:
                    print('存在')
                    update_sql = 'update aminer set is_ava=1 where aminer_id=%s'
                    cur.execute(update_sql, (aminer_id,))
                    update_sql = 'update elsevier_author_career set is_ava=1 where id=%s'
                    cur.execute(update_sql, (elsevier_author_career_ids,))
                    conn.commit()
                    break
            except Exception as e:
                print(e)
                continue


def contrast_jihua_name():
    # sql='select id,authfull,inst_name from elsevier_author_career where is_parse=1 order by id asc limit 1000'
    # sql = 'select id,authfull,inst_name from elsevier_author_career where is_parse=1  and is_ava=0 order by id asc'
    sql = 'select id,name,inst_name,list_json_path from paln_list_people where is_ids=0  and is_ava=1 order by id asc '
    # sql='select id,authfull,inst_name from elsevier_author_career where id=1'

    cur.execute(sql)

    data = cur.fetchall()

    for item in data:
        ids, name, inst_name, list_json_path = item

        # inst_name=inst_name.replace("股份有限公司",'')
        inst_name = inst_name.replace("有限公司", '')
        inst_name=inst_name[0:4]
        # print(inst_name)
        list_json_path = 'Y:/' + list_json_path
        with open(list_json_path, 'r', encoding='utf8') as f:
            json_data = json.load(f)
        hitsTotal = json_data['data']['hitsTotal']
        if hitsTotal > 0:
            dataList = json_data['data']['hitList']
            for info in dataList:
                if not info:
                    continue
                contact = info.get("contact")
                json_id = info['id']
                if contact:
                    bioZh = contact['bioZh'] if info['contact'].get("bioZh") else ''
                    eduZh = contact['eduZh'] if info['contact'].get("eduZh'") else ''
                    workZh = contact['workZh'] if info['contact'].get("workZh") else ''



                    text = bioZh + " " + eduZh + " " + workZh
                    # print(inst_name,text)
                    # print("**************")
                    if "万人计划" in text:
                        print("*************")
                        print('存在这个',inst_name,text,json_id)
                        # print("存在这个")
                        print("****\n")
                        update_sql = 'update paln_list_people set aminer_id=%s,is_ids=%s   where id=%s'
                        cur.execute(update_sql, (json_id,2,ids))
                        conn.commit()
                        break

#通过"万人计划"进行搜索有91个
#通过”任科技部“进行搜索共有2个，在"万人计划"中不包含这两个



        # for aminer_data in aminer_data_list:
        #     try:
        #         ids, aminer_id, org,source_id, academicType, affiliation, affiliationZh, bio, bioZh, edu, eduZh, homepage, phone, work, workZh, gender, is_ava = aminer_data
        #
        #         if inst_name:
        #             inst_name = inst_name.replace(", ", ' ')
        #             inst_name = re.sub(r'[(].*?[)]', '', inst_name, re.S)
        #             inst_name = inst_name.strip().replace(" ", ' ')
        #         if affiliation:
        #             affiliation=affiliation.replace(" ", ' ')
        #         if inst_name:
        #             affiliation=inst_name.replace(" ", ' ')
        #         if bio:
        #             bio=bio.replace(" ", ' ')
        #         if org:
        #             org=org.replace(" ", ' ')
        #
        #         if inst_name in affiliation or inst_name in edu or inst_name or authfull_ in bio or authfull_ in org:
        #             print('存在')
        #             update_sql = 'update aminer set is_ava=1 where aminer_id=%s'
        #             cur.execute(update_sql, (aminer_id,))
        #             update_sql = 'update elsevier_author_career set is_ava=1 where id=%s'
        #             cur.execute(update_sql, (elsevier_author_career_ids,))
        #             conn.commit()
        #             break
        #     except Exception as e :
        #         print(e)
        #         continue


contrast_jihua_name()
# contrast_inst_name()

# def retry_requests():
#     # sql = 'select id,authfull,inst_name from elsevier_author_career where is_ava=0 and id <1001  order  by id asc  limit 1'
#     sql = 'select id,authfull,inst_name from elsevier_author_career where id=960'
#     cur.execute(sql)
#     data = cur.fetchall()
#     url = 'https://searchtest.aminer.cn/aminer-search/search/person'
#     for item in data:
#         in_id, authfull, inst_name = item
#
#         data = {"query": "", "needDetails": True, "page": 0, "size": 20, "aggregations": [{"field": "h_index",
#                                                                                            "rangeList": [
#                                                                                                {"from": 0, "to": 10},
#                                                                                                {"from": 10, "to": 20},
#                                                                                                {"from": 20, "to": 30},
#                                                                                                {"from": 30, "to": 40},
#                                                                                                {"from": 40, "to": 50},
#                                                                                                {"from": 50, "to": 60},
#                                                                                                {"from": 60,
#                                                                                                 "to": 99999}],
#                                                                                            "size": 0, "type": "range"},
#                                                                                           {"field": "lang", "size": 10,
#                                                                                            "type": "terms"},
#                                                                                           {"field": "nation",
#                                                                                            "size": 10,
#                                                                                            "type": "terms"},
#                                                                                           {"field": "gender",
#                                                                                            "size": 10,
#                                                                                            "type": "terms"},
#                                                                                           {"field": "contact.position",
#                                                                                            "size": 20, "type": "terms"},
#                                                                                           {"field": "org_id",
#                                                                                            "size": 200,
#                                                                                            "type": "terms"}],
#                 "filters": [],
#                 "searchKeyWordList": [
#                     {"advanced": True, "keyword": f"{authfull}", "operate": "0", "wordType": 4,
#                      "segmentationWord": "true",
#                      "needTranslate": True},
#                     {"advanced": True, "keyword": f"{inst_name}", "operate": "0", "wordType": 5,
#                      "segmentationWord": "true", "needTranslate": True}],  # 作者单位，先不采集
#                 "usingSemanticRetrieval": True
#                 }
#
#         headers = {
#             "content-type": "application/json;charset=UTF-8"
#         }
#         res = requests.post(url=url, data=json.dumps(data), timeout=20, headers=headers)
#
#         if res.status_code == 200:
#             data = res.json()
#             if data['code'] == 200:
#                 hitsTotal = data['data']['hitsTotal']
#                 # print(data['data'])
#                 print(hitsTotal)
#                 hitList = data['data']['hitList']
#                 print(hitList)
# retry_requests()

# Duke University Medical Center

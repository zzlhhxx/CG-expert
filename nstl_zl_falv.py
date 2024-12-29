from until.sql_tools import mysql_db_conn, getStrAsMD5
import random
import requests
import json

conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
sql = 'select id,list_json,aminer_zl_id,num from nstl_zl where  is_list_dow=1 and law_status is null  order by id asc '
cur.execute(sql)
data = cur.fetchall()

for item in data:
    ids, list_json, aminer_zl_id, num = item
    data_dict = json.loads(list_json)
    print(ids)


    data_=data_dict['data']
    for sub_list in data_[0]:
        if sub_list['f']=="iast":
            law_status=sub_list['v']
            # print(law_status)
            print(num)
            law_status_str='|'.join(law_status)
            print(law_status_str)
            update_sql = f"update nstl_zl  set law_status=%s where aminer_zl_id=%s"
            cur.execute(update_sql, (law_status_str, aminer_zl_id))
            conn.commit()

    #
    #     for item in sub_list:
    #         new_data_list.append({item["f"]: item["v"]})
    #
    # law_status=new_data_list[10]['iast'][0]
    # print(law_status)

    # update_sql = f"update aminer  set profilePubsTotal=%s where id=%s"
    # cur.execute(update_sql, (0, in_id))
    # conn.commit()
a={"code": "0", "took": 83, "total": 1, "data": [
    [{"f": "id", "v": "06e405775434d07b9aadf9603fb23937"}, {"f": "type", "v": "Patent"}, {"f": "score", "v": 10000.0},
     {"f": "yea", "v": ["2022"]}, {"f": "lan", "v": [{"en": "英语"}]}, {"f": "sysfiin",
                                                                        "v": ["hasPatentee", "hasAuthor", "hasInventor",
                                                                              "hasHolding", "year", "sysId",
                                                                              "internationalCode", "priorityNumber",
                                                                              "varietyType", "language", "openYear",
                                                                              "title", "analysisLanguage",
                                                                              "internationalSourceCode", "accessType",
                                                                              "standardYear", "sysDataCreateTime",
                                                                              "countryCode", "sysDataUpdateTime",
                                                                              "sysDataSources", "applyDateStr",
                                                                              "sysSubType", "searchClassificationCode",
                                                                              "languageIdentify", "sysDataStatus",
                                                                              "applyNumber", "sysDataType",
                                                                              "sysSourceId", "entityType",
                                                                              "openCountryCode", "updateTime",
                                                                              "abstract", "titleEng", "idSet",
                                                                              "openDateStr", "classificationCode",
                                                                              "sysDataVersion", "sourceType",
                                                                              "createTime", "prioritySourceNumber",
                                                                              "letter", "sysAccessTypeOrder",
                                                                              "internationalMainCode", "openNumber",
                                                                              "sysParentType", "openDate", "applyDate",
                                                                              "sysDocTypeCode", "sysOrderId",
                                                                              "sysDataStorageTime", "sysDocTypeFlag"]},
     {"f": "syid", "v": ["06e405775434d07b9aadf9603fb23937"]}, {"f": "acty", "v": ["nstl"]},
     {"f": "coco", "v": [{"US": "美国"}]}, {"f": "sysuty", "v": ["P02"]},
     {"f": "tit", "v": ["HOLE TRANSPORT MATERIAL, SYNTHESIS THEREOF, AND SOLAR CELL"]}, {"f": "abs", "v": [
        "The organic small molecule 4,4′,4″,4′″-(5,5",
        "-dimethoxycyclopenta-1,3-diene-1,2,3,4-tetrayl)tetrakis(N,N-bis(4",
        "-methoxyhenyl)aniline (CPDA 1), shows electrochemical",
        " properties very close to spiro-OMeTAD indicating a high",
        " compatibility with PSC systems for its use as a hole transport"]}, {"f": "hasAut", "v": [
        [{"f": "id", "v": "f4c0781bfd53d9c7235de35aa703e940"}, {"f": "type", "v": "People"},
         {"f": "nam", "v": ["Liu, Yuhang"]}],
        [{"f": "id", "v": "cdb605a67f57d50a2d888874e9fc780a"}, {"f": "type", "v": "People"},
         {"f": "nam", "v": ["Zakeeruddin, Shaik Mohammed"]}],
        [{"f": "id", "v": "9229cbb3300d5112345df13f4c11e4b6"}, {"f": "type", "v": "People"},
         {"f": "nam", "v": ["Graetzel, Michael"]}],
        [{"f": "id", "v": "be13062d800dcd9f774544d5c207d7fb"}, {"f": "type", "v": "People"},
         {"f": "nam", "v": ["Bauer, Michael"]}],
        [{"f": "id", "v": "e194feabd7df9f51e9006b396bac1e2c"}, {"f": "type", "v": "People"},
         {"f": "nam", "v": ["Bäuerle, Peter"]}]]}, {"f": "hasInv", "v": [
        [{"f": "id", "v": "f4c0781bfd53d9c7235de35aa703e940"}, {"f": "type", "v": "People"},
         {"f": "nam", "v": ["Liu, Yuhang"]}],
        [{"f": "id", "v": "cdb605a67f57d50a2d888874e9fc780a"}, {"f": "type", "v": "People"},
         {"f": "nam", "v": ["Zakeeruddin, Shaik Mohammed"]}],
        [{"f": "id", "v": "9229cbb3300d5112345df13f4c11e4b6"}, {"f": "type", "v": "People"},
         {"f": "nam", "v": ["Graetzel, Michael"]}],
        [{"f": "id", "v": "be13062d800dcd9f774544d5c207d7fb"}, {"f": "type", "v": "People"},
         {"f": "nam", "v": ["Bauer, Michael"]}],
        [{"f": "id", "v": "e194feabd7df9f51e9006b396bac1e2c"}, {"f": "type", "v": "People"},
         {"f": "nam", "v": ["Bäuerle, Peter"]}]]}, {"f": "hasHol", "v": [
        [{"f": "id", "v": "95863b5736f11c5db8272243326775ea"}, {"f": "type", "v": "Holding"},
         {"f": "lico", "v": [{"CN111001": "中国科学技术信息研究所"}]}]]},
     {"f": "availableOrderType", "v": "全文申请单"}]],
 "traceId": "3597277ca2ff489a8240032bc32594f5.83.17333961320116781"}

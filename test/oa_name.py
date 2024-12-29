import requests

from until.sql_tools import mongo_client,mysql_db_conn
from until.time_tool import saveTime
import re
import pycountry
import json
from urllib.parse import unquote
from lxml import etree


conn=mysql_db_conn(dbname='cg')
cur=conn.cursor()

select_ = 'select id,oa_name from oa_to_aminer where is_download=1 order by id asc limit 1'
# select_ = 'select id,name,inst_name,year,source,list_json,html_path,xm_ids,oa_path,oa_id,aminer_id,zl_ids from paln_list_people where id=20000033 '
cur.execute(select_)
data = cur.fetchall()
print(len(data))
for item in data:
    ids,oa_name = item
    print(ids,oa_name)

    url = 'https://searchtest.aminer.cn/aminer-search/search/person'

    query = {"query": "", "needDetails": True, "page": 0, "size": 20, "aggregations": [{"field": "h_index",
                                                                                        "rangeList": [
                                                                                            {"from": 0, "to": 10},
                                                                                            {"from": 10,
                                                                                             "to": 20},
                                                                                            {"from": 20,
                                                                                             "to": 30},
                                                                                            {"from": 30,
                                                                                             "to": 40},
                                                                                            {"from": 40,
                                                                                             "to": 50},
                                                                                            {"from": 50,
                                                                                             "to": 60},
                                                                                            {"from": 60,
                                                                                             "to": 99999}],
                                                                                        "size": 0, "type": "range"},
                                                                                       {"field": "lang", "size": 10,
                                                                                        "type": "terms"},
                                                                                       {"field": "nation", "size": 10,
                                                                                        "type": "terms"},
                                                                                       {"field": "gender", "size": 10,
                                                                                        "type": "terms"},
                                                                                       {"field": "contact.position",
                                                                                        "size": 20, "type": "terms"},
                                                                                       {"field": "org_id", "size": 200,
                                                                                        "type": "terms"}],
             "filters": [],
             "searchKeyWordList": [
                 {"advanced": True, "keyword": f"{oa_name}", "operate": "0", "wordType": 4, "segmentationWord": "True",
                  "needTranslate": True},
                 {"advanced": True, "keyword": f"", "operate": "0", "wordType": 5,
                  "segmentationWord": "True",
                  "needTranslate": True}], "usingSemanticRetrieval": True}

    headers = {
        "content-type": "application/json;charset=UTF-8"
    }
    res = requests.post(url=url, data=json.dumps(query), headers=headers)

    if res.status_code == 200:
        print("有")
    else:
        print(ids,oa_name)

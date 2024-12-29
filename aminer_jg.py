
import time

from until.sql_tools import mysql_db_conn, getStrAsMD5
from until.config import he

from lxml import etree
from urllib.parse import unquote
import random
import requests
import json
import os

url="https://datacenter.aminer.cn/gateway/open_platform/api/v3/organization/Open/OrgOpenData"


conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
sql = 'select id,source_id,aminer_id,org from aminer where is_ava=1  and char_length(org)>1  order by  id asc limit 1000'
cur.execute(sql)
data = cur.fetchall()


for item in data:
    in_id, source_id, aminer_id ,org= item
    # print(org)
    # print(source_id)
    # print("*****")


    headers={
        "Content-Type":"application/json;charset=utf-8",
        "Authorization":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzMyODQ0MTUsInRpbWVzdGFtcCI6MTczMzE5ODAxNiwidXNlcl9pZCI6IjY3NDUzNWVkNWZjNWJlOTNiMTlmY2Q3OCJ9.oHDwNwvFAVQLzkdW_ySEpkNfQ98wbvGGUGgQAcnbVK4"
    }

    a={"org":f"{org}"}
    # print(a)
    response=requests.post(url,headers=headers,data=json.dumps(a))
    if response.status_code==200:
        # print(response.text)
        response_json=json.loads(response.text)
        # print(type(response_json))
        resp=response_json["data"]  #data":[{"org_id":"","org_name":"NEW ENGLAND CTR, TUFTS UNIV"}]

        for org_id in resp:
            print(org_id)
            orgid=org_id["org_id"]if org_id.get("org_id") else ""
            orgname = org_id["org_name"] if org_id.get("org_name") else ""
            print(aminer_id)
            print("*****")
            print(orgname)

            sql_str="insert into aminer_org_id (id,aminer_id,source_id,org,org_id,org_name) value (%s,%s,%s,%s,%s,%s)"
            # sql_str = "update aminer_org_id set  id=%s,aminer_id=%s, source_id=%s, org=%s, org_id=%s, org_name=%s "
            cur.execute(sql_str, (in_id, aminer_id,source_id,org,orgid,orgname))
            conn.commit()
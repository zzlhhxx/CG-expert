import requests

import re
import time

from until.sql_tools import mysql_db_conn, getStrAsMD5, freeRepeat, mongo_client
from until.config import he

from lxml import etree
from urllib.parse import unquote
import random

import json
import os

conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()


select_sql='select id,name_en,lw_path from amine_xm where is_lw=1 and id_   order by id asc '
cur.execute(select_sql)
data=cur.fetchall()
for item in data:
    ids, name_en, lw_path=item


# lw_id="5390877f20f70186a0d2fb46"
#
# url=f"https://datacenter.aminer.cn/gateway/open_platform/api/v3/paper/platform/details/not/contain/wos/by/id?id={lw_id}"
# headers={
#     'Authorization': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzUxODQwMzIsInRpbWVzdGFtcCI6MTczNTAxMTIzMiwidXNlcl9pZCI6IjY3NDUzNWVkNWZjNWJlOTNiMTlmY2Q3OCJ9.GjdWLR4xp_mw355g1uqLbGtMAZe0OfMGT4g5aY7p_TE"
# }
#
# res=requests.get(url=url,headers=headers)
# print(res.text)
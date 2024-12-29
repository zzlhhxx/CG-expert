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

conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
sql = 'select id,detail_json,title from openalex_author_detail where  is_ava=1  order by id asc limit 1'
cur.execute(sql)
datas = cur.fetchall()
for data in datas:
    id, detail_json, title = data
    detail_json_1 = json.loads(detail_json)
    last_known_institutions = detail_json_1['last_known_institutions'][0]
    display_name = last_known_institutions['display_name']
    print(display_name)



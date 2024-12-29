import re
import time

from until.sql_tools import mysql_db_conn, getStrAsMD5, freeRepeat, mongo_client
from until.config import he

from lxml import etree
from urllib.parse import unquote
import random
import requests
import json
import os

conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()

select_sql='select id,oa_name,aminer_detail_json from oa_to_aminer where is_download=1  order by id asc limit 1 '
cur.execute(select_sql)
data=cur.fetchall()
for item in data:
    in_id, oa_name, aminer_detail_json=item
    path=r'Z:/'+aminer_detail_json
    with open(path, 'r', encoding='utf8') as f:
        json_data = json.load(f)
        authors	=json_data['authors']
        for author in authors:

            author_name=author['name']
            print(author_name)



from pymongo import MongoClient
import json
from until.sql_tools import mysql_db_conn, getStrAsMD5


conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
# sql = 'select id,source_id,aminer_id,org from aminer where is_ava=1  and char_length(org)>1  order by  id asc limit 1000'
# cur.execute(sql)
# data = cur.fetchall()






# 连接到MongoDB
client = MongoClient("192.168.5.21", 27017)

# 选择数据库
db = client['cg']

# 选择集合（类似于SQL中的表）
collection = db['zjwl_xm']

# 读取数据
documents = collection.find().limit(1)
for document in documents:
    authors=document['authors']
    for author in authors:
        _person_id=author['_person_id']
        print()

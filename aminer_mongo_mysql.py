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
collection = db['author_table']

# 读取数据
documents = collection.find({},{"id","au_name","au_name_zh"})
for document in documents:
    print(document)     #{'_id': 1, 'au_name': 'Michael Graetzel', 'au_name_zh': '米夏埃尔·格雷策尔'}
    a_id=document["_id"]
    a_name=document["au_name"] if document.get("au_name") else " "
    a_name_zh=document["au_name_zh"]if document.get("au_name_zh") else " "
    # print(a_id)
    # print(type(document))  #<class 'dict'>
    # print(a_id)
    # print(a_name)
    # print(a_name_zh)
    sql_str = "insert into author_table (id,au_name,au_name_zh) value (%s,%s,%s)"
    # sql_str = "update aminer_org_id set  id=%s,aminer_id=%s, source_id=%s, org=%s, org_id=%s, org_name=%s "
    cur.execute(sql_str, (a_id, a_name, a_name_zh))
    conn.commit()

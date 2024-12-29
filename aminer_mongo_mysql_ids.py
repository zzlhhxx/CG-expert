from pymongo import MongoClient
import json
from until.sql_tools import mysql_db_conn, getStrAsMD5
from pymongo import MongoClient


# 连接到MongoDB
client = MongoClient("192.168.5.21", 27017)
# 选择数据库
db = client['cg']
# 选择集合（类似于SQL中的表）
collection = db['pub_table']
# 读取数据
documents = collection.find()

for item in documents:
    _id=item['_id']
    print(_id)
    pub_id=item['pub_id']
    # collection.update_one({"_id": _id}, {"$set": {
    #         "_id": pub_id,
    #     }})
    collection.update_one(
        {'_id': _id},
        {'$set': {'_id': pub_id}, '$unset': {'_id': 1}}
    )



def update_id():
    conn = mysql_db_conn(dbname='cg')
    cur = conn.cursor()
    sql = 'select id,source_id,aminer_id,zl_ids,lw_ids,xm_ids from aminer where is_ava=1    order by  id asc limit 3000'
    cur.execute(sql)
    data = cur.fetchall()
    # print(data)

    #
    # for item in data:
    #     ids,source_id,aminer_id,zl_ids,lw_ids,xm_ids = item #mysql字段
    #     if zl_ids:
    #         zl_ids_list=zl_ids.split(",,"),
    #     else:
    #         zl_ids_list=[]
    #     if lw_ids:
    #         lw_ids_list=lw_ids.split(",,"),
    #     else:
    #         lw_ids_list=[]
    #     if xm_ids:
    #         xm_ids_list=xm_ids.split(",,"),
    #     else:
    #         xm_ids_list=[]
    #
    #     collection.update_one({"_id": source_id},{"$set": {
    #         "zl_ids": zl_ids_list,
    #         "lw_ids": lw_ids_list,
    #         "xm_ids": xm_ids_list
    #
    #     }})

    # print(ids)
    # print(zl_ids)
    # print(type(zl_ids))
    # print(lw_ids)
    # print(type(lw_ids))
    # print(xm_ids)
    # print(type(xm_ids))




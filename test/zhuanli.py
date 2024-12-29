from pymongo import MongoClient
import json

# 连接到MongoDB
client = MongoClient("192.168.5.21", 27017)

# 选择数据库
db = client['cg']

# 选择集合（类似于SQL中的表）
collection = db['author_table']

# 读取数据
documents = collection.find({},{"zl_ids":1})
for document in documents:
    print("*****************")
    print(document)
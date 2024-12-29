from pymongo import MongoClient
import json

# 连接到MongoDB
client = MongoClient("192.168.5.21", 27017)

# 选择数据库
db = client['cg']

# 选择集合（类似于SQL中的表）
collection = db['zl_table']

# 读取数据
documents = collection.find({}, {"country": 1, "kind": 1, "pub_num": 1})




for item in documents:

    id=item['_id']
    country=item['country']
    kind=item['kind']
    pub_num=item['pub_num']
    country_=''
    for cc in country:
        country_+=cc.capitalize()   # 首字母大写

    num=country_+pub_num+kind
    # print(item)
    # print(type(item))
    # i+=1
    # print(i)
    # print(country_)
    print(num)
    collection.update_one(

        {"_id":id},
        {'$set': {
            'num': num
        }
            }
    )
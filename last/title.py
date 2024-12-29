from until.sql_tools import mongo_client


db=mongo_client("cg")

c=db['zjwl_zl']

data=c.find()

for item in data:
    au_phone=item['title']
    in_id=item['_id']
    if "  " in au_phone:
        print("*********")
        print(au_phone)
        print("*********")
        # au_phone_tihuan=au_phone.replace("  ","").replace(", ",",")
        # print("*********")
        # print(au_phone_tihuan)
        # print("*********")
        # c.update_one(
        #     {'_id': in_id},
        #     {'$set': {'title': au_phone_tihuan}}
        # )
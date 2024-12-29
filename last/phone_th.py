from until.sql_tools import mongo_client


db=mongo_client("cg")

c=db['zjwl_author']

data=c.find().limit(1000)

for item in data:
    au_phone=item['au_phone']
    in_id=item['_id']
    print(au_phone)
    # if len(au_phone):
        # for phone in au_phone:
        #     print(phone)
            # phone_zero=phone.replace("(0)","").replace("(","").replace(")","").replace(" ","-").replace(".","-").replace("--","-").replace("---","-").replace("--","-")
            # print(phone_zero)
            # print("**********")

            # c.update_one(
            #     {'_id': in_id},
            #     {'$set': {'au_phone': phone_zero}}
            # )

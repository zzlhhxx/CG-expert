from until.sql_tools import mongo_client


db=mongo_client("cg")

c=db['zjwl_author']

data=c.find().limit(1000)

for item in data:
    au_phone=item['au_phone']
    if len(au_phone):
        for phone in au_phone:
            print(phone)
            print("**********")
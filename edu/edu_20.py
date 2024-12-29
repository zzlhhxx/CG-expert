from until.sql_tools import mongo_client


db=mongo_client("cg")

c=db['zjwl_author']

data=c.find().limit(20)

for item in data:

    au_edu_1=item['au_edu']
    au_name=item['au_name']
    if len(au_name):

        for i in au_edu_1:
            text=i['text']
            sql='select '
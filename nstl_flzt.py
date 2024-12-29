import json

import requests
from until.sql_tools import mysql_db_conn,freeRepeat,mongo_client

# db=mongo_client('cg')
# c=db['zl_table']
# data=c.find()

conn = mysql_db_conn(dbname='cg')
cur=conn.cursor()

select_sql='select id,aminer_zl_id,nstl_id,num from nstl_zl where is_list_dow=0  order by id asc limit  3 '

cur.execute(select_sql)

data=cur.fetchall()
print(len(data))
for item in data:
    ids, aminer_zl_id, nstl_id,num=item
    url = "https://www.nstl.gov.cn/api/service/nstl/web/execute?target=nstl4.search4&function=paper/pc/list/pl"

    query={"c": 10,"st": "0","f": [],"p": "","q": [{
                    "k": "",
                    "v": num,
                    "e": 1,
                    "o": "AND",
                    "a": 0
                },
                {
                    "k": "laid",
                    "a": 1,
                    "o": "",
                    "f": 1,
                    "vs": ["日文", "韩文", "外文"]
                }
            ],
            "op": "AND",
            "s": ["nstl", "haveAbsAuK:desc", "yea:desc", "score"],
            "t": ["Patent"]
        }
    print(query)
    data = {
        "query":json.dumps(query),
        "webDisplayId": 11,
        "sl": 1,
        "searchWordId": "80b744dc4ce4a79f8443585156878dcc",
        "searchId": "2d29f0a67f68bb02ebcc17c49c93be6d",
        "facetRelation": [],
        "pageSize": 10,
        "pageNumber": 1
    }
    response = requests.post(url,data=data)
    resp = response.json()
    if resp.status_code== 200:
        print("******")
    # break
    # data=resp["data"][0][0]
# for item in data:
#     _id=item['_id']
#     num=item['num']
#     insert_sql='insert into nstl_zl(aminer_zl_id,num) value(%s,%s)'
#     cur.execute(insert_sql,(str(_id),num))
#     conn.commit()


# sql = 'select id,zl_id from aminer_zl where is_donwload_path=1  order by id asc limit 1'
# sql = 'select id,hitsTotal,authfull,inst_name,aminer_path from elsevier_author_career where id =2 '
# cur.execute(sql)
# das = cur.fetchall() #mysql查詢數據
# for d in das:
#     in_id, zl_id=d
#
#     # nstl_id=data["v"] if data.get("v") else ""
#     # if nstl_id=="":
#     #     print("空值")
#
#
#     # sql_insert="INSERT INTO nstl_zl (id,aminer_zl_id,nstl_id,list_json,is_list_dow)VALUES (%s,%s,%s,%s,%s)"
#     # cur.execute(sql_insert,(in_id,zl_id,nstl_id,))
#     # conn.commit()





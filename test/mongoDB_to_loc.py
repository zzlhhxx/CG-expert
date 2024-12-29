from pymongo import MongoClient
import json
from until.sql_loc import mysql_db_conn, getStrAsMD5,freeRepeat

# conn_21=mysql_db_conn(conn_name='21',dbname='cg')
# cur_21=conn_21.cursor()
conn_5=mysql_db_conn(conn_name='localhost',dbname='mysql_loc')
cur_5=conn_5.cursor()

client = MongoClient("192.168.5.21", 27017)
db = client['cg']
collection = db['zjwl_zl']

# 读取数据
documents = collection.find()
for document in documents:

    inventors=document['inventors']
    # patentees=document['patentees']
    # print(inventors,patentees)
    in_id=document["_id"]
    print(in_id)
    for inventor in inventors:
        if inventor.get("person_id"):
            name = inventor['name']

            person_id=inventor['person_id']

            repeat_result = freeRepeat('zl_orgs', "aminer_id", person_id, conn_5)
            # print(aminer_id)
            if repeat_result:
                insert_sql = 'insert into zl_orgs (name,aminer_id) value(%s,%s)'
                cur_5.execute(insert_sql, (name, person_id))
                conn_5.commit()
    patentees=document['patentees']
    if len(patentees):
        for patentee in patentees:
            if patentee.get("person_id"):
                person_id = patentee['person_id']
                name = patentee['name']
                repeat_result = freeRepeat('zl_orgs', "aminer_id", person_id, conn_5)
                # print(aminer_id)
                if repeat_result:
                    insert_sql = 'insert into zl_orgs (name,aminer_id) value(%s,%s)'
                    cur_5.execute(insert_sql, (name, person_id))
                    conn_5.commit()
    assignees=document['assignee']
    if len(assignees):
        for assignee in assignees:

            if assignee.get("person_id"):
                name = assignee['name']
                person_id = assignee['person_id']
                repeat_result = freeRepeat('zl_orgs', "aminer_id", person_id, conn_5)
                # print(aminer_id)
                if repeat_result:
                    insert_sql = 'insert into zl_orgs (name,aminer_id) value(%s,%s)'
                    cur_5.execute(insert_sql, (name, person_id))
                    conn_5.commit()







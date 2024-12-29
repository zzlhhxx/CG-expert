import time

from until.sql_tools import mysql_db_conn, getStrAsMD5

import json




conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
sql = 'select id,name,list_json_path from paln_list_people where is_ava=1 and is_ids=1   order  by id asc '
cur.execute(sql)
data = cur.fetchall()

for item in data:
    ids, name, list_json_path = item
    with open(f"Z:/{list_json_path}", 'r', encoding='utf8') as f:
        data = json.load(f)


        data_json=data["data"]

        hitList=data_json["hitList"] if data_json.get("hitList") else ''
        if hitList:
            hitList_t=hitList[0] if hitList else ''
            if hitList_t:
                contact=hitList_t["contact"]if hitList_t.get("contact") else ''
                if contact:
                    affiliation = contact["affiliation"] if contact.get("affiliation") else ''
                    print(affiliation)
                    update_ = 'update paln_list_people set inst_name_en=%s where id =%s'
                    cur.execute(update_, ( affiliation,ids))
                    conn.commit()
                    print(ids,name)








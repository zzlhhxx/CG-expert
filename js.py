from until.sql_tools import mysql_db_conn


conn=mysql_db_conn(dbname='cg')

cur=conn.cursor()


sql='select id,authfull,inst_name from elsevier_author_career where is_parse=1 order by id asc limit 1'

cur.execute(sql)

data=cur.fetchall()

for item in data:
    ids,authfull,inst_name=item
    select_sql='select * from aminer where source_id=%s'
    cur.execute(select_sql,(ids,))
    aminer_data_list=cur.fetchall()
    for aminer_data in aminer_data_list:
        ids,aminer_id, source_id, academicType, affiliation, affiliationZh, bio, bioZh, edu, eduZh, homepage, phone, work,workZh, gender,is_ava=aminer_data
        print(aminer_data)
        break
        # if authfull in
    break
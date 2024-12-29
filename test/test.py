import MySQLdb
import json


def mysql_db_conn(dbname=None):
    global conn
    conn = MySQLdb.connect(
        host='120.53.84.233',
        port=3306,
        user='cg',
        db=dbname,
        charset='utf8mb4',
        password="DRDWji3pabfxF6Bx"
    )
    return conn


# conn=mysql_db_conn('cg')
# cur=conn.cursor()
# sql="select * from elsevier_author_career where id=2"
# cur.execute(sql)
# data=cur.fetchall()
# print(data)
#
# for i in data:
#     print(i)

# with open('Z:/html/aminer/0/0/1.json', 'r', encoding='utf8') as f:
#      json_data=json.load(f)
#
# hitList=json_data['data']['hitList']
# contact=hitList[0]['contact']
# academicType=contact['academicType']
# phone=contact['phone']
# position=contact['position']
# data = {
#     "academicType": academicType,
#     "phone": phone,
#     "position": position
# }
# for item in data:
#     print(data[item])
# conn=mysql_db_conn('cg')
# cur=conn.cursor()
#
# sql='select * from get_baike_url where id =%s'
#
# cur.execute(sql,(2,))
#
# data=cur.fetchall()

# for item in data :
#     ids,author,inst_name,cntry,a,b,c,d,e=item
#     print(ids,author,inst_name,cntry)

# a = {
#     "abstract": "Chemical doping is an important strategy to alter the charge-transport properties of both molecular and polymeric organic semiconductors that find widespread application in organic electronic devices. We report on the use of a new class of Co(III) complexes as p-type dopants for triarylamine-based hole conductors such as spiro-MeOTAD and their application in solid-state dye-sensitized solar cells (ssDSCs). We show that the proposed compounds fulfill the requirements for this application and that the discussed strategy is promising for tuning the conductivity of spiro-MeOTAD in ssDSCs, without having to rely on the commonly employed photo-doping. By using a recently developed high molar extinction coefficient organic D-pi-A sensitizer and p-doped spiro-MeOTAD as hole conductor, we achieved a record power conversion efficiency of 7.2%, measured under standard solar conditions (AM1.5G, 100 mW cm(-2)). We expect these promising new dopants to find widespread applications in organic electronics in general and photovoltaics in particular.",
#     "abstract_zh": "a",
#     'nihao': ""}
# # for k,v in a.items():
# #     print(k,v)
#
# c=a['eeeeeeeee']
# d=a.get('eeeee')
# print(d)
# print("****************")
# print(c)

try:
 print(5/0)
except ZeroDivisionError:
 print("You can't divide by zero!")
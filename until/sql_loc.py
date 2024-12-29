import MySQLdb
from urllib.parse import unquote
import hashlib
import pymongo

def getStrAsMD5(parmStr=None):
    if parmStr:
        if isinstance(parmStr, str):
            parmStr = parmStr.replace('https://', "").replace('http://', "")
            parmStr = unquote(parmStr, 'utf-8').replace("&amp;", "&")
            parmStr = parmStr.encode("utf-8")
        m = hashlib.md5()
        m.update(parmStr)
        return m.hexdigest()
    else:
        return ''

def mongo_client(table:str):
    client = pymongo.MongoClient("192.168.5.21", 27017)
    db = client[table]
    return db

def freeRepeat(table_name, repeat_field, repeat_field_value, conn):
    cursor = conn.cursor()
    sql = "select id from " + table_name + " where " + repeat_field + " = %s"
    cursor.execute(sql, (repeat_field_value,))
    results = cursor.fetchall()

    if len(results) < 1:
        cursor.close()
        return True
    else:
        cursor.close()
        # print(str(repeat_field_value)+"已存在")
        return False


def mysql_db_conn(conn_name='localhost',dbname=None):
    global conn
    if conn_name =='localhost':
        print('aaaaa')
        conn = MySQLdb.connect(
            host='192.168.5.5',
            port=3306,
            user='root',
            db=dbname,
            charset='utf8mb4',
            password="1234"
        )
        return conn
    if conn_name =='21':
        conn = MySQLdb.connect(
            host='192.168.5.21',
            port=3306,
            user='root',
            db=dbname,
            charset='utf8mb4',
            password="1234"
        )
        return conn
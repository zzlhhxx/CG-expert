import time
from fake_useragent import UserAgent

import  MySQLdb
import urllib.parse
import requests
from lxml import etree
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

conn=mysql_db_conn('cg')
cur=conn.cursor()
authfull_cur=conn.cursor()
sql='select id,authfull from get_baike_url limit 10'
cur.execute(sql)

ids=cur.fetchall()

for id_tuple in ids:
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
        "authority":'cn.bing.com'
    }
    id_value,authfull = id_tuple
    # authfull_cur.execute("SELECT authfull FROM get_baike_url WHERE id = %s", (id_value,))
    # record = authfull_cur.fetchone()
    # value=record[0]
    url_template = "https://www.bing.com/search?q="
    encoded_value = urllib.parse.quote(authfull)
    url_bing = url_template + encoded_value

    res=requests.get(url_bing,headers=headers,timeout=20)
    print(res.status_code)
    if res.status_code !=200:
        print('反爬',res.text)
    tree = etree.HTML(res.text)
    links = tree.xpath('//h2/a/@href')
    if not len(links):
        print(res.text)
    baike_url=''
    for link in links :
        if 'baike.baidu.com' in link:
            baike_url=link

    print(baike_url)
    print(url_bing)
    time.sleep(5)
cur.close()
conn.close()
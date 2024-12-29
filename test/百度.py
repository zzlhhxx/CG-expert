from until.sql_tools import mongo_client, mysql_db_conn
import re
import json
from until.time_tool import timestamp_to_date_str
import datetime
import requests
conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
from lxml import etree




sql = 'select id,baike_url from baike_author_info where is_download_html=1   order by id asc limit 1 '
cur.execute(sql)
data = cur.fetchall()
print(len(data))
for item in data:
    ids, baike_url= item
    print(baike_url)

    response=requests.get(url=baike_url)
    tree = etree.HTML(response.text)
    links = tree.xpath('/html/body/div[1]/div/div[2]/div[2]/div/div[1]/div/div[4]/dl[1]/div[4]/dd/span/text()')
    print(links)
    # for link in links:
    #     print(link.
    #     ())




#查看专利没有入库的  267910
#查看项目没有下载的
#查看论文没有入库了


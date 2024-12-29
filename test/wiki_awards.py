import json
import re
from datetime import datetime
from lxml import etree
from yuduo.work.sql_tools import mysql_db_conn,mongo_client
from yuduo.work.time_tools import time_format
from yuduo.work.replace_until import replace_xpath,replace_html_tags
# path_html = r'Z:/cg_expert_data/html/aminer_xm/'

db=mongo_client("cg")

c=db['xm_table']

def re_replace(data):
    retrun_data = re.sub(pattern='<(.|\n)+?>', repl='', string=data)
    return retrun_data

def judge_list(data):
    retrun_data = re.sub(pattern='<(.|\n)+?>', repl='', string=data)

    return retrun_data




conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
sql = 'select id,awards from wiki_author_info where is_download_html=1 order by  id asc'
# sql = 'select id,source_id,aminer_id,profilePubsTotal,lw_path from aminer where id=797  order by  id asc '
cur.execute(sql)
wk_data = cur.fetchall()
for i in wk_data:
    ids,awards = i
    if awards:
        # print(id,awards)
        awards_jiexi1 = awards.split("</td>")
        awards_jiexi1 = [i for i in awards_jiexi1 if judge_list(i) != ''][0]
        if '<br>' not in awards_jiexi1 and '</li>' not in awards_jiexi1:
            awards_jiexi1 = awards_jiexi1.replace("</p>", '\n')
        else:
            awards_jiexi1 =awards_jiexi1.replace("<br>",'\n').replace("</li>",'\n').replace("</p>",'\n')
        awards_jiexi1=re.sub(r'[[].*?[]]','',awards_jiexi1)
        awards_jiexi1=re_replace(awards_jiexi1)
        print(awards_jiexi1)
        print("***********")
        update_sql = "update wiki_author_info set awards_jiexihou=%s where id=%s"
        cur.execute(update_sql, (awards_jiexi1, ids))
        conn.commit()
        # print(id,items)

#通过这个wiki_author_info，去zjwl_author 以id查询，更新进去 au_dirth_date au_awards

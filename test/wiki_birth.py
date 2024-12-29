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



conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
sql = 'select id,birth from wiki_author_info where is_download_html=1 and birth_jiexihou is NULL order by  id asc'
# sql = 'select id,source_id,aminer_id,profilePubsTotal,lw_path from aminer where id=797  order by  id asc '
cur.execute(sql)
wk_data = cur.fetchall()
for i in wk_data:
    # id, birth=i
    if i[1]:
        # # 匹配XXXX-XX-XX格式的生日
        # birthday_pattern = re.compile(r'\b\d{4}-\d{2}-\d{2}\b')
        # birth = birthday_pattern.findall(i[1])
        # if birth:
        #     print(birth)
        #     update_sql = "update wiki_author_info set birth_jiexihou=%s where id=%s"
        #     cur.execute(update_sql, (birth[0], i[0]))
        #     conn.commit()

        # # 匹配日月年英文格式的生日
        # birthday_pattern = re.compile(r'(\d{1,4}\s+\w+\s+\d{4})')
        # birth = birthday_pattern.findall(i[1])
        # if birth:
        #     # print(birth)
        #     date_str = birth[0]
        #     format_str = "%d %B %Y"  # %B 是月份的全名
        #     # 使用strptime转换
        #     try:
        #         date = datetime.strptime(date_str, format_str)
        #         # print(date)
        #         formatted_date = date.strftime('%Y-%m-%d')
        #         print(formatted_date)  # 输出: 1944-09-05
        #         update_sql = "update wiki_author_info set birth_jiexihou=%s where id=%s"
        #         cur.execute(update_sql, (formatted_date, i[0]))
        #         conn.commit()
        #     except:
        #         print(date_str)
        #         update_sql = "update wiki_author_info set birth_jiexihou=%s where id=%s"
        #         cur.execute(update_sql, (date_str, i[0]))
        #         conn.commit()

        # 匹配XXXX-XX格式的日期
        # birthday_pattern = re.compile(r'\b\d{4}-\d{2}\b')
        # birth = birthday_pattern.findall(i[1])
        # if birth:
        #     print(birth)
        #     update_sql = "update wiki_author_info set birth_jiexihou=%s where id=%s"
        #     cur.execute(update_sql, (birth[0], i[0]))
        #     conn.commit()

        # # 匹配月年英文格式的日期
        # birthday_pattern = re.compile(r'(\w+\s+\d{4})')
        # birth = birthday_pattern.findall(i[1])
        # if birth:
        #     print(birth)
        #     date_str = birth[0]
        #     format_str = "%B %Y"  # %B 是月份的全名
        #     # 使用strptime转换
        #     try:
        #         date = datetime.strptime(date_str, format_str)
        #         # print(date)
        #         formatted_date = date.strftime('%Y-%m')
        #         print(formatted_date)  # 输出: 1944-09
        #         update_sql = "update wiki_author_info set birth_jiexihou=%s where id=%s"
        #         cur.execute(update_sql, (formatted_date, i[0]))
        #         conn.commit()
        #     except:
        #         print(date_str)
        #         update_sql = "update wiki_author_info set birth_jiexihou=%s where id=%s"
        #         cur.execute(update_sql, (date_str, i[0]))
        #         conn.commit()


        # # 匹配月日年英文日期
        # date_pattern = r"(\w+)\s+(\d+),+\s+(\d+)"
        # # 使用re模块匹配
        # match = re.match(date_pattern, i[1])
        # if match:
        #     try:
        #         # 使用datetime模块转换
        #         month_name = match.group(1)
        #         day = int(match.group(2))
        #         year = int(match.group(3))
        #         # 将月份转换为数字
        #         month_number = datetime.strptime(month_name, "%B").month
        #         # 创建datetime对象
        #         converted_date = datetime(year, month_number, day)
        #         formatted_date = converted_date.strftime('%Y-%m')
        #         print(formatted_date)  # 输出: 1944-09
        #         update_sql = "update wiki_author_info set birth_jiexihou=%s where id=%s"
        #         cur.execute(update_sql, (formatted_date, i[0]))
        #         conn.commit()
        #     except:
        #         pass


        # 匹配XXXX格式日期
        birthday_pattern = re.compile(r'\b\d{4}')
        birth = birthday_pattern.findall(i[1])
        if birth:
            update_sql = "update wiki_author_info set birth_jiexihou=%s where id=%s"
            cur.execute(update_sql, (birth[0], i[0]))
            conn.commit()





# XXXX-XX-XX
# XXXX-XX
# XXXX
import time

from until.sql_tools import mongo_client,mysql_db_conn
from until.time_tool import saveTime
import re
import pycountry
import json
from urllib.parse import unquote
from lxml import etree
def get_country_code(country_name):
    country = pycountry.countries.get(name=country_name)
    if country:
        return country.alpha_2  # 返回国家的 ISO 3166-1 alpha-2 两位缩写
    return None

def country_code_to_name(country_code):
    try:
        country = pycountry.countries.get(alpha_3=country_code)  # 使用 alpha-3 (3字母缩写)
        return country.name if country else "Unknown"
    except Exception as e:
        return f"Error: {e}"

conn=mysql_db_conn(dbname='cg')
cur=conn.cursor()


sql='select id, paln_list_people'
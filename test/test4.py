import time
import logging
from fake_useragent import UserAgent
import MySQLdb
import urllib.parse
import requests
from lxml import etree

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 数据库连接配置
DB_CONFIG = {
    'host': '120.53.84.233',
    'port': 3306,
    'user': 'cg',
    'db': 'cg',
    'charset': 'utf8mb4',
    'password': 'DRDWji3pabfxF6Bx'
}


def mysql_db_conn(dbname=None):
    """建立数据库连接"""
    conn = MySQLdb.connect(**DB_CONFIG)
    return conn


def fetch_ids_and_authfull(cur):
    """从数据库中获取id和authfull"""
    sql = 'SELECT id, authfull FROM get_baike_url LIMIT 10'
    cur.execute(sql)
    return cur.fetchall()


def get_bing_search_url(authfull):
    """生成Bing搜索URL"""
    url_template = "https://www.bing.com/search?q="
    encoded_value = urllib.parse.quote(authfull)
    return url_template + encoded_value


def get_baike_url_from_bing(url_bing):
    """从Bing搜索结果中提取百度百科URL"""
    headers = {
        "User-Agent": UserAgent().random,
    }
    try:
        res = requests.get(url_bing, timeout=20)
        res.raise_for_status()
        tree = etree.HTML(res.text)
        links = tree.xpath('//h2/a/@href')
        for link in links:
            if 'baike.baidu.com' in link:
                return link
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed for URL: {url_bing}, Error: {e}")
        return None


def main():
    conn = mysql_db_conn()
    cur = conn.cursor()
    authfull_cur = conn.cursor()

    ids = fetch_ids_and_authfull(cur)
    for id_value, authfull in ids:
        url_bing = get_bing_search_url(authfull)
        baike_url = get_baike_url_from_bing(url_bing)

        if baike_url:
            logging.info(f"Found Baike URL: {baike_url} for ID: {id_value}")
        else:
            logging.warning(f"No Baike URL found for ID: {id_value}, URL: {url_bing}")

        time.sleep(5)

    cur.close()
    authfull_cur.close()
    conn.close()


if __name__ == "__main__":
    main()

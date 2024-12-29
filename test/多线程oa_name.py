# -*- coding=utf-8 -*-
import queue
import re
import threading
import time
import requests
import urllib3
import MySQLdb
# from tools.sql_tools import mysql_db_conn
from user_agent import generate_user_agent
import  os
import json
def mysql_db_conn(name='localhost',dbname=None):
    global conn
    if name =='localhost':
        # global conn
        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            db=dbname,
            charset='utf8mb4',
            password="1234"
        )
    if name =='21':

        conn = MySQLdb.connect(
            host='192.168.5.12',
            port=3306,
            user='root',
            db=dbname,
            charset='utf8mb4',
            password="1234"
        )
    return conn


lock = threading.Lock()
urllib3.disable_warnings()
globalDict = {"PRODUCT_EXIT": False,
              "CONSUMER_EXIT": False,
              "total_num": 0}


he = {
    "User-Agent": generate_user_agent()

}

def consumerGetData(conQueue):
    while True:
        try:
            # 从队列取出数据
            row = conQueue.get(False)
            return row
        except queue.Empty:
            print("消费者线程等待生产者生产")
            # 判断生产者是否结束
            if not getValue('PRODUCT_EXIT'):
                # 若生产者未结束,则循环等待
                time.sleep(5)
                continue
            else:
                print("队列无知了")
                return False


def setValue(key, value):
    globalDict[key] = value


def getValue(key):
    return globalDict[key]


LIST = []


def ip_parse(ip_str):
    ip = ip_str["http"].replace("http://", "")
    ips = ip.split(":")[0]
    port = ip.split(":")[-1]
    return {"ip": ips, "port": port}


class ProductThread(threading.Thread):
    def __init__(self, product_queue, db_host, db_name, table_name, max_id):
        threading.Thread.__init__(self)
        self.product_queue = product_queue
        self.table_name = table_name
        self.max_id = max_id
        self.conn = mysql_db_conn(name=db_host, dbname=db_name)

    def run(self):
        # print(self.sql)
        ids = 0
        cursor = self.conn.cursor()
        while not getValue('PRODUCT_EXIT'):
            be = time.time()
            sql = f"select id,oa_name,inst_name from {self.table_name}  where id >{ids}  and  is_download=1  order by id asc limit 1000"
            cursor.execute(sql,)
            # cursor.execute(sql)
            mes_list = list(cursor.fetchall())  # ((id,title,source_id)(id,title,source_id))

            print(len(mes_list))
            if len(mes_list) >0 :
                ids = mes_list[-1][0]
                print(f"消费者获取成功，目前最大值{ids}")
                for mes in mes_list:
                    self.product_queue.put((mes))  # 添加入队列
                break

            else:
                setValue("PRODUCT_EXIT", True)
            self.conn.commit()
            print(time.time() - be)


class ConsumerThread(threading.Thread):
    def __init__(self, thread_name, product_queue, proxy_host, db_host, db_name, table_name):
        threading.Thread.__init__(self)
        self.product_queue = product_queue
        self.thread_name = thread_name
        self.lock = threading.RLock()
        self.table_name = table_name
        self.proxy_host = proxy_host
        self.conn = mysql_db_conn(name=db_host, dbname=db_name)
        self.conn_p = mysql_db_conn(name=proxy_host, dbname="proxy")

    def get_proxy_mysql(self,num):
        print("请求新的代理 ",num)
        conn_p = mysql_db_conn(name=self.proxy_host, dbname="proxy")
        cursor_p = conn_p.cursor()
        try_time = 0
        while True:
            try:
                t1 = time.time()
                se_sql = "SELECT `ip`,`port` FROM book_zhi_ma ORDER BY RAND() LIMIT 1"
                cursor_p.execute(se_sql)
                mes_list = list(cursor_p.fetchone())
                if mes_list:
                    proxies = {'http': 'http://%s:%s' % (mes_list[0], mes_list[1]),
                               'https': 'http://%s:%s' % (mes_list[0], mes_list[1])}
                    t2 = time.time()
                    if t2 - t1 > 2:
                        print("太撑了", t2 - t1)
                    se_sql = "delete FROM book_zhi_ma where ip=%s and port=%s"
                    cursor_p.execute(se_sql, (mes_list[0], mes_list[1]))
                    self.conn_p.commit()
                    cursor_p.close()
                    conn_p.close()
                    return proxies
                else:
                    time.sleep(5)
                    continue
            except Exception as e:
                conn_p = mysql_db_conn(name=self.proxy_host, dbname="proxy")
                cursor_p = conn_p.cursor()
                print(f"代理获取失败，第{e.__traceback__.tb_lineno}行发生error为 ", e)
                time.sleep(1)
                try_time += 1
                continue

    def run(self):
        global LIST
        cursor = self.conn.cursor()
        consumer_thread_exit = False
        # with lock:
            # proxy = self.get_proxy_mysql(str(self.thread_name)+" 首次请求ip")
            # print(str(self.thread_name),proxy)
        while not consumer_thread_exit:
            row = consumerGetData(self.product_queue)  # 判断消费者是否结束，结束则取出数据
            if row is False:
                # print("没有啦")
                break
            in_id = row[0]
            oa_name = row[1]
            inst_name=row[2]
            try_time = 0
            url = 'https://searchtest.aminer.cn/aminer-search/search/person'
            query = {"query": "", "needDetails": True, "page": 0, "size": 20, "aggregations": [{"field": "h_index",
                                                                                                "rangeList": [
                                                                                                    {"from": 0,
                                                                                                     "to": 10},
                                                                                                    {"from": 10,
                                                                                                     "to": 20},
                                                                                                    {"from": 20,
                                                                                                     "to": 30},
                                                                                                    {"from": 30,
                                                                                                     "to": 40},
                                                                                                    {"from": 40,
                                                                                                     "to": 50},
                                                                                                    {"from": 50,
                                                                                                     "to": 60},
                                                                                                    {"from": 60,
                                                                                                     "to": 99999}],
                                                                                                "size": 0,
                                                                                                "type": "range"},
                                                                                               {"field": "lang",
                                                                                                "size": 10,
                                                                                                "type": "terms"},
                                                                                               {"field": "nation",
                                                                                                "size": 10,
                                                                                                "type": "terms"},
                                                                                               {"field": "gender",
                                                                                                "size": 10,
                                                                                                "type": "terms"},
                                                                                               {
                                                                                                   "field": "contact.position",
                                                                                                   "size": 20,
                                                                                                   "type": "terms"},
                                                                                               {"field": "org_id",
                                                                                                "size": 200,
                                                                                                "type": "terms"}],
                     "filters": [],
                     "searchKeyWordList": [
                         {"advanced": True, "keyword": f"{oa_name}", "operate": "0", "wordType": 4,
                          "segmentationWord": "True",
                          "needTranslate": True},
                         {"advanced": True, "keyword": f"{inst_name}", "operate": "0", "wordType": 5,
                          "segmentationWord": "True",
                          "needTranslate": True}], "usingSemanticRetrieval": True}

            while try_time < 2:
                try:
                    time.sleep(1)
                    headers = {
                        "content-type": "application/json;charset=UTF-8"
                    }
                    res = requests.post(url=url, data=json.dumps(query),headers=headers, timeout=10)
                    print()
                    if res.status_code ==200:
                        print(res.json())
                    else:
                        print("没有",in_id,oa_name)
            #             reslut_data=res.json()
            #             if reslut_data['success']:
            #                 path = path_html + str(in_id // 10000) + '/' + str(in_id // 100) + '/'
            #                 if os.path.exists(path) is False:
            #                     os.makedirs(path)
            #                 dest_dir = os.path.join(path, str(in_id) +  ".json")
            #                 with open(dest_dir, 'w', encoding='utf8') as ff:
            #                     json.dump(reslut_data, ff,  ensure_ascii=False)
            #                 html_path = dest_dir.replace(path_html[0:1] + ":/", "")
            #                 update_sql = f"update {self.table_name} set zl_detail_path=%s,is_donwload_path=%s where id = %s"
            #                 cursor.execute(update_sql, (html_path, 1, in_id))
            #                 self.conn.commit()
            #                 with lock:
            #                     setValue("total_num", getValue('total_num') + 1)
            #                     # print("done",self.thread_name)
            #                 break
            #             else:
            #                 update_sql = f"update {self.table_name} set is_donwload_path=%s where id = %s"
            #                 cursor.execute(update_sql, (-1, in_id))
            #                 self.conn.commit()
            #                 print(res.text)
            #                 print('下载失败',zl_id)
            #                 break
            #         else:
            #             continue
                except Exception as erro:
                    print(erro,'错误')
                    continue
            # print("消费者%s结束" % self.thread_name)
        setValue("CONSUMER_EXIT", True)


def YNewsTransTitleMain(consumer_thread_size, product_thread_size, queue_max_size, proxy_host, db_host, db_name,
                        table_name, max_id, ):
    """

    :param consumer_thread_size:  生产者线程
    :param product_thread_size:   消费者线程
    :param queue_max_size:        队列大小
    :param proxy_host:            代理host
    :param db_host:               链接数据库的主机名称
    :param db_name:               数据库表明
    :param table_name:            数据库
    :param max_id:                最大id

    :return:
    """
    # 定义queue
    product_queue = queue.Queue(queue_max_size)
    # 创建并开始生产者
    ProductThreadList = []
    for i in range(product_thread_size):
        product = ProductThread(product_queue, db_host, db_name, table_name, max_id)
        ProductThreadList.append(product)
        product.start()
    print("生产者开启完毕")
    time.sleep(2)
    print("队列长度：%s" % product_queue.qsize())
    # 创建并开始消费者
    # time.sleep(100)
    consumer_thread_list = []
    for i in range(consumer_thread_size):
        time.sleep(1)
        consumer = ConsumerThread(i, product_queue, proxy_host, db_host, db_name, table_name, )
        consumer_thread_list.append(consumer)
        consumer.start()
    print("消费者开启完毕")
    lastNum = 0
    while not getValue('CONSUMER_EXIT'):
        printTime = 8.64
        time.sleep(printTime)
        print("队列长度：%s,已处理 %s,%s秒处理xml数量 %s,一天预估数量%s" % (
            product_queue.qsize(), getValue('total_num'), printTime, getValue('total_num') - lastNum,
            (getValue('total_num') - lastNum) * 10000))
        lastNum = getValue('total_num')
    else:
        print("消费者线程出现停止,整个程序开始停止")

    for product in ProductThreadList:
        product.join()
    print("所有生产者线程停止,生产者线程总数%s" % consumer_thread_size)

    for consumer in consumer_thread_list:
        consumer.join()
    print("所有消费者线程停止,消费者线程总数%s" % product_thread_size)
    setValue("PRODUCT_EXIT", False)
    setValue("CONSUMER_EXIT", False)
    setValue("total_num", 0)
    global LIST
    # print(LIST)
    # 还原全局变量的初始化值

path_html=r'Z:/cg_expert_data/html/aminer_zl_detail_json/'

YNewsTransTitleMain(
    consumer_thread_size=20,
    product_thread_size=1,
    queue_max_size=2000,
    proxy_host="21",
    db_host="21",
    db_name="cg",
    table_name="oa_to_aminer",
    max_id=825228,
)





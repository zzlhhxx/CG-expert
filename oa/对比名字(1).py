# -*- coding=utf-8 -*-
import queue

import threading
import time
import requests
import urllib3
import MySQLdb
# from tools.sql_tools import mysql_db_conn
from user_agent import generate_user_agent

import json


def mysql_db_conn(name='localhost', dbname=None):
    global conn
    if name == 'localhost':
        # global conn
        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            db=dbname,
            charset='utf8mb4',
            password="1234"
        )
    if name == '21':
        conn = MySQLdb.connect(
            host='192.168.5.21',
            port=3306,
            user='root',
            db=dbname,
            charset='utf8mb4',
            password="1234"
        )
    if name == '12':
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

proxy = {
    "https": "192.168.5.21:41091",
    "http": '192.168.5.21:41091',
}

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
            # 40000031
            sql = f"select id,doi,aminer_detail_json,work_list_path,oa_name,detail_json from {self.table_name} where  id >%s and aminer_id is null  and is_download=1 order by id asc limit 10000"
            # sql = f"select id,doi,aminer_detail_json,work_list_path,oa_name from {self.table_name} where  id=40000020 "
            cursor.execute(sql, (ids,))
            # cursor.execute(sql)
            mes_list = list(cursor.fetchall())  # ((id,title,source_id)(id,title,source_id))
            print(len(mes_list))
            if len(mes_list) > 0:
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
            doi = row[1]
            aminer_detail_json = row[2]
            work_list_path = row[3]
            oa_name = row[4].lower()
            detail_json=row[5]
            print(detail_json)
            # try_time = 0
            # html_path_list = []
            # address = 'Z:/' + aminer_detail_json
            # # print(address)
            # aminer_data = open(address, 'r', encoding='utf-8').read()
            # aminer_d = json.loads(aminer_data)
            # authors = aminer_d['authors']
            # authors_str = str(authors).lower()
            # oa_name_ = oa_name.replace(".", "").lower()
            # aminer_id = ''
            # name = ''
            #
            # if oa_name in authors_str or oa_name_ in authors_str:
            #     for aminer_author in authors:
            #         if aminer_author.get("id"):
            #             name = aminer_author.get("name")
            #             if not name:
            #                 continue
            #             name_ = name.lower()
            #
            #             if name_ == oa_name or oa_name_ == name_ :
            #                 aminer_id = aminer_author['id']
            #                 print('找到了!!!!', aminer_id, in_id)
            #                 break
            #
            # if aminer_id:
            #     print(aminer_id)

                # update_sql = f"update oa_to_aminer  set aminer_id=%s,aminer_name=%s where id = %s"
                # cursor.execute(update_sql, (aminer_id, name, in_id))
                # self.conn.commit()

            with lock:
                setValue("total_num", getValue('total_num') + 1)
                # print("done",self.thread_name)
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


path_html = r'Z:/cg_expert_data/html/oa_lw/'

YNewsTransTitleMain(
    consumer_thread_size=10,
    product_thread_size=1,
    queue_max_size=2000,
    proxy_host="12",
    db_host="12",
    db_name="cg",
    table_name="oa_to_aminer",
    max_id=825228,
)

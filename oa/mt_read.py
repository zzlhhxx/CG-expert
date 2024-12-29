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
import gzip

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
    if name =='231':
        # global conn
        conn = MySQLdb.connect(
            host='39.162.22.247',
            port=41093,
            user='root',
            db=dbname,
            charset='utf8mb4',
            password="root"
        )
    if name =='21':

        conn = MySQLdb.connect(
            host='192.168.5.21',
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
        cur=self.conn.cursor()
        # print(self.sql)
        mes_list=[]
        sql='select id,path,record_count from oa_path where is_done=0 order by record_count desc  '
        cur.execute(sql)
        data=cur.fetchall()
        for mes in data:

            self.product_queue.put((mes))  # 添加入队列
        # with open(manifest_path, 'r', encoding='utf-8') as f:
        #     data = json.load(f)
        #     entries = data['entries']
        #     for index, ent in enumerate(entries):
        #         url = ent['url']
        #         file_path = url.replace("openalex", "openalex-snapshot").replace("s3://", "E://")
        #         content_length = ent['meta']['content_length']
        #         record_count = ent['meta']['record_count']
        #         # print(f'开始读取：{url} 路径下的gz文件，数据量：content_length：{content_length}，record_count：{record_count}')
        #



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

    def run(self):
        global LIST
        cursor = self.conn.cursor()
        consumer_thread_exit = False
        while not consumer_thread_exit:
            row = consumerGetData(self.product_queue)  # 判断消费者是否结束，结束则取出数据
            if row is False:
                # print("没有啦")
                break
                # id, path, record_count
            ids = row[0]
            file_path = row[1]
            record_count = row[2]
            count=0
            data_batch=[]
            with gzip.open(file_path, 'rt', encoding='utf-8') as f:
                while True:
                    try:
                        line = f.readline()
                        if not line:  # 文件结束
                            break
                        # try:
                        data = json.loads(line.strip())
                        openalex_id = data['id'].replace("https://openalex.org/", '')
                        json_data = json.dumps(data, ensure_ascii=False)
                        topics = data['topics']
                        topics = json.dumps(topics, ensure_ascii=False)

                        data_batch.append((openalex_id, file_path.replace("E://", ''), json_data,topics))
                        if len(data_batch) >= 1000:  # 批量提交
                            count+=len(data_batch)
                            # print(f'路径下：{file_path} ，入库数据量{len(data_batch)}')
                            cursor.executemany(insert_sql, data_batch)
                            self.conn.commit()
                            data_batch = []
                            with lock:
                                setValue("total_num", getValue('total_num') + count)
                                print(f'{file_path}，入库数量：{count},实际数量：{record_count}')
                            # logging.info(f"{count} records processed so far.")

                    except json.JSONDecodeError as e:
                        print(f"JSON decode error in file {file_path}: {e}")
                        continue
                    except Exception as e:
                        print(f"Error processing line: {line.strip()}, Error: {e}")
                        continue

                # 处理剩余不足一批的数据
                if data_batch:
                    cursor.executemany(insert_sql, data_batch)
                    self.conn.commit()

                with lock:
                    count += len(data_batch)
                    update_ = 'update oa_path set is_done=1,count=%s where id=%s'
                    cursor.execute(update_, (count, ids,))
                    self.conn.commit()
                    setValue("total_num", getValue('total_num') + count)
                    print(f'完成，{file_path}，入库数量：{count},实际数量：{record_count},入库id：{ids}')
            #

            # print(f'路径下：{file_path} 读取完成，入库数据量{count}')

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
    # print("队列长度：101053289")
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
             product_queue.qsize(),getValue('total_num'), printTime, getValue('total_num') - lastNum,
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

manifest_path = "E:/openalex-snapshot/data/authors/manifest"
insert_sql = """
    INSERT INTO openalex_author_3(openalex_id, source_path, data_json,topics) 
    VALUES (%s, %s, %s, %s)
"""
YNewsTransTitleMain(
    consumer_thread_size=2,
    product_thread_size=1,
    queue_max_size=2000,
    proxy_host="21",
    db_host="21",
    db_name="cg",
    table_name="openalex_author",
    max_id=825228,
)

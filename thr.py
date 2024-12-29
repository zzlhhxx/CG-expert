# -*- coding=utf-8 -*-
import json
import os
import queue
import re
import thr
import time
import MySQLdb
import requests
from lxml import etree

IMAGE_PATH = "D:/cg_source_data/battles/dbpedia/"


def sqlCon(con_name="localhost", db_name="news"):
    global conn
    if con_name == "localhost":
        conn = MySQLdb.connect(host='localhost', port=3306, user='root', db=db_name, charset='utf8mb4',
                               password="1234")
    return conn


globalDict = {"PRODUCT_EXIT": False,
              "CONSUMER_EXIT": False,
              "totalNum": 0}


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
                return False


def setValue(key, value):
    globalDict[key] = value


def getValue(key):
    return globalDict[key]


from urllib import request

User_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.42"

he = {
    "User-Agent": User_Agent,
}


class ProductThread(threading.Thread):
    def __init__(self, wwzlQueue, db_name, table_name, max_id):
        threading.Thread.__init__(self)
        self.wwzlQueue = wwzlQueue
        self.table_name = table_name
        self.max_id = max_id
        self.conn = sqlCon(con_name="localhost", db_name=db_name)

    def run(self):
        cursor = self.conn.cursor()
        # sql = "SELECT id,detail_url from battles where titles is null and 10097 <= id and id  <= 12754 order by id asc "
        sql = "SELECT id,detail_url from battles WHERE  title not like 'No Name' and titles like 'None' "
        cursor.execute(sql)
        mes_list = list(cursor.fetchall())
        self.conn.commit()
        for mes in mes_list:
            try:
                self.wwzlQueue.put(mes)
            except Exception as e:
                print(e)
                continue
        setValue("PRODUCT_EXIT", True)


class ConsumerThread(threading.Thread):
    def __init__(self, threadName, wwzlQueue, db_name, table_name):
        threading.Thread.__init__(self)
        self.wwzlQueue = wwzlQueue
        self.threadName = threadName
        self.lock = threading.RLock()
        self.cc = requests.session()
        self.table_name = table_name
        self.conn = sqlCon(con_name="localhost", db_name=db_name)

    def run(self):
        cursor = self.conn.cursor()
        global totalNum
        CONSUMER_TYHREAD_EXIT = False
        while not CONSUMER_TYHREAD_EXIT:
            is_to_table = True
            row = consumerGetData(self.wwzlQueue)
            if row is False:
                # 若能获取值则继续,否则程序结束
                break
            pass
            detail_url = row[1]
            ids = detail_url.split('/')[-1]
            in_id = row[0]
            try_time = 0
            url = "https://www.wikidata.org/w/api.php"
            params = {
                'ids': ids,  # 实体id,可多个，比如'Q123|Q456'
                'action': 'wbgetentities',
                'format': 'json',
                'language': 'en',
            }
            res = requests.get(url=url, params=params)
            json_data = res.json()
            data_re = re.findall("""'enwiki': {'site': 'enwiki', 'title': "(.*?)", .*?}""", str(json_data), re.S)
            print(data_re, ids)
            time.sleep(2)
            while try_time < 2:
                try:
                    if len(data_re) > 0:
                        data = data_re[0]
                        print('入库titles', data)
                        # update battles set titles=%s where id=%s and titles is null
                        update_sql = "update " + self.table_name + " set titles=%s, is_ava=%s where id = %s"
                        cursor.execute(update_sql, (data, 1, in_id))
                        self.conn.commit()
                        self.lock.acquire()
                        setValue("totalNum", getValue('totalNum') + 1)
                        self.lock.release()
                        print("成功", in_id)
                        break
                    else:
                        data = "None"
                        update_sql = "update " + self.table_name + " set titles=%s,is_ava=%s where id = %s"
                        cursor.execute(update_sql, (data, -1, in_id))
                        self.conn.commit()
                        self.lock.acquire()
                        setValue("totalNum", getValue('totalNum') + 1)
                        self.lock.release()
                        print("没有title,is_ava=-1", in_id)
                        break
                except Exception as e:
                    print(e)
                    try_time += 1
                    continue
        print("消费者%s结束" % self.threadName)
        setValue("CONSUMER_EXIT", True)


# 1 有值 -1 无值 -2 文件类型错误 -3 404   -4 采集失败
# is_replace_path_image  1 下载正确 2下载不正确，但可以入库
def get_titles(ConsumerThreadSize, ProductThreadSize, queueMaxSize, db_name, table_name, max_id):
    # 定义queue
    wwzlQueue = queue.Queue(queueMaxSize)
    # 创建并开始生产者
    ProductThreadList = []
    for i in range(ProductThreadSize):
        product = ProductThread(wwzlQueue, db_name, table_name, max_id)
        ProductThreadList.append(product)
        product.start()
    print("生产者开启完毕")
    time.sleep(2)
    print("队列长度：%s" % wwzlQueue.qsize())
    # 创建并开始消费者
    ConsumerThreadList = []
    for i in range(ConsumerThreadSize):
        time.sleep(0.2)
        consumer = ConsumerThread(i, wwzlQueue, db_name, table_name)
        ConsumerThreadList.append(consumer)
        consumer.start()
    print("消费者开启完毕")
    lastNum = 0
    while not getValue('CONSUMER_EXIT'):
        printTime = 1
        time.sleep(printTime)
        print("队列长度：%s,已处理 %s,%s秒处理xml数量 %s" % (
            wwzlQueue.qsize(), getValue('totalNum'), printTime, getValue('totalNum') - lastNum))
        lastNum = getValue('totalNum')
    else:
        print("消费者线程出现停止,整个程序开始停止")

    for product in ProductThreadList:
        product.join()
    print("所有生产者线程停止,生产者线程总数%s" % ConsumerThreadSize)

    for consumer in ConsumerThreadList:
        consumer.join()
    print("所有消费者线程停止,消费者线程总数%s" % ProductThreadSize)
    setValue("PRODUCT_EXIT", False)
    setValue("CONSUMER_EXIT", False)
    setValue("totalNum", 0)

    # 还原全局变量的初始化值


get_titles(10, 1, 100000, "news", "battles", 0)

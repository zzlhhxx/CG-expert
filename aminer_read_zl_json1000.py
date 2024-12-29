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
import  os

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
        # print(self.sql)
        ids = 0
        cursor = self.conn.cursor()
        while not getValue('PRODUCT_EXIT'):
            be = time.time()
            sql = f"select id,aminer_id,zl_path,source_id from {self.table_name}  where id >%s  and  is_ava=1 and source_id>1843 order by id asc limit 1"
            cursor.execute(sql, (ids,))
            # cursor.execute(sql)
            data=cursor.fetchall()
            mes_list = list(data)  #  ((id,f_id,zl_id,source_id),(id,f_id,zl_id,source_id))  (1, 23, '66bdb0a4b94ee990d59c330d', 1)

            if len(mes_list) >0 :
                ids = mes_list[-1][0] #获取最大id
                print(f"消费者获取成功，目前最大值{ids}")

                print(ids)
                #目前最大值23  #目前最大值87
                for mes in mes_list:
                    # self.product_queue.put(mes)  # 添加入队列
                    self.product_queue.put(mes)  # 添加入队列
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

    # def get_proxy_mysql(self,num):
    #     print("请求新的代理 ",num)
    #     conn_p = mysql_db_conn(name=self.proxy_host, dbname="proxy")
    #     cursor_p = conn_p.cursor()
    #     try_time = 0
    #     while True:
    #         try:
    #             t1 = time.time()
    #             se_sql = "SELECT `ip`,`port` FROM book_zhi_ma ORDER BY RAND() LIMIT 1"
    #             cursor_p.execute(se_sql)
    #             mes_list = list(cursor_p.fetchone())
    #             if mes_list:
    #                 proxies = {'http': 'http://%s:%s' % (mes_list[0], mes_list[1]),
    #                            'https': 'http://%s:%s' % (mes_list[0], mes_list[1])}
    #                 t2 = time.time()
    #                 if t2 - t1 > 2:
    #                     print("太撑了", t2 - t1)
    #                 se_sql = "delete FROM book_zhi_ma where ip=%s and port=%s"
    #                 cursor_p.execute(se_sql, (mes_list[0], mes_list[1]))
    #                 self.conn_p.commit()
    #                 cursor_p.close()
    #                 conn_p.close()
    #                 return proxies
    #             else:
    #                 time.sleep(5)
    #                 continue
    #         except Exception as e:
    #             conn_p = mysql_db_conn(name=self.proxy_host, dbname="proxy")
    #             cursor_p = conn_p.cursor()
    #             print(f"代理获取失败，第{e.__traceback__.tb_lineno}行发生error为 ", e)
    #             time.sleep(1)
    #             try_time += 1
    #             continue

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
            print(row)   #(1, 23, '66bdb0a4b94ee990d59c330d', 1)
                        #id,aminer_id,zl_path,source_id

            try_time = 0

            # url = f'https://www.aminer.cn/patent/{zl_id}'
            # while try_time < 2:
            #     try:
            #         time.sleep(1)
            #         # res = requests.get(url=url, headers=he, proxies=proxy, timeout=10)
            #         res = requests.get(url=url, headers=he, timeout=10)
            #         # print(res.text)
            #
            #         if res.status_code ==200:
            #             path = path_html + str(in_id // 10000) + '/' + str(in_id // 100) + '/'
            #
            #             if os.path.exists(path) is False:  #判断路径是空吗，不存在就创建
            #                 os.makedirs(path)
            #             dest_dir = os.path.join(path, str(in_id) + ".html")
            #             # print(dest_dir)
            #             with open(dest_dir, 'wb', ) as ff:
            #                 ff.write(res.content)
            #             html_path = dest_dir.replace(path_html[0:1] + ":/", "")
            #
            #             #id,f_id,zl_id,source_id
            #             update_sql = f"update {self.table_name} set zl_detail_path=%s,is_donwload_path=%s where id = %s"
            #             cursor.execute(update_sql, (html_path, 1, in_id))
            #             self.conn.commit()
            #
            #             with lock:
            #                 setValue("total_num", getValue('total_num') + 1)
            #                 # print("done",self.thread_name)
            #             time.sleep(5)
            #             break
            #
            #         elif "尝试验证码的次数" in res.text or "ip封禁" in res.text or "验证码" in res.text or "跳转到登录页" in res.text:
            #             with lock:
            #                 proxy = self.get_proxy_mysql(str(self.thread_name)+"ip封禁")
            #                 # print(proxy)
            #                 time.sleep(3)
            #                 # try_time += 1
            #             continue
            #         else:
            #             update_sql = "update book_best set is_ava=-3,is_job_url=-3 where id=%s"
            #             cursor.execute(update_sql, (in_id,))
            #             self.conn.commit()
            #
            #
            #     except Exception as erro:
            #         print(erro)
            #         if "time" not in str(erro):
            #             print(f"失败，重试,,,{erro}")
            #         with lock:
            #             proxy = self.get_proxy_mysql(str(self.thread_name)+" 代理非time时间的其他问题")
            #             time.sleep(2)
            #         try_time += 1
            #         # print(f"重试尝试{try_time},{proxy}")
            #         continue
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
    # 创建并开始生产者，从指定的数据库中获取连接地址，放入队列中
    ProductThreadList = []
    for i in range(product_thread_size):
        product = ProductThread(product_queue, db_host, db_name, table_name, max_id)
        ProductThreadList.append(product)
        product.start()

    print("生产者开启完毕")
    time.sleep(2)
    print("队列长度：%s" % product_queue.qsize())

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

path_html=r'Y:/cg_expert_data/html/aminer_zl_1000/'   #下载存储的路径

YNewsTransTitleMain(
    consumer_thread_size=5,
    product_thread_size=1,
    queue_max_size=2000,
    proxy_host="21",
    db_host="21",
    db_name="cg",
    table_name="aminer",
    max_id=0,
)

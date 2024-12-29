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
from until.sql_tools import mongo_client, mysql_db_conn
import re
import json
from until.time_tool import timestamp_to_date_str
import datetime


mongo_db = mongo_client('cg')
c = mongo_db['zjwl_zl']

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
            sql = f"select id,zl_id,zl_detail_path from {self.table_name} where  id >%s and is_donwload_path=1 and is_to_mongo=0 order by id asc limit 1000"
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
            ids = row[0]
            zl_id = row[1]
            zl_detail_path = row[2]
            address = 'Z:/' + zl_detail_path
            try:
                data = open(address, 'r', encoding='utf-8').read()

                json_data = json.loads(data)

                if json_data:

                    patents = json_data['data'][0]
                    if not patents:
                        print('不完整')
                        continue
                    title = ''
                    if patents.get("title"):
                        for k1, v1 in patents['title'].items():

                            if k1 == 'en':
                                title = v1[0]
                            elif k1 == 'zh':
                                title = v1[0]
                            else:
                                title = v1[0]
                                # print(k1)
                    summary = ''
                    if patents.get("abstract"):
                        for k2, v2 in patents['abstract'].items():
                            if k2 == 'en':
                                summary = v2[0]
                            elif k2 == 'zh':
                                summary = v2[0]
                            else:
                                summary = v2[0]
                                # print(k1)

                    claims = ''

                    if patents.get("claims"):
                        for k3, v3 in patents['claims'].items():
                            if k3 == 'en':
                                claims = v3
                                # print(v3)
                            elif k3 == 'zh':
                                claims = v3
                            else:
                                claims = v3
                            if claims:
                                if len(claims):
                                    claims = "\n".join(claims).strip()
                    keywords = []

                    kind = patents['pub_kind'] if patents.get('pub_kind') else ''  # 专利种类
                    country = patents['country'] if patents.get("country") else ''

                    pub_num = patents['pub_num'] if patents.get("pub_num") else ''  # 公开发布号

                    country_ = ''
                    for cc in country:
                        country_ += cc.capitalize()  # 首字母大写

                    num = country_ + pub_num + kind  # 专利号

                    # 发明人和发明机构  设置列表append函数放入列表

                    inventor_list = []
                    if patents.get("inventor"):
                        for inv in patents['inventor']:
                            inv_div = {
                                "name": inv['name'],
                                "organs": [],
                            }
                            if inv.get("person_id"):
                                person_id = inv['person_id']
                                inv_div['person_id'] = person_id

                            inventor_list.append(inv_div)
                    ipc_list = []
                    ipcs = patents.get("ipc")  # ipc
                    if ipcs:
                        for ipc in ipcs:
                            if not ipc.get("l4"):
                                continue
                            ipc_h = ipc['l4']
                            ipc_list.append({
                                'num': ipc_h,
                            })
                    cpc_list = []
                    cpcs = patents.get("cpc")  # ipc
                    if cpcs:
                        for cpc in cpcs:
                            if cpc.get("raw"):
                                cpc_h = cpc['raw']
                            else:
                                cpc_h = cpc['l4']
                            cpc_list.append({
                                'num': cpc_h,
                            })
                    pub_date = ''
                    if patents.get('pub_date'):
                        pub_date = patents['pub_date']['seconds']

                        if pub_date > 0:
                            pub_date = timestamp_to_date_str(pub_date, '%Y-%m-%d')
                        else:
                            pub_date = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=pub_date)
                        print(pub_date)

                    app_num = patents['app_num'] if patents.get("app_num") else ''  # 申请号
                    app_date = patents.get("app_date")

                    if app_date:
                        app_date = app_date['seconds']

                        if app_date > 0:

                            if type(app_date) == type(1):

                                app_date = timestamp_to_date_str(app_date, '%Y-%m-%d')
                            else:
                                app_date = timestamp_to_date_str(app_date['seconds'], '%Y-%m-%d')
                        else:
                            app_date = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=app_date)

                    assignee = []
                    if patents.get("assignee"):
                        assignee_names = patents['assignee']  #
                        for ass in assignee_names:
                            assignee.append({
                                "name": ass['name'],
                                "organs": [],
                            })
                    applicant = []
                    if patents.get("applicant"):
                        applicant_names = patents['applicant']  #
                        for appl in applicant_names:
                            applicant.append({
                                "name": appl['name'],
                                "organs": [],
                            })
                        # print(applicant_names)
                    law_status = ''  #
                    cited_count_total = 0  # 申请人名
                    net_address = f"https://www.aminer.cn/patent/{patents['id']}"
                    pub_date = str(pub_date)
                    app_date = str(app_date)
                    pub_date = pub_date.replace("00:00:00", "")
                    app_date = app_date.replace("00:00:00", "")
                    print(pub_date, app_num)
                    au_patent = {
                        "_id": patents['id'],
                        "title": title,
                        "summary": summary,
                        "claim": claims,
                        "keywords": keywords,
                        "num": num,
                        "kind": kind,
                        "country": country_,
                        "inventors": inventor_list,
                        "patentees": assignee,
                        "ipc": ipc_list,
                        "cpc": cpc_list,
                        "pub_num": pub_num,
                        "pub_date": pub_date,
                        "app_num": app_num,
                        "app_date": app_date,
                        "assignee": applicant,
                        "law_status": law_status,
                        "cited_count_total": cited_count_total,
                        "net_address": [net_address],
                    }
                    if not c.find_one({"_id": patents['id']}):
                        c.insert_one(au_patent)
                    update_ = 'update aminer_zl set is_to_mongo=1 where id=%s'
                    cursor.execute(update_, (ids,))
                    self.conn.commit()
                else:
                    print(zl_id, data)

            except Exception as e:
                print(e, ' ', address, ids, app_date)


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
    table_name="aminer_zl",
    max_id=825228,
)

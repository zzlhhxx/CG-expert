# -*- coding=utf-8 -*-
import json
import queue
import threading
import time
import traceback
import MySQLdb
import urllib3

lock = threading.RLock()


def mysql_db_conn(name="12", dbname=None):
    conn = MySQLdb.connect(host='192.168.5.12', port=3306, user='root', db=dbname, charset='utf8mb4',
                           password="1234")

    return conn


# -*- coding=utf-8 -*-
import time
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

urllib3.disable_warnings()

PDF_PATH = "D:/cg_source_data/pdf/"
globalDict = {"PRODUCT_EXIT": False,
              "CONSUMER_EXIT": False,
              "total_num": 0}


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

key_ = [
    {
        # 浩博
        "SPARKAI_APP_ID": '733d8d1d',
        "SPARKAI_API_SECRET": 'ZmU2NzIwMjcwYmNhN2NiNjViOWUzZjEw',
        "SPARKAI_API_KEY": 'a6b13652d052b8151a9477f38314716c',
    },
    {
        # 虎子
        "SPARKAI_APP_ID": 'f690a584',
        "SPARKAI_API_SECRET": 'NGM2YmRjOWM4YTljYzg1NmMyMDkzZDQ1',
        "SPARKAI_API_KEY": '3e612b0199a13a1c5c312bd820d100fa',
    }, {
        # 泽磊
        "SPARKAI_APP_ID": '714f8ce8',
        "SPARKAI_API_SECRET": 'N2E0M2UyMmYwOWIyYzA4NjNkMzZjNTUw',
        "SPARKAI_API_KEY": '469a714f466d7682090e5bf04d14c783',
    }, {
        # 星合
        "SPARKAI_APP_ID": '0d7343ef',
        "SPARKAI_API_SECRET": 'NjViYTRiZjU2MGQ4YjRmNDliMmRhOWNk',
        "SPARKAI_API_KEY": 'faa48c0bb8e42757d536f7255ef9dc8a',
    }, {
        # 星宇
        "SPARKAI_APP_ID": '93be3ce8',
        "SPARKAI_API_SECRET": 'ZWI3NjViMWQ4ZGI2ZjllNmFkOTU3YWMz',
        "SPARKAI_API_KEY": '11c2baa50c263800ef9c59575ae43c13',
    }, {
        # 玉朵科技
        "SPARKAI_APP_ID": 'd0b3d7d3',
        "SPARKAI_API_SECRET": 'OWE5MmRiYjhmMGZmNjZiNTQxYWM4NWQ0',
        "SPARKAI_API_KEY": '65674cc66faf667ced8779ee78b00842',
    },
 {
        # 曹鑫
        "SPARKAI_APP_ID": '94836e48',
        "SPARKAI_API_SECRET": 'M2UxYjY4MTYxNTYwNWM4MjE1ZjJhNDJh',
        "SPARKAI_API_KEY": '82013040a8567b23cedbe87c7aed66bb',
    },
 {
        # 盖青峰
        "SPARKAI_APP_ID": 'e21f11e4',
        "SPARKAI_API_SECRET": 'NzcyMTdkNTJmOTc4MWM2MjQzNzg0NTcy',
        "SPARKAI_API_KEY": '79d35e4b94b344b074c4ec2f4f60dfcc',
    },

]


def ip_parse(ip_str):
    ip = ip_str["http"].replace("http://", "")
    ips = ip.split(":")[0]
    port = ip.split(":")[-1]
    return {"ip": ips, "port": port}


class ProductThread(threading.Thread):
    def __init__(self, product_queue, db_host, db_name, table_name, field, max_id):
        threading.Thread.__init__(self)
        self.product_queue = product_queue
        self.table_name = table_name
        self.field = field
        self.max_id = max_id
        self.conn = mysql_db_conn(name=db_host, dbname=db_name)

    def run(self):
        ids = 0
        cursor = self.conn.cursor()
        while not getValue('PRODUCT_EXIT'):
            be = time.time()
            # sql = f"select ids,jianjie from  awards_xunfei where is_ava=0 and ids >%s order by ids desc limit 1 "
            sql = f"select ids,jianjie from  awards_xunfei where ids=10000011"
            # cursor.execute(sql, (ids,))
            cursor.execute(sql,)
            requestDataMessageList = list(cursor.fetchall())
            print(len(requestDataMessageList))
            if len(requestDataMessageList) > 0:
                ids = requestDataMessageList[-1][0]
                for requestDataMessage in requestDataMessageList:
                    self.product_queue.put(requestDataMessage)
                break
            else:
                setValue("PRODUCT_EXIT", True)
            print(time.time() - be)


class ConsumerThread(threading.Thread):
    def __init__(self, thread_name, product_queue, proxy_host, db_host, db_name, table_name, field):
        threading.Thread.__init__(self)
        self.product_queue = product_queue
        self.field = field  # 翻译字段
        self.thread_name = thread_name
        self.lock = threading.RLock()
        self.conn = mysql_db_conn(name=db_host, dbname=db_name)

    def run(self):
        global LIST
        consumer_thread_exit = False
        cursor = self.conn.cursor()
        apple = key_[self.thread_name]
        SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'
        SPARKAI_APP_ID=apple['SPARKAI_APP_ID']
        SPARKAI_API_KEY=apple['SPARKAI_API_KEY']
        SPARKAI_API_SECRET=apple['SPARKAI_API_SECRET']
        SPARKAI_DOMAIN = 'generalv3.5'
        spark = ChatSparkLLM(
            spark_api_url=SPARKAI_URL,
            spark_app_id=SPARKAI_APP_ID,
            spark_api_key=SPARKAI_API_KEY,
            spark_api_secret=SPARKAI_API_SECRET,
            spark_llm_domain=SPARKAI_DOMAIN,
            streaming=False,
            request_timeout=20,

        )
        index=0
        while not consumer_thread_exit:
            row = consumerGetData(self.product_queue)
            if row is False:
                break
            ids = row[0]
            edu = row[1]
            if edu:
                try:
                    t1=time.time()
                    edu = edu.replace("Taiwan", 'TaiwanProvince')
                    # str = '"name":,"college":"","degree":"","country":"","content":"",'
                    # edustr = """你现在是一个全球大学数据库，现在有一个字符串，你去提取学校相关的字段，然后对这个你根据这个字符串意思，进行合理切割，得到一个列表，然后针对每一个列表进行解析得出 name-字符串出现的学校，degree-出现的学位信息，country-大学所在的国家（要求大写简称），college-出现的学院或者系别，最后把当前解析的文本，放入到text中，最终形成一个JSON。得出的json格式为{index:"",["data":[解析得到的元素]},如果没有找到就留空就行。但是要求一定要准确！你直接返回一个json数组就行，不用说其他的，直接把数组返回出来就行。字段格式样按照我写的，不能新增和删除！不用换行！。字符串为："""
                    # edustr="""你现在是一个全球大学数据库，现在有一个字符串，你去提取学校相关的字段，然后对这个你根据这个字符串意思，进行合理切割，得到一个列表，然后针对每一个列表进行解析得出 name-字符串出现的学校名称！，degree-出现的学位信息，country-大学所在的国家（要求大写简称），college-出现的学院或者系别，最后把当前解析的文本，放入到text中，最终形成一个字符串。要个格式一定要以我的为准，如果解析不到，要留空！。格式为text:"", name:"", degree:"",country:"", college:""<br>text:"", name:"", degree:"",country:"", college:"",如果没有找到就留空就行。但是要求一定要准确！直接返回字符串就行，不用说其他的，字段格式样按照我写的，不能新增和删除！。字符串为："""
                    # edustr="""你现在是一个全球专家数据库，现在有一串字符串，如果在字符串中有专家的出生年月和获得荣誉奖项，就把专家的出生年月和获得荣誉奖项提取出来，如果没有就根据字符串内容进行全网搜索，返回准确的专家的出生年月和获得荣誉奖项。返回的结果中出生年月和获得荣誉奖项之间用两个英文逗号分隔，获得荣誉奖项用两个<br>包裹起来，返回的结果类型为字符串"""
                    edustr = """你现在是一个全球专家数据库，现在有一串字符串，如果在字符串中有专家的出生年月和获得荣誉奖项，就把专家的出生年月和获得荣誉奖项提取出来，如果有多个荣誉请用<br>标签连接起来。返回的字符串格式为year:,awards:，返回的结果类型为字符串.要求不能更改我的格式，如果解析不到，直接留空！因为我要解析你发给我的字段，所以格式一定要精准！"""
                    edustr=edustr+" "+edu
                    messages = [ChatMessage(
                        role="user",
                        content=edustr
                    )]
                    handler = ChunkPrintHandler()
                    a = spark.generate([messages], callbacks=[handler])
                    if a:
                        text = a.generations[0][0].text
                        # update_ = 'update edu_xunfei set str_content=%s,is_done=1 where id=%s'
                        # cursor.execute(update_, (text, ids,))
                        # self.conn.commit()
                        t2 = time.time()
                        print(text)
                        print(edu)
                        index += 1
                        with lock:
                            setValue("total_num", getValue('total_num') + 1)
                            # print("done",self.thread_name)
                        print(f'入库1条数据,需要时间：{int(t2 - t1)}')
                        time.sleep(2)

                except Exception as e:
                    # update_ = 'update edu_xunfei set is_done=-1 where id=%s'
                    # cursor.execute(update_, ( ids,))
                    # self.conn.commit()
                    print('错误',e,self.thread_name)
                    time.sleep(2)
                    continue
        # print("消费者%s结束" % self.thread_name)
        setValue("CONSUMER_EXIT", True)


def youtube_trans_youdao_main(consumer_thread_size, product_thread_size, queue_max_size, proxy_host, db_host, db_name,
                              table_name, field, max_id):
    product_queue = queue.Queue(queue_max_size)
    ProductThreadList = []
    for i in range(product_thread_size):
        product = ProductThread(product_queue, db_host, db_name, table_name, field, max_id)
        ProductThreadList.append(product)
        product.start()
    print("生产者开启完毕")
    time.sleep(5)
    print("队列长度：%s" % product_queue.qsize())
    consumer_thread_list = []
    for i in range(consumer_thread_size):
        time.sleep(20)
        consumer = ConsumerThread(i, product_queue, proxy_host, db_host, db_name, table_name, field)
        consumer_thread_list.append(consumer)
        consumer.start()
    print("消费者开启完毕")
    lastNum = 0
    while not getValue('CONSUMER_EXIT'):
        printTime = 86.4
        time.sleep(printTime)
        print("队列长度：%s,已处理 %s,%s秒处理xml数量 %s,一天预估数量%s" % (
            product_queue.qsize(), getValue('total_num'), printTime, getValue('total_num') - lastNum,
            (getValue('total_num') - lastNum) * 1000))
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



youtube_trans_youdao_main(
    consumer_thread_size=1,
    product_thread_size=1,
    queue_max_size=1000,
    proxy_host="12",
    db_host="12",
    db_name="cg",
    table_name="awards_xunfei",
    field="1",
    max_id=0)

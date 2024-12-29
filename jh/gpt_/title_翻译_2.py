# -*- coding=utf-8 -*-
import queue
import threading
import time
import traceback

import MySQLdb
import openai
import urllib3

lock = threading.RLock()

def mysql_db_conn(name="du_he", dbname=None):
    conn = MySQLdb.connect(host='36.99.121.186', port=3306, user='dubingcao', db="dubingcao", charset='utf8mb4',
                               password="rdyiHXBTaxkcafYi")

    return conn

urllib3.disable_warnings()

PDF_PATH = "D:/cg_source_data/pdf/"
globalDict = {"PRODUCT_EXIT": False,
              "CONSUMER_EXIT": False,
              "total_num": 0}


openai.api_key = "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"
openai.proxy = "http://192.168.50.251:41091"

# openai.api_key = "sk-XCjt7NNwyJMLsYSvN58cPlWFgsryiemPoylYVlVSZsKAn3Qn"#我
# openai.api_key = "sk-l51leHDKOnvi0l1asYVv6Yc7GjOt1oos3eStu8xQ7KDaZkOz"#徐伟佳 50
# openai.api_key = "sk-t9YtIssYM5d9Do1GQ8EgZChcOfgI8UYREORWdRlHHBrDmnEY"#刘杰
# openai.api_key = "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"
# openai.api_key = "sk-tS3MKvnOCg8sID7Us22mjA8HCubdIOL9spuvFz4oaEicT0p5"#梁成虎
# openai.api_base = "https://api.chatanywhere.com.cn/v1"
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
    def __init__(self, product_queue, db_host, db_name, table_name, field, max_id):
        threading.Thread.__init__(self)
        self.product_queue = product_queue
        self.table_name = table_name
        self.field = field
        self.max_id = max_id

    def run(self):
        ids = 1000000
        while not getValue('PRODUCT_EXIT'):
            conn = mysql_db_conn(name="", dbname="pilimi")
            cursor = conn.cursor()
            be = time.time()
            sql = f"select zlibrary_id,title from books_title where zlibrary_id>%s and `is_trans`=-1 and zlibrary_id%% 3 = 2 order by zlibrary_id asc limit 1000"
            cursor.execute(sql, (ids,))
            requestDataMessageList = list(cursor.fetchall())
            if len(requestDataMessageList) > 0:
                ids = requestDataMessageList[-1][0]
                print(ids)
                for requestDataMessage in requestDataMessageList:
                    self.product_queue.put(requestDataMessage)
            else:
                setValue("PRODUCT_EXIT", True)
            cursor.close()
            conn.close()
            print(time.time() - be)



class ConsumerThread(threading.Thread):
    def __init__(self, thread_name, product_queue, proxy_host, db_host, db_name, table_name, field):
        threading.Thread.__init__(self)
        self.product_queue = product_queue
        self.field = field  # 翻译字段
        self.thread_name = thread_name
        self.lock = threading.RLock()


    def run(self):
        global LIST
        consumer_thread_exit = False
        vars = ''
        nums = 0
        need_time = 0
        while not consumer_thread_exit:
            row = consumerGetData(self.product_queue)
            if row is False:
                break
            if row[1]:
                vars_before = "翻译工作：以下数据格式为 数字序号🤝图书名称\n数字序号🤝图书名称\n...。不同图书名可能不同语言，请逐行，将图书名称根据其语言的实际情况，翻译为简体中文 输出格式为 数字序号🤝翻译后的图书名称。 不需要有其他解释：\n"
                vars_single = f'{row[0]}🤝{row[1]}\n'
                try:
                    vars += vars_single
                    if nums < 110:
                        nums += 1
                    else:
                        conn = mysql_db_conn(name="", dbname="dubingcao")
                        cursor = conn.cursor()
                        vars = vars_before + vars[0:-1]

                        # print(vars)
                        messages = [{'role': 'user', 'content': vars}]
                        print(messages)
                        s_time = time.time()
                        completion = openai.ChatCompletion.create(timeout=10, model="gpt-3.5-turbo-16k",
                                                                  messages=messages,temperature=0)
                        dd = completion.choices[0].message.content
                        end_time = time.time()
                        need_time = end_time - s_time
                        if need_time < 30:
                            time.sleep(30 - int(need_time))
                        print(dd.replace("\n", "\\n"))
                        if dd:
                            if "🤝" in dd:
                                for title_mes in dd.split("\n"):
                                    try:
                                        id = title_mes.split("🤝")[0]
                                        title_cn = title_mes.split("🤝")[1]
                                        # print(id,"   ",title_cn)
                                        update_sql = f"update books_title set `title_cn` = %s ,`is_trans`=%s where zlibrary_id =%s"
                                        cursor.execute(update_sql, (title_cn, 1, id))
                                        self.lock.acquire()
                                        conn.commit()
                                        setValue("total_num", getValue('total_num') + 1)
                                        self.lock.release()
                                    except Exception as e:
                                        print(e)
                                        continue
                            else:
                                time.sleep(100)
                        vars = ""
                        nums = 0
                        print(f"请求用时{need_time}")
                        cursor.close()
                        conn.close()
                except Exception as e:
                    vars = ""
                    nums = 0
                    traceback.print_exc()
                    print("ERROR:", e)
                    if "502" not in str(e):
                        time.sleep(300)
                    continue
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


if __name__ == '__main__':
    while True:
        youtube_trans_youdao_main(
            consumer_thread_size=1, product_thread_size=1,
            queue_max_size=2900,
            proxy_host="231", db_host="du_he",
            db_name="dubingcao", table_name="1",
            field="1", max_id=0)


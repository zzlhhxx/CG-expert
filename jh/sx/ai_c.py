#!/usr/local/bin/python3.8
# -*- coding: utf8 -*-
# 调用openai api的步骤
# 1. 安装openai库 pip install openai
# 2. 设置openai的api_key
# 3. 调用openai的api
# 4. 参考文档
# https://platform.openai.com/docs/api-reference/completions/create
# https://platform.openai.com/docs/api-reference/authentication
# https://platform.openai.com/docs/api-reference/completions/create
# https://platform.openai.com/docs/libraries/community-libraries


import os
import openai
from until.sql_tools import mysql_db_conn, getStrAsMD5
import json
# 1. 准备好请求的url
#openai.organization = "YOUR_ORG_ID" #
#openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.api_key = "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" # 要更换成自已的API KEY
openai.api_key = "sk-qJe1TmuguRO0Pa7h2f12E073B76349AcB4Ab0bB9786277B4" # 要更换成自已的API KEY
# openai.api_key = "sk-m8cwIrFCGiKti8z4ZyihlXkL5ki2HyjhKtU3Wft0b5XiuNqQ" # 泽磊
# openai.api_key = "sk-XCjt7NNwyJMLsYSvN58cPlWFgsryiemPoylYVlVSZsKAn3Qn"#我
# openai.api_key = "sk-l51leHDKOnvi0l1asYVv6Yc7GjOt1oos3eStu8xQ7KDaZkOz"#徐伟佳
# openai.api_key = "sk-t9YtIssYM5d9Do1GQ8EgZChcOfgI8UYREORWdRlHHBrDmnEY"#刘杰
# openai.api_key = "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"
# openai.api_key = "sk-tS3MKvnOCg8sID7Us22mjA8HCubdIOL9spuvFz4oaEicT0p5"#梁成虎
# 查看可以使用的模型列表
openai.proxy = "http://192.168.5.21:41091"



def get_model_list():
    models= openai.Model.list()
    print(models)
# 生成文本示例
def generate_text(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    return message.strip()
# 调用openai 画图示例
def generate_image(prompt):
    response = openai.Image.create(
        prompt = prompt,
        n=1,
        size="512x512"
    )
    image_url = response['data'][0]['url']
    return image_url
# 调用openai 问答示例
def chat(prompt):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content":prompt}
    ]
)
    answer = response.choices[0].message.content
    return answer
# 调用openai 改正错词输出正确句子
def correct():
    prompt="改正错词输出正确句子:\n\n我在京东电商平台买了苹果耳几和华为体脂称"  #建议prompt: 改正错词输出正确句子:\n\n input_sentence
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content":prompt}
    ]
)
    answer = response.choices[0].message.content
    return answer
# 调用openai 识别关键词
def keyword():
    prompt="对下面内容识别2个关键词，每个词字数不超过3个字:\n\n齐选汽车挂件车内挂饰车载后视镜吊坠高档实心黄铜玉石出入平安保男女 红流苏-玉髓平安扣"  #建议prompt: 对下面内容识别n个关键词，每个词字数不超过m个字:\n\n input data
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content":prompt}
    ]
)
    answer = response.choices[0].message.content
    return answer
# 抽取文本向量 (Embedding)
def embedding():
    content = '苹果手机'
    response = openai.Embedding.create(
    model="text-embedding-ada-002",
    input=content
)
    answer = response.data[0].embedding
    return answer
def api_test():
    conn = mysql_db_conn(dbname='cg')
    cur = conn.cursor()
    sql = 'select id,name,inst_name from paln_list_people  where  is_ava=1 and is_ids=0 order by  id asc limit 2 '
    cur.execute(sql)
    data = cur.fetchall()
    for item in data:
        in_id, name, inst_name = item

    # 测试chat
        prompt = """
        我给例子的数据：
        11	华卫琦	万华化学集团股份有限公司
        15	郭朝晖	中国钢研科技集团有限公司
        18	严永刚	四川国纳科技有限公司
        要生产例子的数据：
        [
          {
            "id": 11,
            "title": "万华化学集团股份有限公司",
            "title_en": "Wanhua Chemical Group Co., Ltd.",
            "abbr": "万华化学",
            "university": "浙江大学",
            "work": "2001年1月加入万华，历任化工过程研究所所长、发展规划部部长、技术研究部部长、中央研究院院长、公司技术总监，现任万华化学集团股份有限公司常务副总裁兼万华中央研究院院长、国家聚氨酯工程技术研究中心主任。",
            "edu": "浙江大学化工系化学工程专业本科毕业，曾留学日本，获得化工专业博士学位，MBA。",
            "source": "https://www.lixinger.com/equity/company/detail/sh/600309/600309/senior-executive/resume"
          },
          {
            "id": 15,
            "title": "中国钢研科技集团有限公司",
            "title_en": "China Iron & Steel Research Institute Group",
            "abbr": "中国钢研",
            "university": "浙江大学",
            "work": "曾任宝钢（宝武）中央研究院首席研究员，现任上海优也信息科技有限公司首席科学家，清华大学特聘研究员。",
            "edu": "1990年本科毕业于浙江大学数学系，后在化工系、工控所获得化工和自动化的硕士、博士学位。",
            "source": "https://www.sohu.com/a/118795965_529972"
          },
          {
            "id": 18,
            "title": "四川国纳科技有限公司",
            "title_en": "Sichuan Guona Technology Co., Ltd.",
            "abbr": "国纳科技",
            "university": "不详",
            "work": "现任四川国纳科技有限公司总经理兼总工程师。",
            "edu": "我国生物材料领域唯一获得国内外双博士学位的科研工作者。",
            "source": "https://baike.baidu.com/item/%E5%9B%9B%E5%B7%9D%E5%9B%BD%E7%BA%B3%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/627761"
          }
        ]

        我要生产的数据
        {in_id} ,{name}, {inst_name}
        """
        response = chat(prompt)
        print(response)
        # updata_sql = f"""update paln_list_people set ai_json=%s where id=%s"""
        # cur.execute(updata_sql,(response,in_id))
        # conn.commit()





if __name__ == '__main__':
    api_test()
from openai import OpenAI
from until.sql_tools import mysql_db_conn, getStrAsMD5



client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="YOUR API KEY",
    base_url="https://api.chatanywhere.tech/v1"
)
client.api_key = "sk-m8cwIrFCGiKti8z4ZyihlXkL5ki2HyjhKtU3Wft0b5XiuNqQ" # 泽磊

client.proxy = "http://192.168.5.21:41091"



# 非流式响应
def gpt_35_api(messages: list):
    """为提供的对话消息创建新的回答

    Args:
        messages (list): 完整的对话消息
    """
    completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    return completion.choices[0].message.content

def gpt_35_api_stream(messages: list):
    """为提供的对话消息创建新的回答 (流式传输)

    Args:
        messages (list): 完整的对话消息
    """
    #gpt-3.5-turbo  200次上限
    stream = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")





if __name__ == '__main__':
    conn = mysql_db_conn(dbname='cg')
    cur = conn.cursor()
    sql = 'select id,name,inst_name from paln_list_people  where  is_ava=1 and is_ids=0 and id>664 order by  id asc '
    cur.execute(sql)
    data = cur.fetchall()
    for item in data:
        in_id, name, inst_name = item
        tt1="""
                "id": 1,
                "title": "万华化学集团股份有限公司",
                "int_name": "Wanhua Chemical Group Co., Ltd.",
                "abbr": "万华化学",
                "university": "浙江大学
                "work": "2001年1月加入万华参加工作，现任本公司副总裁，兼任技术总监国家聚氨酯工程技术研究中心常务副主任"
                "edu":"浙江大学化学系化学工程专业本科毕业、硕博连读研究生美国俄亥俄州莱特州立大学MBA"
                "source":"https://www.aminer.cn/profile/weiqi-hua/53f46225dabfaec09f22eca7"

                
                """
        p=f"""
        
                现在根据我给的专家姓名和工作单位，进行全网搜索，返回必须结果是json格式，返回的键和键值要求，title：最新的工作单位、title_en:最新的工作单位英文名称、abbr：单位的简称、university：专家毕业的最新大学、，work：工作经历 、edu：教育经历、source：上面键的信息来源地址

            举个例子入
            我给的数据：
            id:1 ,name:华卫琦, inst_name:万华化学集团股份有限公司
            你要返回的结果：
            [
              {tt1}
            ]
                现在你要给我处理的数据：
                id:{in_id}, name:{name}, inst_name:{inst_name}
                """
        messages = [{'role': 'user','content':p},]
        # 非流式调用
        # gpt_35_api(messages)
        # 流式调用
        res=gpt_35_api(messages)
        print(res)
        updata_sql = f"""update paln_list_people set ai_json=%s where id=%s"""
        cur.execute(updata_sql,(res,in_id))
        conn.commit()
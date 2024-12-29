from openai import OpenAI




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
    print(completion.choices[0].message.content)

def gpt_35_api_stream(messages: list):
    """为提供的对话消息创建新的回答 (流式传输)

    Args:
        messages (list): 完整的对话消息
    """
    stream = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")





if __name__ == '__main__':

    p="""
    
    现在根据我给的专家姓名和工作单位，进行全网搜索，返回必须结果是json格式，返回的键和键值要求，title：最新的工作单位、title_en:最新的工作单位英文名称、abbr：单位的简称、university：专家毕业的最新大学
举个例子入
我给的数据：
1 华卫琦 万华化学集团股份有限公司
你要返回的结果：
[
  {
    "id": 1,
    "title": "万华化学集团股份有限公司",
    "int_name": "Wanhua Chemical Group Co., Ltd.",
    "abbr": "万华化学",
    "university": "浙江大学"
  }
]
2 姚建军 西安智源电气有限公司
    
    
    """
    messages = [{'role': 'user','content':p},]
    # 非流式调用
    # gpt_35_api(messages)
    # 流式调用
    gpt_35_api_stream(messages)
import json

import requests


# 详情页面
# https://www.aminer.cn/profile/neal-stuart-young-neal-s-young/542ec5bbdabfae498ae3ae6b

# 论文      post
# https://apiv2.aminer.cn/n
#
# a = [{"action": "person.SearchPersonPaper", "parameters": {"person_id": "542ec5bbdabfae498ae3ae6b",
#                                                            "search_param": {"needDetails": False, "page": 1, "size": 10,
#                                                                             "sort": [
#                                                                                 {"field": "year", "asc": False}]}}}]

url = 'Z:/html/aminer_html/0/0/28.html'

# resp = requests.post(url, data=json.dumps(a),timeout=20)
#
# if resp.status_code ==200:
#
#     data = json.loads(resp.text)
#     # print(data)
#     hitList=data['data'][0]['data']['hitList']
#
#     for item in hitList:
#         print(item)
#
#
# # data1=dict(data)
# print(data['data'][0].get)
# print(data)
# # data=dict(response.text)
# # hit_list = data.get('data', {}).get('hitList', [])
# # print(hit.list)


with open('Z:/html/aminer_html/0/0/28.html', 'r', encoding='utf-8')as f:
    data = json.load(f)
    print(data)
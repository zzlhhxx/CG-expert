import requests
import json
# url='https://www.aminer.cn/profile/neal-stuart-young-neal-s-young/66828bbb43ef2f4939baa131'
# response=requests.get(url)
# print(response.text)

# url='https://searchtest.aminer.cn/aminer-search/search/patent'
#
# b = {"filters": [
#     {"boolOperator": 3, "field": "inventor.person_id", "type": "term", "value": "542ec5bbdabfae498ae3ae6b"}],
#     "sort": [{"field": "pub_date", "asc": False}], "needDetails": True, "query": "", "page": 0, "size": 20}
# response=requests.post(url,data=json.dumps(b))
# print(response.text)


a='P. R. Newman'

print(a.replace('.',''))

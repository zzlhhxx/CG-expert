# 论文
# https://apiv2.aminer.cn/n
a = [{"action": "person.SearchPersonPaper", "parameters": {"person_id": "5631e77645cedb3399f52483",
                                                           "search_param": {"needDetails": False, "page": 0, "size": 10,
                                                                            "sort": [
                                                                                {"field": "year", "asc": False}]}}}]


# 详情页面
# https://www.aminer.cn/profile/neal-stuart-young-neal-s-young/66828bbb43ef2f4939baa131



# 专利
# https://searchtest.aminer.cn/aminer-search/search/patent

b = {"filters": [
    {"boolOperator": 3, "field": "inventor.person_id", "type": "term", "value": "542ec5bbdabfae498ae3ae6b"}],
    "sort": [{"field": "pub_date", "asc": False}], "needDetails": True, "query": "", "page": 0, "size": 20}
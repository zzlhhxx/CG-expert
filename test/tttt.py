import requests

# headers = {
#     'Accept': 'application/json, text/plain, */*',
#     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
#     'Connection': 'keep-alive',
#     'DNT': '1',
#     'Origin': 'https://openalex.org',
#     'Referer': 'https://openalex.org/',
#     'Sec-Fetch-Dest': 'empty',
#     'Sec-Fetch-Mode': 'cors',
#     'Sec-Fetch-Site': 'same-site',
#     'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
# }

response = requests.get(
    'https://api.openalex.org/authors?page=1&filter=default.search:Jinsong Leng&sort=relevance_score:desc&per_page=10&apc_sum=false&cited_by_count_sum=false',

)

print(response.text)
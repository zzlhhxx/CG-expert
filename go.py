import requests

proxy_url = "http://192.168.0.101:41091"
proxies = {
    "http": proxy_url,
    "https": proxy_url
}

API_BASE_URL = "https://en.wikipedia.org/w/api.php"
page_title = "John Robertson (physicist)"

params = {
    "action": "query",
    "format": "json",
    "titles": page_title,
    "prop": "extracts",
    "exchars": 100000,  # 调整为100000字符
    "explaintext": True,
    "redirects": True
}

response = requests.get(API_BASE_URL, params=params, proxies=proxies)
data = response.json()
print(data)
page_info = next(iter(data["query"]["pages"].values()))
print(data)
if "extract" in page_info:
    extract = page_info["extract"]
    print(f"获取到的内容长度: {len(extract)} 字符")
    print(extract)
else:
    print(f"未能获取到 {page_title} 的简介内容。")

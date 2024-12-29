import requests
from lxml import etree
from fake_useragent import UserAgent
# 要爬取的维基百科页面的URL
url = "https://en.wikipedia.org/wiki/John_Robertson_(physicist)"
headers={
    "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
}
# 发送GET请求获取页面内容
response = requests.get(url,headers=headers)
print(response.text)
# # 使用lxml的etree解析页面内容
# html = etree.HTML(response.text)
#
# # 使用xpath提取页面中的信息
#
# # 例如，获取页面标题
# page_title = html.xpath('//title/text()')[0]
# print("页面标题:", page_title)
#
# # 获取所有段落内容
# paragraphs = html.xpath('//p/text()')
# for paragraph in paragraphs:
#     print(paragraph)
#
# # 获取所有链接
# links = html.xpath('//a/@href')
# for link in links:
#     print(link)
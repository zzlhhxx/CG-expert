import requests
from lxml import etree
import re


url='https://baike.baidu.com/item/%E7%8E%8B%E4%B8%AD%E6%9E%97/63571#1'
rep=requests.get(url)
rep.encoding='utf-8'

if rep.status_code==200:
    print('返回成功')
    tree=etree.HTML(rep.text)
    d=tree.xpath('//div[@class="lemmaSummary_xoHAz J-summary"]//text()')
    text=''.join(d).strip()
    text = re.sub(r'\[.*?\]', '', text)
    print(text)
    with open('test.txt','w',encoding='utf-8') as f:
        wr=f.write(text)
        f.close()
        if wr:
            print('写入成功')
        else:
            print('写入失败')
else:
    print('返回失败')


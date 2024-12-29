import time

from until.sql_tools import mysql_db_conn, getStrAsMD5
from until.config import he

from lxml import etree
from urllib.parse import unquote
import random
import requests
import json
import os
import pymongo

def mongo_client(table:str):
    client = pymongo.MongoClient("192.168.5.21", 27017)
    db = client[table]
    return db


db=mongo_client('cg')
c=db['author_table']
data=c.find()
for item in data:
    _id=item['_id']
    au_organs=item['au_organs']
    au_edu=item['au_edu']
    id=item['_id']
    au_last_organs=item['au_last_organs']

    # if not au_edu:
    #     au_edu_list=[]
    # else:
    #     au_edu_list=au_edu.split("<br>")


    if not au_last_organs:
        au_last_organs_list=[]
    else:
        au_last_organs_list=au_last_organs.split(",")
        print(au_last_organs_list)



    c.update_one({"_id": _id}, {'$set': {'au_last_organs': au_last_organs_list}})



    # if "<br>" in au_edu:   #判断是否有br
    #     print(au_edu)
    #
    #     if not au_organs:  # 判断是否有机构
    #         continue
    #     # print(au_organs)
    #     if not au_edu:       # 判断是否有教育
    #         continue
    #
    #
    #     au_edu_1=au_edu.split("<br>")  #根据br分割
    #     print(au_edu_1)
    #     for au in au_edu_1:             #遍历分割后的列表
    #         au_edu_ld=au.split(',')     #对列表中的字符串分割
    #         print(au_edu_ld)
    #     # print(au_edu_1)
    #     print(id)
    #     print('**************')
    #     print('\n')

        # print(len(au_edu_1))

        # print(au_organs.split("<br>"))
        # au_organs_list=au_organs.split("<br>")
    #     # print(len(au_organs_list))
    # else:
    #     print("没有br")
    #     au_edu_len=len(au_edu)
    #     print('字符串长度:'+au_edu_len)
    #     au_edu_d=au_edu.split(',')
    #     print(au_edu_d)
    #     print(id)
    #     print('\n')
    #     continue







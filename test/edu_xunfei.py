import time

from until.sql_tools import mongo_client,mysql_db_conn
from until.time_tool import saveTime
import re
import pycountry
import json
from urllib.parse import unquote
from lxml import etree
def get_country_code(country_name):
    country = pycountry.countries.get(name=country_name)
    if country:
        return country.alpha_2  # 返回国家的 ISO 3166-1 alpha-2 两位缩写
    return None

def country_code_to_name(country_code):
    try:
        country = pycountry.countries.get(alpha_3=country_code)  # 使用 alpha-3 (3字母缩写)
        return country.name if country else "Unknown"
    except Exception as e:
        return f"Error: {e}"

conn=mysql_db_conn(dbname='cg')
cur=conn.cursor()
mongo_db = mongo_client('cg')

def author_oepnalex(select_id,conn):
    select_ = 'select id,source_id from zjwl_author where is_paln =1 and is_expert=0 and is_el=0 and oa_id=%s'
    cur.execute(select_, (select_id,))
    openalex_data = cur.fetchone()
    h_index = ''
    i10_index = ''
    au_organs = []
    au_last_organs = []
    display_name_alternatives = []
    if openalex_data:
        openalex_id, detail_json = openalex_data
        if detail_json:
            openalex_json_data = json.loads(detail_json)
            display_name_alternatives = openalex_json_data['display_name_alternatives']
            h_index = openalex_json_data['summary_stats']['h_index']
            i10_index = openalex_json_data['summary_stats']['i10_index']
            affiliations = openalex_json_data['affiliations']
            last_known_institutions = openalex_json_data['last_known_institutions']

            for a in affiliations:
                name = a['institution']['display_name']
                country = a['institution']['country_code']
                type = a['institution']['type']
                years = a['years']
                if len(years) > 1:
                    years_str = f"{years[-1]}-{years[0]}"
                else:
                    years_str = years[0]
                au_organs.append({
                    "name": name,
                    "country": country,
                    "type": type,
                    "years": years_str,
                    "position": '',
                })
            for last in last_known_institutions:
                name = last['display_name']
                au_last_organs.append({
                    "name": last['display_name'],
                    "position": ''
                })

    return  display_name_alternatives,h_index,i10_index,au_organs,au_last_organs


select_ = 'select id,name,inst_name,year,source,list_json,html_path,xm_ids,oa_path,oa_id,aminer_id,zl_ids from paln_list_people where is_ids=1 order by id asc  '
# select_ = 'select id,name,inst_name,year,source,list_json,html_path,xm_ids,oa_path,oa_id,aminer_id,zl_ids from paln_list_people where id=20000033 '
cur.execute(select_)
data = cur.fetchall()
print(len(data))
for item in data:
    ids,name,inst_name,year,source,list_json,html_path,xm_ids,oa_path,oa_id,aminer_id ,zl_ids = item
    au_id = ids
    address = 'Z:/' + html_path
    # print(address)
    data = open(address, 'r', encoding='utf-8').read()
    # # tree = etree.HTML(data)
    tree = etree.HTML(data)
    # print(open(address, 'r', encoding='utf-8').read())
    json_data = re.findall(r'window.g_initialProps = (.*);', data, )
    try:
        if len(json_data):
            dict_data=json.loads(json_data[0])
            profile = dict_data['profile']['profile']
            #
            # au_name = name
            # au_aliases=[]
            # au_avatar =profile['avatar'] if profile.get("avatar") else ''
            #
            # au_dirth_date = ''
            # au_country = 'CN'
            # if profile['profile'].get("bio_zh"):
            #     au_resume=profile['profile']['bio_zh'].replace("<br>", '\n').replace('\u3000', ' ').strip() if profile['profile'].get(
            #     'bio_zh') else ''
            # else:
            #     au_resume =profile['profile']['bio'].replace("<br>", '\n').replace('\u3000', ' ').strip() if profile['profile'].get('bio') else ''
            # au_level = ''
            # au_fields = ''
            # au_phone  =profile['profile']['phone'].strip().split(";") if profile['profile'].get("phone") else []
            # au_mail =profile['profile']['email'].strip() if profile['profile'].get("email") else []
            # au_edu_list=[]
            # au_topics = profile['tags'] if profile.get("tags") else []
            #
            # affiliation = profile['affiliation'] if profile.get("affiliation") else []
            # affiliation_zh = profile['affiliation_zh'] if profile.get("affiliation_zh") else []
            # position = profile['position'] if profile.get("position") else []
            # position_zh = profile['position_zh'] if profile.get("position_zh") else []
            # if affiliation_zh:
            #     affiliation_zl_list = affiliation_zh.split(';')
            #
            # au_awards = ''
            # au_conference = []
            # #去查询oa的数据
            # au_count_total={
            #     'cited_count_total':'', #等待论文入库时更新
            #     'pub_count':0,
            # }
            au_edu=''
            if profile['profile'].get("edu"):
                au_edu=profile['profile'].get("edu")

                # print(au_edu)
            if not au_edu:
                if profile['profile'].get("edu_zh"):
                    au_edu = profile['profile'].get("edu_zh")
            if au_edu:
                inser_='insert into edu_xunfei(id,edu,aminer_id) values(%s,%s,%s)'
                cur.execute(inser_,(ids,au_edu,aminer_id))
                conn.commit()
                # au_edu_split_list=au_edu.split("<br>")
                # for au_edu_item in au_edu_split_list:
                #     au_edu_list.append({
                #         "name":au_edu_item, #毕业院校名称
                #         "college ":'', #学院（系）
                #         "country":'',#毕业院校所在国家
                #         "degree":'',#当前院校毕业所获得的学位
                #     })

    except Exception as e :
        print("出错",e)
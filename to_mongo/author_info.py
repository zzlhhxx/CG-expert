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
# c = mongo_db['test_author']
c = mongo_db['zjwl_author']
gender_dict={
    "female":2,
    "male":1,
    "unknown":0,
}
def author_oepnalex(select_id,conn):
    select_ = 'select id,oa_path from paln_list_people where is_ids =1 and is_oa_download=1  and oa_id=%s'
    cur.execute(select_, (select_id,))
    openalex_data = cur.fetchone()
    h_index = 0
    i10_index = 0
    au_organs = []
    works_count = 0
    cited_by_count=0
    au_last_organs = []
    display_name_alternatives = []
    if openalex_data:
        openalex_id, detail_json = openalex_data

        detail_json="z:/"+detail_json
        print(detail_json)
        with open(detail_json,"r",encoding='utf-8') as f:
            # json_data=json.loads(f.read())
            json_data = f.read()
            # print(json_data)

            if json_data:
                openalex_json_data = json.loads(json_data)
                print("**********")
                results=openalex_json_data['results']
                for result in results:
                    if oa_url==result['id']:
                        print(oa_url,result['id'])
                        print("*******")
                        display_name_alternatives=result['display_name_alternatives']if result.get("display_name_alternatives") else []

                        works_count=result['works_count']
                        cited_by_count=result['cited_by_count']
                        h_index=result['summary_stats']['h_index']
                        i10_index=result['summary_stats']['i10_index']
                        affiliations = result['affiliations']

                        last_known_institutions = result['last_known_institutions']
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
                        # for last in last_known_institutions:
                        #     name = last['display_name']
                        #     au_last_organs.append({
                        #         "name": last['display_name'],
                        #         "position": ''
                        #     })

    return  display_name_alternatives,h_index,i10_index,au_organs,au_last_organs,works_count,cited_by_count

def hy(ids):
    select_ = f'select {ids},hy_ids_done from nstl_hy where id=%s'
    cur.execute(select_,(ids,))
    data_hy = cur.fetchone()
    hy_list = []
    if data_hy:
        in_id, hy_ids_done = data_hy
        if hy_ids_done:
            for hy_id in hy_ids_done.split(',,'):
                hy_list.append(hy_id)
        return hy_list




select_ = 'select id,name,inst_name,year,source,list_json,html_path,xm_ids,oa_path,oa_id,aminer_id,zl_ids,plan_type from paln_list_people where is_ids=1   order by id asc  '
# select_ = 'select id,name,inst_name,year,source,list_json,html_path,xm_ids,oa_path,oa_id,aminer_id,zl_ids,plan_type from paln_list_people where id=20000017 '
cur.execute(select_)
data = cur.fetchall()
print(len(data))
for item in data:
    ids,name,inst_name,year,source,list_json,html_path,xm_ids,oa_path,oa_id,aminer_id,zl_ids,plan_type = item
    if oa_id:
        oa_url="https://openalex.org/"+oa_id

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
            au_name = name
            au_aliases=[]
            au_avatar =profile['avatar'] if profile.get("avatar") else ''
            au_gender = gender_dict[profile['profile']['gender']] if profile['profile'].get("gender") else 0
            au_dirth_date = ''
            au_country = 'CN'
            if profile['profile'].get("bio_zh"):
                au_resume=profile['profile']['bio_zh'].replace("<br>", '\n').replace('\u3000', ' ').strip() if profile['profile'].get(
                'bio_zh') else ''
            else:
                au_resume =profile['profile']['bio'].replace("<br>", '\n').replace('\u3000', ' ').strip() if profile['profile'].get('bio') else ''
            au_level = ''
            au_fields = ''
            au_phone  =profile['profile']['phone'].strip().split(";") if profile['profile'].get("phone") else []
            au_phone_ = []
            if len(au_phone):
                for phone in au_phone:
                    phone_zero = phone.replace("(0)", "").replace("(", "").replace(")", "").replace(" ", "-").replace(
                        ".", "-").replace("--", "-").replace("---", "-").replace("--", "-").replace("（",'').replace("）",'-').replace("－",'-')
                    au_phone_.append(phone_zero)



            au_mail =profile['profile']['email'].strip() if profile['profile'].get("email") else []
            au_edu_list=[]
            au_topics = profile['tags'] if profile.get("tags") else []
            position = ''
            org_name = ''

            org_ = profile['profile']
            if org_.get("position"):
                position = org_['position']
            else:
                if org_.get("position_zh"):
                    position = org_['position_zh']
            if org_.get("affiliation"):
                org_name = org_['affiliation'].split(";")[0]
            else:
                if org_.get("affiliation_zh"):
                    org_name = org_['affiliation_zh'].split(";")[0]

            au_awards=[]
            if "拟入选对象名单" in plan_type or "拟入选名单" in plan_type or "入选名单" in plan_type:
                au_awards=[year+"年入选"+plan_type.replace("拟入选对象名单", "").replace("拟入选名单", "").replace("入选名单", "")]

            au_conference = []

            au_articles=[]
            au_patent=[]
            au_project=[]

            print('1')
            au_aliases, h_index, i10_index, au_organs, au_last_organs,works_count,cited_by_count = author_oepnalex(oa_id, conn)

            au_metrics={
                'h_index':h_index,
                'i10_index':i10_index,
            }
            au_count_total={
                'cited_count_total':cited_by_count, #等待论文入库时更新
                'pub_count':works_count,
            }
            if org_name:
                au_last_organs = [{
                    "name": org_name,
                    "position": position,
                }]
            else:
                au_last_organs=au_last_organs
            print(au_last_organs)
            if len(au_last_organs):
                au_last_organs=au_last_organs[0]
                au_last_organs=[au_last_organs]

            au_source=[]
            if profile['profile'].get("homepage"):
                au_source_url = profile['profile']['homepage']
                au_source_url = unquote(au_source_url, 'utf-8').replace("&amp;", "&")
                au_source.append(au_source_url)

            au_source.append(f'https://www.aminer.cn/profile/{aminer_id}')
            au_create_date=saveTime()
            au_update_date=saveTime()
            hy_ids=hy(ids)
            # if lw_ids:
            #     lw_ids=lw_ids.split(",,")
            # else:
            #     lw_ids=[]
            if zl_ids:
                zl_ids=zl_ids.split(",,")
            else:
                zl_ids=[]
            if xm_ids:
                xm_ids=xm_ids.split(",,")
            else:
                xm_ids=[]




            author = {
                        "_id":au_id,
                        "au_name":au_name,
                        "au_aliases":au_aliases,
                        "au_avatar":au_avatar,
                        "au_gender":au_gender,
                        "au_dirth_date":au_dirth_date,
                        "au_country":au_country,
                        "au_resume":au_resume,
                        "au_level":au_level,
                        "au_fields":au_fields,
                        "au_phone":au_phone_,
                        "au_mail":au_mail,
                        "au_edu":au_edu_list,
                        "au_topics":au_topics,
                        "au_last_organs":au_last_organs,
                        "au_organs":au_organs,
                        "au_awards":au_awards,
                        "au_conference":au_conference,
                        "au_count_total":au_count_total,
                        "au_articles":au_articles,
                        "au_patent":au_patent,
                        "au_project":au_project,
                        "au_metrics":au_metrics,
                        "au_source":au_source,
                        "au_create_date":au_create_date,
                        "au_update_date":au_update_date,

                        "_zl_ids":zl_ids,
                        "_lw_ids":[],
                        "_xm_ids":xm_ids,
                        "hy_ids":hy_ids,
                        "is_synced": 0  ,
                        "au_topics_new":""  ,
                        "is_plan":1
                    }
            print("*****11*****")
            if not c.find_one({"_id":au_id}):
                c.insert_one(author)
            # update_='update paln_list_people set is_to_mongo=1 where id =%s'
            # cur.execute(update_,(ids,))
            # conn.commit()


    except Exception as e :
        print(e,ids)
        print(f"第几行{e.__traceback__.tb_lineno},")
        continue
        # au_edu_split_list=au_edu.split("<br>")

    # # if lw_ids:
    # #     lw_ids=lw_ids.split(",,")
    # # else:
    # #     lw_ids=[]
    # if zl_ids:
    #     zl_ids=zl_ids.split(",,")
    # else:
    #     zl_ids=[]
    # if xm_ids:
    #     xm_ids=xm_ids.split(",,")
    # else:
    #     xm_ids=[]
    # # print(in_id,source_id,aminer_id)
    # address = 'Z:/' + html_path
    # # print(address)
    # data = open(address, 'r', encoding='utf-8').read()
    # # tree = etree.HTML(data)
    # # print(open(address, 'r', encoding='utf-8').read())
    # json_data = re.findall(r'window.g_initialProps = (.*);', data, )
    # if cntry ==None:
    #     cntry=''
    # au_country=get_country_code(country_code_to_name(cntry))
    # if len(json_data):
    #     json_data = json_data[0]
    #     try:
    #         dict_data = json.loads(json_data)
    #         profile = dict_data['profile']['profile']
    #         au_id =in_id
    #         au_name = profile['name']
    #         au_aliases = []
    #         au_avatar =profile['avatar'] if profile.get("avatar") else ''
    #         if not profile.get("profile"):
    #             continue
    #         au_gender =gender_dict[profile['profile']['gender']] if profile['profile'].get("gender") else 0
    #         au_dirth_date  = '' #生日，需要去完善
    #         au_country =au_country
    #         au_source=[]
    #         if profile['profile'].get("homepage"):
    #             au_source_url = profile['profile']['homepage']
    #             au_source_url = unquote(au_source_url, 'utf-8').replace("&amp;", "&")
    #             au_source.append(au_source_url)
    #
    #         au_source.append(f'https://www.aminer.cn/profile/{aminer_id}')
    #
    #         if profile['profile'].get("bio_zh"):
    #             au_resume=profile['profile']['bio_zh'].replace("<br>", '\n').replace('\u3000', ' ').strip() if profile['profile'].get(
    #                 'bio_zh') else ''
    #         else:
    #             au_resume =profile['profile']['bio'].replace("<br>", '\n').replace('\u3000', ' ').strip() if profile['profile'].get(
    #                     'bio') else ''
    #         au_level =''  #string
    #         au_fields =''
    #         au_phone  =profile['profile']['phone'].strip().split(";") if profile['profile'].get("phone") else []
    #         au_mail =profile['profile']['email'].strip() if profile['profile'].get("email") else []
    #         au_edu_list=[]
    #         if profile['profile'].get("edu"):
    #             au_edu=profile['profile']['edu']
    #             au_edu_split_list=au_edu.split("<br>")
    #             for au_edu_item in au_edu_split_list:
    #                 au_edu_list.append({
    #                     "name":au_edu_item, #毕业院校名称
    #                     "college ":'', #学院（系）
    #                     "country":'',#毕业院校所在国家
    #                     "degree":'',#当前院校毕业所获得的学位
    #                 })
    #         au_topics=profile['tags'] if profile.get("tags") else []
    #
    #         #对比openalex
    #         au_aliases,h_index, i10_index, au_organs, au_last_organs=author_oepnalex(in_id,conn)
    #         #提取wiki百科
    #
    #         au_awards=''
    #         au_conference=[]#会议
    #         # lw_ids=lw_ids
    #         au_count_total={
    #             'cited_count_total':'', #等待论文入库时更新
    #             'pub_count':0,
    #         }
    #         au_articles=[]
    #         au_patent=[]
    #         au_project=[]
    #         au_metrics={
    #             'h_index':h_index,
    #             'i10_index':i10_index,
    #         }
    #
    #
    #         au_create_date=saveTime()
    #         au_update_date=saveTime()
    #
    #         author={
    #             "_id":au_id,
    #             "au_name":au_name,
    #             "au_aliases":au_aliases,
    #             "au_avatar":au_avatar,
    #             "au_gender":au_gender,
    #             "au_dirth_date":au_dirth_date,
    #             "au_country":au_country,
    #             "au_resume":au_resume,
    #             "au_level":au_level,
    #             "au_fields":au_fields,
    #             "au_phone":au_phone,
    #             "au_mail":au_mail,
    #             "au_edu":au_edu_list,
    #             "au_topics":au_topics,
    #             "au_last_organs":au_last_organs,
    #             "au_organs":au_organs,
    #             "au_awards":au_awards,
    #             "au_conference":au_conference,
    #             "au_count_total":au_count_total,
    #             "au_articles":au_articles,
    #             "au_patent":au_patent,
    #             "au_project":au_project,
    #             "au_metrics":au_metrics,
    #             "au_source":au_source,
    #             "au_create_date":au_create_date,
    #             "au_update_date":au_update_date,
    #
    #             "_zl_ids":zl_ids,
    #             "_lw_ids":[],
    #             "_xm_ids":xm_ids,
    #         }
    #
    #         # if not c.find_one({"_id":au_id}):
    #         #     print('入库一条数据',in_id)
    #         #     c.insert_one(author)
    #             # update_='update aminer set is_to_mongo=1 where id =%s'
    #             # cur.execute(update_,(in_id,))
    #             # conn.commit()
    #     except Exception as e :
    #         print(e,in_id)
    #         continue
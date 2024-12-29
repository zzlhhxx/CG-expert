import re
import time

from tools.sql_tools import mysql_db_conn, getStrAsMD5, freeRepeat, mongo_client
from tools.config import he

from lxml import etree
from urllib.parse import unquote
import random
import requests
import json
import os

path_html = r'E:/html/aminer_html/'

conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
mongo_db = mongo_client('cg')
c = mongo_db['author_table']
gender_dict={
    "female":2,
    "male":1,
    "unknown":0,
}

def parse_author_info():
    sql = 'select id,source_id,aminer_id,html_path from aminer where is_ava=1 and is_download_html =1 and profilePubsTotal is not  null order by  id asc  '
    # sql = 'select id,source_id,aminer_id,html_path from aminer where source_id =1063 and is_ava=1  '
    cur.execute(sql)
    data = cur.fetchall()
    print(len(data))
#
    for item in data:
        in_id, source_id, aminer_id, html_path = item
        # print(in_id,source_id,aminer_id)
        address = 'D:/' + html_path
        # print(address)
        data = open(address, 'r', encoding='utf-8').read()
        # tree = etree.HTML(data)
        # print(open(address, 'r', encoding='utf-8').read())
        json_data = re.findall(r'window.g_initialProps = (.*);', data, )
        if len(json_data):
            json_data = json_data[0]

            dict_data = json.loads(json_data)
            profile = dict_data['profile']['profile']
            battles_dict = {
                "_id": source_id,
                "au_name": profile['name'],
                "au_name_zh": profile['name_zh'] if profile.get("name_zh") else '',
                "au_avatar_url": profile['avatar'] if profile.get("avatar") else '',
                "au_aliases": '',
                # female 女  male  男 unknown 未知
                "au_gender": gender_dict[profile['profile']['gender']] if profile['profile'].get("gender") else '',
                "au_dirth_date": profile['au_dirth_date'] if profile.get("au_dirth_date") else '',
                "au_country": '',
                "lang": profile['profile']['lang'] if profile['profile'].get("lang") else '',
                "au_resume": profile['profile']['bio'].replace("<br>", '\n').strip() if profile['profile'].get(
                    'bio') else '',
                "au_resume_cn": profile['profile']['bio_zh'].replace("<br>", '\n').strip() if profile['profile'].get(
                    'bio_zh') else '',
                "au_phone": profile['profile']['phone'].strip() if profile['profile'].get("phone") else '',
                "au_mail": profile['profile']['email'].strip() if profile['profile'].get("email") else '',
                "au_edu": profile['profile']['edu'] if profile['profile'].get("edu") else '',
                "au_topics": profile['tags'] if profile.get("tags") else [],
                "au_last_organs": profile['profile']['affiliation'] if profile['profile'].get("affiliation") else '',
                "au_last_organs_zh": profile['profile']['affiliation_zh'] if profile['profile'].get("affiliation_zh") else '',
                "au_organs": profile['profile']['edu'] if profile['profile'].get("edu") else '',
                "au_organs_zh": profile['profile']['edu_zh'] if profile['profile'].get("edu_zh") else '',

            }
            c.insert_one(battles_dict)




def update_lw_total():
    sql = 'select id,source_id,aminer_id,html_path from aminer where is_ava=1 and is_download_html =1  order by  id asc '
    # sql = 'select id,source_id,aminer_id,html_path from aminer where is_ava=1 and id=3111 '
    cur.execute(sql)
    data = cur.fetchall()

    for item in data:
        in_id, source_id, aminer_id, html_path = item
        # print(in_id,source_id,aminer_id)
        address = 'E:/' + html_path
        # print(address)
        data = open(address, 'r', encoding='utf-8').read()
        # tree = etree.HTML(data)
        # print(open(address, 'r', encoding='utf-8').read())
        json_data = re.findall(r'window.g_initialProps = (.*);', data, )

        if len(json_data):
            json_data = json_data[0]
            dict_data = json.loads(json_data)
            profile = dict_data['profile']['profile']
            profilePubsTotal = dict_data['profile']['profilePubsTotal']
            print(profilePubsTotal)
        else:
            profilePubsTotal = 0
        update_sql = 'update aminer set profilePubsTotal=%s where id =%s'
        cur.execute(update_sql, (profilePubsTotal, in_id))
        conn.commit()



def del_mongo_key():
    c = mongo_db['author_table']
    data = c.find()
    for item in data:
        _id=item['_id']
        print(_id)
        sql = 'select id,source_id,aminer_id,html_path from aminer where source_id=%s and is_ava=1 '
        # sql = 'select id,source_id,aminer_id,html_path from aminer where is_ava=1 and id=3111 '
        cur.execute(sql,(_id,))
        aminer_data = cur.fetchone()
        aminerid, source_id, aminer_id, html_path=aminer_data
        address = 'E:/' + html_path
        # print(address)
        data = open(address, 'r', encoding='utf-8').read()
        # tree = etree.HTML(data)
        # print(open(address, 'r', encoding='utf-8').read())
        json_data = re.findall(r'window.g_initialProps = (.*);', data, )
        if len(json_data):
            json_data = json_data[0]
            dict_data = json.loads(json_data)
            profile = dict_data['profile']['profile']
            au_topics_=profile['tags'] if profile.get("tags") else [],
            c.update_one({"_id": _id}, {'$set': {'au_topics_': au_topics_}})
        # break


del_mongo_key()

# parse_author_info()

# update_lw_total()
a = {'global': {'collapsed': False, 'preventRender': False, 'isCompanyIp': False}, 'profile': {'transitionState': False,
                                                                                               'profile': {
                                                                                                   'avatar': 'https://static.aminer.cn/upload/avatar/1238/1709/1473/5440905edabfae7d84b8285f.jpg',
                                                                                                   'bind': False,
                                                                                                   'id': '5440905edabfae7d84b8285f',
                                                                                                   'indices': {
                                                                                                       'activity': 728.4279,
                                                                                                       'citations': 420204,
                                                                                                       'diversity': 4.0257,
                                                                                                       'gindex': 620,
                                                                                                       'hindex': 282,
                                                                                                       'newStar': 3.3125,
                                                                                                       'pubs': 1706,
                                                                                                       'risingStar': 3.3125,
                                                                                                       'sociability': 8.2406},
                                                                                                   'links': {'gs': {
                                                                                                       'type': 'gs',
                                                                                                       'url': ''},
                                                                                                       'resource': {
                                                                                                           'resource_link': [
                                                                                                               {
                                                                                                                   'id': 'hp',
                                                                                                                   'url': 'https://www.epfl.ch/labs/lpi/graetzel/'},
                                                                                                               {
                                                                                                                   'id': 'dblp',
                                                                                                                   'url': ''}]}},
                                                                                                   'name': 'Michael Graetzel',
                                                                                                   'name_zh': '米夏埃尔·格雷策尔',
                                                                                                   'num_followed': 6,
                                                                                                   'num_upvoted': 0,
                                                                                                   'num_viewed': 1174,
                                                                                                   'profile': {
                                                                                                       'address': '',
                                                                                                       'affiliation': 'Laboratory of Photonics and Interfaces, Institute of Chemical Sciences and Engineering, Swiss Federal Institute of Technology',
                                                                                                       'bio': 'Professor of Physical Chemistry at the Ecole polytechnique fédérale de Lausanne (EPFL) Michael Graetzel, PhD, directs there the Laboratory of Photonics and Interfaces. He pioneered research on energy and electron transfer reactions in mesoscopic systems and their use to generate electricity and fuels from sunlight. He invented mesoscopic injection solar cells, one key embodiment of which is the dye-sensitized solar cell (DSC). DSCs are meanwhile commercially produced at the multi-MW-scale and created a number of new applications in particular as lightweight power supplies for portable electronic devices and in building integrated photovoltaics. They engendered perovskite solar cells (PSCs) which turned into the most exciting break-through in the history of photovoltaics. He received a number of prestigious awards, of which the most recent ones include the RusNANO Prize, the Zewail Prize in Molecular Science, the Global Energy Prize, the Millennium Technology Grand Prize, the Marcel Benoist Prize, the King Faisal International Science Prize, the Einstein World Award of Science and the Balzan Prize. He is a Fellow of several learned societies and holds eleven honorary doctor’s degrees from European and Asian Universities. His over 1500 publications have received some 220’000 citations with an h-factor of 218 (SI-Web of Science) demonstrating the strong impact of his scientific work.',
                                                                                                       'bio_zh': 'Graetzel教授是染料敏化太阳电池的发明人和钙钛矿太阳电池领域的国际知名专家。他领导建立了光子界面实验室，发明了染料敏化太阳电池，发表1000多篇科技论文，出版了两本专著，拥有50余项发明专利，他的工作被引次数超过134000，H因子167，是世界上被引用次数最高的10位化学家之一。 <br><br>\u3000\u3000Graetzel教授的报告深入浅出，他回顾了其从事染料敏化太阳电池的研究历程，并介绍了钙钛矿太阳电池领域的最新研究进展。报告结束后，与会人员与Michael Graetzel进行了深入讨论和交流。<br>2021年11月18日，被纳入2021年新当选中国科学院外籍院士名单并予以公示',
                                                                                                       'edu': 'Dr.rer.nat. in Physical Chemistry, 1971 (summa cum laude), TU Berlin.<br>Diploma degree in Chemistry, 1968 (summa cum laude), Free University of Berlin',
                                                                                                       'edu_zh': '',
                                                                                                       'email': '',
                                                                                                       'fax': '+41 21 693 31 15',
                                                                                                       'gender': 'male',
                                                                                                       'homepage': 'https://www.epfl.ch/labs/lpi/graetzel/',
                                                                                                       'lang': 'english',
                                                                                                       'note': '无教育经历',
                                                                                                       'org_zh': '',
                                                                                                       'phone': '+41 21 693 31 12',
                                                                                                       'position': 'Professor',
                                                                                                       'position_zh': '教授',
                                                                                                       'work': 'Full Professor, Director of the Laboratory of Photonics and Interfaces at EPFL, 1981 – present<br>Head of the Chemistry Department, EPFL 1991-1993, and 1983-1985. 1977 -1981.<br>Associated Professor of Physical Chemistry, EPFL 1977 – 1981 :<br>External Scientific Member, Max Planck Institute for Solid State Research Stuttgart, Germany 2018- present.<br>Guest Professor, NTU Singapore, 2011 -2018<br>Distinguished Invited Professor, National University of Singapore, 2005-2009 Invited Professor, Ecole Polytechnique Supérieure de Paris-Cachan 1998.<br>Invited Professor, University of California at Berkeley. 1974-1976.<br>Senior Staff Scientist, Hahn-Meitner Institute Berlin, Germany, 1971-1972.<br>Lecturer of Photochemistry and Physical Chemistry, Free University of Berlin.1975 -1976.<br>Petroleum Research Foundation Post-Doctoral Fellow University of Notre Dame, USA. 1972-1974 Research Associate, Hahn Meitner Institute Berlin, 1969 – 1972',
                                                                                                       'work_zh': ''},
                                                                                                   'tags': [
                                                                                                       'Carbon Nanotubes',
                                                                                                       'Carbon Nanotube',
                                                                                                       'Band Gap',
                                                                                                       'Solar Cells',
                                                                                                       'Aqueous Solutions',
                                                                                                       'Titanium Dioxide',
                                                                                                       'Energy Transfer',
                                                                                                       'Electron Transfer',
                                                                                                       'Transition Metal',
                                                                                                       'Spray Pyrolysis',
                                                                                                       'Conduction Band',
                                                                                                       'Aqueous Solution',
                                                                                                       'Electric Field',
                                                                                                       'Visible Light',
                                                                                                       'Energy Harvesting',
                                                                                                       'Power Conversion',
                                                                                                       'Metal Oxide Semiconductor',
                                                                                                       'Surface Area',
                                                                                                       'Novel Synthesis',
                                                                                                       'Perovskite Solar Cells'],
                                                                                                   'tags_score': [
                                                                                                       27.860908794543683,
                                                                                                       27.69167440666948,
                                                                                                       27.03539736980877,
                                                                                                       26.84622202459935,
                                                                                                       26.19157668913913,
                                                                                                       25.783532336611334,
                                                                                                       25.69889465844803,
                                                                                                       25.0155870759523,
                                                                                                       24.747021084587285,
                                                                                                       24.646779368559596,
                                                                                                       24.585509638292326,
                                                                                                       24.283797678963005,
                                                                                                       22.678474790454867,
                                                                                                       22.61520801339418,
                                                                                                       22.271813175263713,
                                                                                                       22.064216657959214,
                                                                                                       20.774136728042254,
                                                                                                       15.936578083868348,
                                                                                                       7.458939437646711,
                                                                                                       176]},
                                                                                               'profileID': '5440905edabfae7d84b8285f',
                                                                                               'profilePubsPage': 1,
                                                                                               'profilePubs': [],
                                                                                               'profilePubsTotal': 1696,
                                                                                               'profilePatentsPage': 0,
                                                                                               'profilePatents': None,
                                                                                               'profilePatentsTotal': None,
                                                                                               'profilePatentsEnd': False,
                                                                                               'profileProjectsPage': 1,
                                                                                               'profileProjects': {
                                                                                                   'success': True,
                                                                                                   'msg': '',
                                                                                                   'data': None,
                                                                                                   'log_id': '2pQWyWO2djgAJJEcgU7wF9eu3yU'},
                                                                                               'profileProjectsTotal': 0,
                                                                                               'newInfo': None,
                                                                                               'checkDelPubs': []}}

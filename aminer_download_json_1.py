import time
from until.sql_tools import mysql_db_conn,freeRepeat
from lxml import etree
from urllib.parse import unquote
import random
import requests
import json
import os

path_html = r'D:/cg_expert_data/html/aminer/'

conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
sql = 'select id,hitsTotal,authfull,inst_name,html_path from elsevier_author_career where is_download=1 and is_parse=0  order by id asc limit 1'
# sql = 'select id,hitsTotal,authfull,inst_name,aminer_path from elsevier_author_career where id =2 '
cur.execute(sql)
data = cur.fetchall() #mysql查詢數據

for item in data:
    ids, hitsTotal, authfull, inst_name, aminer_path = item #mysql字段
    aminer_path = 'Y:/' + aminer_path.replace("cg_expert_data/", '')
    print(aminer_path)
    with open(aminer_path, 'r', encoding='utf8') as f:
        json_data = json.load(f)
    data_item = json_data['data']
    print(data_item)
    hitList = data_item['hitList']
    for hit in hitList:
        if not hit:
            continue
        avatar=hit['activity'] if hit.get('activity') else ''
        avatar=hit['avatar'] if hit.get('hit') else ''
        aminer_id = ""
        academicType = ""
        affiliation = ""
        affiliationZh = ""
        bio = ""
        bioZh = ""
        edu = ""
        eduZh = ""
        homepage = ""
        phone = ""
        work = ""
        workZh = ""
        gender = ""
        aminer_id = hit['id'] if hit.get('id') else ''
        if hit.get('contact'):
            contact=hit['contact']
            # academicType=hit['academicType']
            academicType=hit['contact']['academicType'] if hit['contact'].get('academicType') else ''
            address=hit['contact']['address'] if hit['contact'].get('address') else ''
            affiliation=hit['contact']['affiliation'] if hit['contact'].get('affiliation') else ''
            affiliationZh=hit['contact']['affiliationZh'] if hit['contact'].get('affiliationZh') else ''
            bio=hit['contact']['bio'] if hit['contact'].get('bio') else ''
            bioZh=hit['contact']['bioZh'] if hit['contact'].get('bioZh') else ''
            edu=hit['contact']['edu'] if hit['contact'].get('edu') else ''
            eduZh=hit['contact']['eduZh'] if hit['contact'].get('eduZh') else ''
            email=hit['contact']['email'] if hit['contact'].get('email') else ''
            fax=hit['contact']['fax'] if hit['contact'].get('fax') else ''
            homepage=hit['contact']['homepage'] if hit['contact'].get('homepage') else ''
            note=hit['contact']['note'] if hit['contact'].get('note') else ''
            phone=hit['contact']['phone'] if hit['contact'].get('phone') else ''
            position=hit['contact']['position'] if hit['contact'].get('position') else ''
            positionZh=hit['contact']['positionZh'] if hit['contact'].get('positionZh') else ''
            work=hit['contact']['work'] if hit['contact'].get('work') else ''
            workZh=hit['contact']['workZh'] if hit['contact'].get('workZh') else ''
            gender=hit['contact']['gender'] if hit['contact'].get('gender') else ''
            gindex=hit['contact']['gindex'] if hit['contact'].get('gindex') else ''


        language=hit['language'] if hit.get('language') else ''
        orgZh=hit['orgZh'] if hit.get('orgZh') else ''
        interests=hit['interests'] if hit.get('interests') else ''
        nameZh=hit['nameZh'] if hit.get('nameZh') else ''
        ncitation=hit['ncitation'] if hit.get('ncitation') else ''
        npubs=hit['npubs'] if hit.get('npubs') else ''
        name=hit['name']

        repeat_result = freeRepeat('aminer', "aminer_id", aminer_id, conn)
        print(aminer_id)


        # if repeat_result:
        #     insert_sql = 'insert into aminer(aminer_id,source_id,academicType,affiliation,affiliationZh,bio,bioZh,edu,eduZh,homepage,phone,work,workZh,gender) value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        #     cur.execute(insert_sql, (
        #     aminer_id, ids, academicType, affiliation, affiliationZh, bio, bioZh, edu, eduZh, homepage, phone, work,
        #     workZh, gender))
        #     update_='update elsevier_author_career set is_parse=1 where id =%s'
        #     cur.execute(update_,(ids,))
        #     conn.commit()


        # print(activity,)
        # print(avatar,)
        # print(contact,)
        # # print(interests,)
        # print(language,)
        # print(name,)
        # print(nameZh,)
        # # print(ncitation,)
        # # print(npubs,)
        # # print(orgZh,)
        print('**********')

a = {'activity': 728.4279,
     'avatar': 'https://static.aminer.cn/upload/avatar/1238/1709/1473/5440905edabfae7d84b8285f.jpg',
     'contact': {'academicType': '顶尖学者', 'address': '',
                 'affiliation': 'Laboratory of Photonics and Interfaces, Institute of Chemical Sciences and Engineering, Swiss Federal Institute of Technology',
                 'affiliationZh': '',
                 'bio': 'Professor of Physical Chemistry at the Ecole polytechnique fédérale de Lausanne (EPFL) Michael Graetzel, PhD, directs there the Laboratory of Photonics and Interfaces. He pioneered research on energy and electron transfer reactions in mesoscopic systems and their use to generate electricity and fuels from sunlight. He invented mesoscopic injection solar cells, one key embodiment of which is the dye-sensitized solar cell (DSC). DSCs are meanwhile commercially produced at the multi-MW-scale and created a number of new applications in particular as lightweight power supplies for portable electronic devices and in building integrated photovoltaics. They engendered perovskite solar cells (PSCs) which turned into the most exciting break-through in the history of photovoltaics. He received a number of prestigious awards, of which the most recent ones include the RusNANO Prize, the Zewail Prize in Molecular Science, the Global Energy Prize, the Millennium Technology Grand Prize, the Marcel Benoist Prize, the King Faisal International Science Prize, the Einstein World Award of Science and the Balzan Prize. He is a Fellow of several learned societies and holds eleven honorary doctor’s degrees from European and Asian Universities. His over 1500 publications have received some 220’000 citations with an h-factor of 218 (SI-Web of Science) demonstrating the strong impact of his scientific work.',
                 'bioZh': 'Graetzel教授是染料敏化太阳电池的发明人和钙钛矿太阳电池领域的国际知名专家。他领导建立了光子界面实验室,发明了染料敏化太阳电池,发表1000多篇科技论文,出版了两本专著,拥有50余项发明专利,他的工作被引次数超过134000,H因子167,是世界上被引用次数最高的10位化学家之一。 <br><br>\u3000\u3000Graetzel教授的报告深入浅出,他回顾了其从事染料敏化太阳电池的研究历程,并介绍了钙钛矿太阳电池领域的最新研究进展。报告结束后,与会人员与Michael Graetzel进行了深入讨论和交流。<br>2021年11月18日,被纳入2021年新当选中国科学院外籍院士名单并予以公示',
                 'edu': 'Dr.rer.nat. in Physical Chemistry, 1971 (summa cum laude), TU Berlin.<br>Diploma degree in Chemistry, 1968 (summa cum laude), Free University of Berlin',
                 'eduZh': '', 'email': 'michael.graetzel@epfl.ch', 'fax': '+41 21 693 31 15',
                 'homepage': 'https://www.epfl.ch/labs/lpi/graetzel/', 'note': '无教育经历',
                 'phone': '+41 21 693 31 12', 'position': 'Professor', 'positionZh': '教授',
                 'work': 'Full Professor, Director of the Laboratory of Photonics and Interfaces at EPFL, 1981 – present<br>Head of the Chemistry Department, EPFL 1991-1993, and 1983-1985. 1977 -1981.<br>Associated Professor of Physical Chemistry, EPFL 1977 – 1981 :<br>External Scientific Member, Max Planck Institute for Solid State Research Stuttgart, Germany 2018- present.<br>Guest Professor, NTU Singapore, 2011 -2018<br>Distinguished Invited Professor, National University of Singapore, 2005-2009 Invited Professor, Ecole Polytechnique Supérieure de Paris-Cachan 1998.<br>Invited Professor, University of California at Berkeley. 1974-1976.<br>Senior Staff Scientist, Hahn-Meitner Institute Berlin, Germany, 1971-1972.<br>Lecturer of Photochemistry and Physical Chemistry, Free University of Berlin.1975 -1976.<br>Petroleum Research Foundation Post-Doctoral Fellow University of Notre Dame, USA. 1972-1974 Research Associate, Hahn Meitner Institute Berlin, 1969 – 1972',
                 'workZh': ''}, 'gender': 'male', 'gindex': 620, 'hindex': 282, 'id': '5440905edabfae7d84b8285f',
     'interests': [{'t': 'Perovskite Solar Cells', 'n': 176,
                    'ny': [2013, 5, 2014, 12, 2015, 12, 2016, 18, 2017, 13, 2018, 19, 2019, 20, 2020, 20, 2021, 12,
                           2022, 11, 2023, 17, 2024, 6]}, {'t': 'Solar Cells', 'n': 170,
                                                           'ny': [1994, 1, 1996, 1, 1997, 1, 1998, 2, 1999, 1, 2001, 1,
                                                                  2003, 1, 2005, 4, 2006, 4, 2007, 5, 2008, 5, 2009, 12,
                                                                  2010, 12, 2011, 2, 2012, 16, 2013, 10, 2014, 9, 2015,
                                                                  10, 2016, 13, 2017, 11, 2018, 14, 2019, 3, 2020, 5,
                                                                  2021, 8, 2022, 3, 2023, 5, 2024, 5]},
                   {'t': 'Dye-Sensitized Solar Cells', 'n': 95,
                    'ny': [1999, 1, 2004, 2, 2005, 1, 2006, 1, 2007, 6, 2008, 4, 2009, 2, 2010, 6, 2011, 8, 2012, 8,
                           2013, 9, 2014, 8, 2015, 6, 2016, 12, 2017, 6, 2018, 8, 2020, 4, 2024, 3]},
                   {'t': 'Photovoltaic Cells', 'n': 51,
                    'ny': [1999, 1, 2004, 1, 2005, 2, 2006, 1, 2007, 2, 2012, 1, 2013, 6, 2014, 7, 2015, 1, 2016, 5,
                           2017, 3, 2018, 2, 2019, 1, 2020, 2, 2022, 1, 2023, 5, 2024, 1]},
                   {'t': 'Sensitizers', 'n': 50,
                    'ny': [1997, 2, 2000, 2, 2001, 2, 2005, 3, 2006, 1, 2007, 3, 2008, 2, 2009, 8, 2010, 5, 2011, 5,
                           2012, 6, 2013, 7, 2014, 2, 2015, 1, 2020, 1]}, {'t': 'Perovskite', 'n': 45,
                                                                           'ny': [2012, 4, 2013, 1, 2014, 8, 2015, 8,
                                                                                  2016, 4, 2017, 5, 2018, 4, 2019, 2,
                                                                                  2021, 1, 2024, 3]},
                   {'t': 'Dyes/Pigments', 'n': 44,
                    'ny': [2004, 4, 2005, 2, 2006, 1, 2007, 4, 2008, 3, 2009, 8, 2010, 6, 2011, 4, 2012, 1, 2013, 1,
                           2014, 1, 2015, 4, 2016, 5]}, {'t': 'Stability', 'n': 44,
                                                         'ny': [2007, 1, 2009, 1, 2012, 1, 2013, 1, 2014, 1, 2015, 4,
                                                                2016, 7, 2017, 4, 2018, 2, 2019, 6, 2020, 2, 2021, 4,
                                                                2022, 4, 2023, 1, 2024, 4]},
                   {'t': 'Dye Sensitized Solar Cell', 'n': 43,
                    'ny': [1995, 1, 2001, 1, 2004, 1, 2005, 1, 2006, 4, 2007, 1, 2008, 4, 2009, 7, 2010, 9, 2011, 2,
                           2013, 3, 2014, 1, 2015, 1, 2016, 1, 2017, 2, 2019, 2]},
                   {'t': 'Humanities And Social Sciences', 'n': 41,
                    'ny': [1989, 1, 1991, 2, 1998, 1, 2001, 1, 2003, 1, 2012, 4, 2013, 2, 2014, 2, 2015, 4, 2016, 1,
                           2017, 7, 2018, 3, 2019, 3, 2021, 3, 2022, 4, 2023, 2]}, {'t': 'Multidisciplinary', 'n': 41,
                                                                                    'ny': [1989, 1, 1991, 2, 1998, 1,
                                                                                           2001, 1, 2003, 1, 2012, 4,
                                                                                           2013, 2, 2014, 2, 2015, 4,
                                                                                           2016, 1, 2017, 7, 2018, 3,
                                                                                           2019, 3, 2021, 3, 2022, 4,
                                                                                           2023, 2]},
                   {'t': 'Science', 'n': 41,
                    'ny': [1989, 1, 1991, 2, 1998, 1, 2001, 1, 2003, 1, 2012, 4, 2013, 2, 2014, 2, 2015, 4, 2016, 1,
                           2017, 7, 2018, 3, 2019, 3, 2021, 3, 2022, 4, 2023, 2]}, {'t': 'Photovoltaics', 'n': 38,
                                                                                    'ny': [2005, 1, 2011, 2, 2012, 2,
                                                                                           2013, 3, 2014, 4, 2015, 3,
                                                                                           2016, 2, 2017, 6, 2018, 2,
                                                                                           2019, 2, 2020, 4, 2021, 1,
                                                                                           2022, 2, 2023, 1]},
                   {'t': 'General', 'n': 35,
                    'ny': [2007, 1, 2008, 2, 2009, 1, 2010, 1, 2011, 1, 2012, 2, 2013, 3, 2014, 5, 2015, 1, 2016, 2,
                           2017, 3, 2018, 3, 2019, 2, 2020, 1, 2021, 1, 2022, 2, 2023, 4]},
                   {'t': 'Dye-Sensitized', 'n': 34,
                    'ny': [2000, 1, 2002, 1, 2003, 1, 2004, 2, 2005, 2, 2007, 1, 2008, 2, 2010, 2, 2012, 2, 2013, 1,
                           2014, 5, 2015, 1, 2016, 5, 2020, 4]}, {'t': 'Titanium Dioxide', 'n': 31,
                                                                  'ny': [1987, 2, 1990, 2, 1995, 5, 1997, 2, 1999, 2,
                                                                         2000, 1, 2003, 1, 2004, 1, 2007, 1, 2010, 3,
                                                                         2011, 1, 2012, 2, 2013, 3, 2014, 3, 2015, 1,
                                                                         2017, 1]}, {'t': 'Water Splitting', 'n': 28,
                                                                                     'ny': [2009, 1, 2010, 2, 2011, 2,
                                                                                            2012, 6, 2013, 1, 2014, 6,
                                                                                            2015, 2, 2016, 1, 2017, 1,
                                                                                            2018, 1, 2020, 1, 2021, 3,
                                                                                            2022, 1]},
                   {'t': 'Energy Conversion', 'n': 28,
                    'ny': [1997, 1, 2009, 6, 2010, 2, 2011, 3, 2012, 1, 2013, 2, 2014, 5, 2015, 2, 2019, 4]},
                   {'t': 'Electrochemistry', 'n': 26,
                    'ny': [1998, 1, 2007, 1, 2008, 1, 2009, 5, 2010, 4, 2011, 1, 2012, 4, 2013, 3, 2014, 1, 2015, 1,
                           2019, 2, 2020, 1]}, {'t': 'Dye-Sensitized Solar Cell', 'n': 25,
                                                'ny': [2004, 2, 2008, 3, 2009, 1, 2011, 2, 2012, 4, 2013, 4, 2014, 5,
                                                       2015, 2, 2018, 1, 2019, 1]}, {'t': 'Electron Transfer', 'n': 25,
                                                                                     'ny': [1981, 2, 1993, 1, 1997, 1,
                                                                                            1998, 1, 2003, 1, 2004, 4,
                                                                                            2009, 4, 2010, 3, 2011, 2,
                                                                                            2012, 2, 2013, 1, 2019, 2]},
                   {'t': 'Solar Cell', 'n': 25,
                    'ny': [1997, 1, 2000, 1, 2003, 1, 2004, 4, 2007, 1, 2009, 1, 2010, 3, 2011, 1, 2014, 1, 2015, 4,
                           2016, 1, 2017, 1, 2018, 1, 2021, 1]}, {'t': 'Electrocatalysis', 'n': 24,
                                                                  'ny': [1987, 1, 1997, 1, 2011, 1, 2013, 3, 2014, 2,
                                                                         2017, 2, 2018, 2, 2019, 7, 2021, 1, 2022, 3,
                                                                         2023, 1]}, {'t': 'Dyes', 'n': 23,
                                                                                     'ny': [1997, 1, 2007, 1, 2009, 1,
                                                                                            2012, 8, 2013, 3, 2014, 4,
                                                                                            2016, 2, 2017, 1, 2018, 1,
                                                                                            2020, 1]},
                   {'t': 'Materials Science', 'n': 22,
                    'ny': [2000, 1, 2003, 1, 2008, 1, 2010, 1, 2011, 1, 2012, 1, 2013, 1, 2014, 4, 2015, 1, 2016, 1,
                           2018, 2, 2019, 2, 2022, 1]}, {'t': 'Perovskites', 'n': 21,
                                                         'ny': [2014, 1, 2015, 2, 2016, 4, 2017, 1, 2018, 2, 2019, 1,
                                                                2020, 1, 2021, 4, 2022, 1, 2023, 3, 2024, 1]},
                   {'t': 'Solar Cell Efficiency', 'n': 20,
                    'ny': [2013, 4, 2016, 2, 2017, 3, 2018, 2, 2019, 4, 2022, 2, 2024, 1]},
                   {'t': 'Ionic Liquids', 'n': 20,
                    'ny': [2006, 1, 2007, 3, 2008, 5, 2009, 3, 2010, 1, 2011, 1, 2012, 3, 2014, 1, 2015, 1, 2017, 1]},
                   {'t': 'Impedance Spectroscopy', 'n': 19,
                    'ny': [2007, 1, 2008, 2, 2009, 3, 2012, 1, 2013, 5, 2014, 3, 2017, 3, 2020, 1]},
                   {'t': 'Ruthenium', 'n': 19,
                    'ny': [1998, 1, 1999, 1, 2004, 4, 2008, 1, 2009, 2, 2012, 2, 2013, 3, 2015, 4, 2016, 1]},
                   {'t': 'Phthalocyanines', 'n': 19,
                    'ny': [2006, 1, 2007, 3, 2009, 5, 2012, 4, 2014, 1, 2016, 2, 2017, 3]},
                   {'t': 'Charge Transfer', 'n': 19,
                    'ny': [1987, 1, 1997, 2, 2001, 1, 2005, 2, 2009, 2, 2010, 2, 2011, 5, 2013, 1, 2018, 2]},
                   {'t': 'Organometal Halide Perovskites', 'n': 18,
                    'ny': [2014, 3, 2016, 1, 2017, 2, 2018, 3, 2019, 2, 2020, 2]}, {'t': 'Energy', 'n': 18,
                                                                                    'ny': [2009, 2, 2011, 1, 2016, 2,
                                                                                           2017, 4, 2018, 1, 2019, 2,
                                                                                           2020, 1, 2021, 1, 2022, 2,
                                                                                           2023, 2]},
                   {'t': 'Photoelectrochemistry', 'n': 18,
                    'ny': [1995, 3, 2001, 1, 2012, 7, 2013, 1, 2014, 1, 2015, 1, 2017, 1, 2021, 2]},
                   {'t': 'Photocatalysis', 'n': 18,
                    'ny': [1987, 1, 1994, 1, 1999, 1, 2009, 1, 2011, 1, 2012, 4, 2013, 1, 2014, 1, 2015, 1, 2017, 1,
                           2018, 1, 2019, 3]}, {'t': 'Thin-Film Solar Cells', 'n': 17,
                                                'ny': [1993, 1, 2013, 4, 2015, 1, 2016, 2, 2018, 2, 2019, 4, 2022, 1]},
                   {'t': 'Solar Energy', 'n': 16,
                    'ny': [1994, 1, 1997, 2, 2000, 1, 2005, 1, 2010, 2, 2011, 1, 2012, 1, 2013, 1, 2018, 2, 2020, 1]},
                   {'t': 'Perovskite Solar Cell', 'n': 16,
                    'ny': [2014, 1, 2015, 1, 2016, 1, 2017, 5, 2019, 3, 2020, 2, 2021, 1, 2022, 1, 2024, 1]},
                   {'t': 'Nanotechnology', 'n': 14,
                    'ny': [2000, 1, 2003, 1, 2004, 2, 2008, 1, 2011, 1, 2012, 1, 2013, 1, 2014, 3, 2016, 1, 2018, 2]},
                   {'t': 'Donor-Acceptor Systems', 'n': 14,
                    'ny': [2010, 2, 2011, 1, 2015, 5, 2016, 4, 2018, 1, 2020, 1]}, {'t': 'Recombination', 'n': 14,
                                                                                    'ny': [2009, 3, 2012, 1, 2013, 2,
                                                                                           2014, 1, 2017, 1, 2018, 2,
                                                                                           2019, 2, 2020, 1, 2022, 1]},
                   {'t': 'Pigments', 'n': 14, 'ny': [2012, 5, 2013, 3, 2015, 4, 2016, 1, 2020, 1]},
                   {'t': 'Nanoparticles', 'n': 13,
                    'ny': [2007, 1, 2009, 2, 2010, 2, 2011, 1, 2012, 1, 2013, 1, 2015, 2, 2017, 2]},
                   {'t': 'Inorganic Chemistry', 'n': 12,
                    'ny': [1996, 1, 2010, 1, 2012, 2, 2014, 3, 2015, 1, 2017, 1, 2019, 1, 2023, 2]},
                   {'t': 'Hydrogen Production', 'n': 12, 'ny': [1981, 5, 2005, 1, 2010, 1, 2013, 1, 2014, 3]},
                   {'t': 'Physical Chemistry', 'n': 12,
                    'ny': [1996, 1, 2010, 1, 2014, 1, 2015, 1, 2016, 1, 2017, 2, 2019, 2, 2023, 3]},
                   {'t': 'Hematite', 'n': 12, 'ny': [2009, 1, 2010, 2, 2011, 1, 2012, 4, 2013, 1, 2015, 2, 2017, 1]},
                   {'t': 'Zinc', 'n': 12, 'ny': [1987, 1, 1999, 1, 2006, 1, 2007, 3, 2009, 4, 2012, 2]},
                   {'t': 'Titanium Oxide', 'n': 12, 'ny': [1981, 4, 1998, 1, 2000, 1, 2006, 1, 2012, 1, 2014, 1]}],
     'language': 'english', 'name': 'Michael Graetzel', 'nameZh': '米夏埃尔·格雷策尔', 'ncitation': 420204,
     'npubs': 1706, 'orgZh': ''}
#
#
# # id zhu
# # souce_id 索引
# # 字段
# # is_ava=1
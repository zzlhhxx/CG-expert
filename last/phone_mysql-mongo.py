import re


from until.sql_tools import mysql_db_conn, getStrAsMD5
from until.config import he
from until.sql_tools import mongo_client
from lxml import etree
from urllib.parse import unquote
import random

import json


db=mongo_client("cg")

c=db['zjwl_author']
conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()

data=c.find()
for item in data:
    in_id_mongo=item["_id"]
    print(in_id_mongo)

    sql = f'select id,source_id,author_info_json,html_path from aminer where is_ava=1 and source_id={in_id_mongo} '
    cur.execute(sql)
    data = cur.fetchone()
    if not data:
        print('出问题了',in_id_mongo)
    else:
        in_id,source_id,author_info_json,html_path = data
        # print(in_id,source_id,aminer_id)
        address = 'Z:/' + html_path
        # print(address)
        oepn_data = open(address, 'r', encoding='utf-8').read()
        # tree = etree.HTML(data)
        # print(open(address, 'r', encoding='utf-8').read())
        json_data = re.findall(r'window.g_initialProps = (.*);', oepn_data, )
        au_phone=[]
        if json_data:
            dict_data = json.loads(json_data[0])
            profile = dict_data['profile']['profile']
            if profile.get("profile"):
                au_phone = profile['profile']['phone'].strip().split(";") if profile['profile'].get("phone") else []
        # if len(au_phone):
        # print(au_phone)
        au_phone_=[]
        if len(au_phone):
            for phone in au_phone:
                phone_zero=phone.replace("(0)","").replace("(","").replace(")","").replace(" ","-").replace(".","-").replace("--","-").replace("---","-").replace("--","-")
                au_phone_.append(phone_zero)
        print(au_phone_)
        c.update_one(
            {'_id': in_id_mongo},
            {'$set': {'au_phone': au_phone_}}
        )


a = {"global": {"collapsed": False, "preventRender": False, "isCompanyIp": False}, "profile": {"transitionState": False,
                                                                                               "profile": {
                                                                                                   "avatar": "https:\u002F\u002Fstatic.aminer.cn\u002Fupload\u002Favatar\u002F1238\u002F1709\u002F1473\u002F5440905edabfae7d84b8285f.jpg",
                                                                                                   "bind": False,
                                                                                                   "id": "5440905edabfae7d84b8285f",
                                                                                                   "indices": {
                                                                                                       "activity": 728.4279,
                                                                                                       "citations": 420204,
                                                                                                       "diversity": 4.0257,
                                                                                                       "gindex": 620,
                                                                                                       "hindex": 282,
                                                                                                       "newStar": 3.3125,
                                                                                                       "pubs": 1706,
                                                                                                       "risingStar": 3.3125,
                                                                                                       "sociability": 8.2406},
                                                                                                   "links": {"gs": {
                                                                                                       "type": "gs",
                                                                                                       "url": ""},
                                                                                                             "resource": {
                                                                                                                 "resource_link": [
                                                                                                                     {
                                                                                                                         "id": "hp",
                                                                                                                         "url": "https:\u002F\u002Fwww.epfl.ch\u002Flabs\u002Flpi\u002Fgraetzel\u002F"},
                                                                                                                     {
                                                                                                                         "id": "dblp",
                                                                                                                         "url": ""}]}},
                                                                                                   "name": "Michael Graetzel",
                                                                                                   "name_zh": "米夏埃尔·格雷策尔",
                                                                                                   "num_followed": 6,
                                                                                                   "num_upvoted": 0,
                                                                                                   "num_viewed": 1174,
                                                                                                   "profile": {
                                                                                                       "address": "",
                                                                                                       "affiliation": "Laboratory of Photonics and Interfaces, Institute of Chemical Sciences and Engineering, Swiss Federal Institute of Technology",
                                                                                                       "bio": "Professor of Physical Chemistry at the Ecole polytechnique fédérale de Lausanne (EPFL) Michael Graetzel, PhD, directs there the Laboratory of Photonics and Interfaces. He pioneered research on energy and electron transfer reactions in mesoscopic systems and their use to generate electricity and fuels from sunlight. He invented mesoscopic injection solar cells, one key embodiment of which is the dye-sensitized solar cell (DSC). DSCs are meanwhile commercially produced at the multi-MW-scale and created a number of new applications in particular as lightweight power supplies for portable electronic devices and in building integrated photovoltaics. They engendered perovskite solar cells (PSCs) which turned into the most exciting break-through in the history of photovoltaics. He received a number of prestigious awards, of which the most recent ones include the RusNANO Prize, the Zewail Prize in Molecular Science, the Global Energy Prize, the Millennium Technology Grand Prize, the Marcel Benoist Prize, the King Faisal International Science Prize, the Einstein World Award of Science and the Balzan Prize. He is a Fellow of several learned societies and holds eleven honorary doctor’s degrees from European and Asian Universities. His over 1500 publications have received some 220’000 citations with an h-factor of 218 (SI-Web of Science) demonstrating the strong impact of his scientific work.",
                                                                                                       "bio_zh": "Graetzel教授是染料敏化太阳电池的发明人和钙钛矿太阳电池领域的国际知名专家。他领导建立了光子界面实验室，发明了染料敏化太阳电池，发表1000多篇科技论文，出版了两本专著，拥有50余项发明专利，他的工作被引次数超过134000，H因子167，是世界上被引用次数最高的10位化学家之一。 \u003Cbr\u003E\u003Cbr\u003E　　Graetzel教授的报告深入浅出，他回顾了其从事染料敏化太阳电池的研究历程，并介绍了钙钛矿太阳电池领域的最新研究进展。报告结束后，与会人员与Michael Graetzel进行了深入讨论和交流。\u003Cbr\u003E2021年11月18日，被纳入2021年新当选中国科学院外籍院士名单并予以公示",
                                                                                                       "edu": "Dr.rer.nat. in Physical Chemistry, 1971 (summa cum laude), TU Berlin.\u003Cbr\u003EDiploma degree in Chemistry, 1968 (summa cum laude), Free University of Berlin",
                                                                                                       "edu_zh": "",
                                                                                                       "email": "",
                                                                                                       "fax": "+41 21 693 31 15",
                                                                                                       "gender": "male",
                                                                                                       "homepage": "https:\u002F\u002Fwww.epfl.ch\u002Flabs\u002Flpi\u002Fgraetzel\u002F",
                                                                                                       "lang": "english",
                                                                                                       "note": "无教育经历",
                                                                                                       "org_zh": "",
                                                                                                       "phone": "+41 21 693 31 12",
                                                                                                       "position": "Professor",
                                                                                                       "position_zh": "教授",
                                                                                                       "work": "Full Professor, Director of the Laboratory of Photonics and Interfaces at EPFL, 1981 – present\u003Cbr\u003EHead of the Chemistry Department, EPFL 1991-1993, and 1983-1985. 1977 -1981.\u003Cbr\u003EAssociated Professor of Physical Chemistry, EPFL 1977 – 1981 :\u003Cbr\u003EExternal Scientific Member, Max Planck Institute for Solid State Research Stuttgart, Germany 2018- present.\u003Cbr\u003EGuest Professor, NTU Singapore, 2011 -2018\u003Cbr\u003EDistinguished Invited Professor, National University of Singapore, 2005-2009 Invited Professor, Ecole Polytechnique Supérieure de Paris-Cachan 1998.\u003Cbr\u003EInvited Professor, University of California at Berkeley. 1974-1976.\u003Cbr\u003ESenior Staff Scientist, Hahn-Meitner Institute Berlin, Germany, 1971-1972.\u003Cbr\u003ELecturer of Photochemistry and Physical Chemistry, Free University of Berlin.1975 -1976.\u003Cbr\u003EPetroleum Research Foundation Post-Doctoral Fellow University of Notre Dame, USA. 1972-1974 Research Associate, Hahn Meitner Institute Berlin, 1969 – 1972",
                                                                                                       "work_zh": ""},
                                                                                                   "tags": [
                                                                                                       "Carbon Nanotubes",
                                                                                                       "Carbon Nanotube",
                                                                                                       "Band Gap",
                                                                                                       "Solar Cells",
                                                                                                       "Aqueous Solutions",
                                                                                                       "Titanium Dioxide",
                                                                                                       "Energy Transfer",
                                                                                                       "Electron Transfer",
                                                                                                       "Transition Metal",
                                                                                                       "Spray Pyrolysis",
                                                                                                       "Conduction Band",
                                                                                                       "Aqueous Solution",
                                                                                                       "Electric Field",
                                                                                                       "Visible Light",
                                                                                                       "Energy Harvesting",
                                                                                                       "Power Conversion",
                                                                                                       "Metal Oxide Semiconductor",
                                                                                                       "Surface Area",
                                                                                                       "Novel Synthesis",
                                                                                                       "Perovskite Solar Cells"],
                                                                                                   "tags_score": [
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
                                                                                               "profileID": "5440905edabfae7d84b8285f",
                                                                                               "profilePubsPage": 1,
                                                                                               "profilePubs": [{
                                                                                                                   "abstract": "This study points out the importance of the templating effect in hybrid organic-inorganic perovskite semiconductors grown on graphene. By combining two achiral materials, we report the formation of a chiral composite heterostructure with electronic band splitting. The effect is observed through circularly polarized light emission and detection in a graphene\u002Falpha-CH(NH2)(2)PbI3 perovskite composite, at ambient temperature and without a magnetic field. We exploit the spin-charge conversion by introducing an unbalanced spin population through polarized light that gives rise to a spin photoconductive effect rationalized by Rashba-type coupling. The prepared composite heterostructure exhibits a circularly polarized photoluminescence anisotropy g(CPL) of similar to 0.35 at similar to 2.54 x 10(3) W cm(-2) confocal power density of 532 nm excitation. A carefully engineered interface between the graphene and the perovskite thin film enhances the Rashba field and generates the built-in electric field responsible for photocurrent, yielding a photoresponsivity of similar to 10(5) A W-1 under similar to 0.08 mu W cm(-2) fluence of visible light photons. The maximum photocurrent anisotropy factor g(ph) is similar to 0.51 under similar to 0.16 mu W cm(-2) irradiance. The work sheds light on the photophysical properties of graphene\u002Fperovskite composite heterostructures, finding them to be a promising candidate for developing miniaturized spin-photonic devices.",
                                                                                                                   "authors": [
                                                                                                                       {
                                                                                                                           "id": "62e4b1ead9f204418d6e709d",
                                                                                                                           "name": "Oleksandr Volochanskyi",
                                                                                                                           "org": "Czech Acad Sci, J Heyrovsky Inst Phys Chem, Dept Low Dimens Syst, Prague 18223, Czech Republic"},
                                                                                                                       {
                                                                                                                           "email": "g.haider@ifw-dresden.de",
                                                                                                                           "id": "5630fa9c45cedb3399c2b203",
                                                                                                                           "name": "Golam Haider",
                                                                                                                           "org": "Czech Acad Sci, J Heyrovsky Inst Phys Chem, Dept Low Dimens Syst, Prague 18223, Czech Republic"},
                                                                                                                       {
                                                                                                                           "id": "6378cd9ad49364c9ac99eb91",
                                                                                                                           "name": "Essa A. Alharbi",
                                                                                                                           "org": "King Abdulaziz City Sci & Technol KACST, Microelect & Semicond Inst, Riyadh 11442, Saudi Arabia"},
                                                                                                                       {
                                                                                                                           "id": "5612dd7d45ce1e5962e18959",
                                                                                                                           "name": "George Kakavelakis",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Lab Photon & Interfaces, CH-1015 Lausanne, Switzerland",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c85c"},
                                                                                                                       {
                                                                                                                           "id": "65a5dc198a47b62d65954a24",
                                                                                                                           "name": "Martin Mergl",
                                                                                                                           "org": "Czech Acad Sci, J Heyrovsky Inst Phys Chem, Dept Low Dimens Syst, Prague 18223, Czech Republic"},
                                                                                                                       {
                                                                                                                           "id": "62e4bc09d9f204418d70e569",
                                                                                                                           "name": "Mukesh Kumar Thakur",
                                                                                                                           "org": "Czech Acad Sci, J Heyrovsky Inst Phys Chem, Dept Low Dimens Syst, Prague 18223, Czech Republic"},
                                                                                                                       {
                                                                                                                           "id": "62e47bcad9f204418d689b33",
                                                                                                                           "name": "Anurag Krishna",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Lab Photon & Interfaces, CH-1015 Lausanne, Switzerland",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c85c"},
                                                                                                                       {
                                                                                                                           "id": "5440905edabfae7d84b8285f",
                                                                                                                           "name": "Michael Graetzel",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Lab Photon & Interfaces, CH-1015 Lausanne, Switzerland",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c85c"},
                                                                                                                       {
                                                                                                                           "email": "martin.kalbac@jh-inst.cas.cz",
                                                                                                                           "id": "53f44984dabfaedd74dfb276",
                                                                                                                           "name": "Martin Kalbac",
                                                                                                                           "org": "Czech Acad Sci, J Heyrovsky Inst Phys Chem, Dept Low Dimens Syst, Prague 18223, Czech Republic"}],
                                                                                                                   "create_time": "2024-09-20T10:33:42.131Z",
                                                                                                                   "doi": "10.1021\u002Facsami.4c10289",
                                                                                                                   "id": "66ec821701d2a3fbfc6b90ea",
                                                                                                                   "issn": "1944-8244",
                                                                                                                   "keywords": [
                                                                                                                       "chirality",
                                                                                                                       "optical helicity sensing",
                                                                                                                       "Rashbasplitting",
                                                                                                                       "graphene",
                                                                                                                       "perovskite",
                                                                                                                       "photodetector"],
                                                                                                                   "lang": "en",
                                                                                                                   "num_citation": 0,
                                                                                                                   "pages": {
                                                                                                                       "end": "52798",
                                                                                                                       "start": "52789"},
                                                                                                                   "title": "Graphene-Templated Achiral Hybrid Perovskite for Circularly Polarized Light Sensing.",
                                                                                                                   "update_times": {
                                                                                                                       "u_a_t": "2024-11-21T20:15:56Z",
                                                                                                                       "u_v_t": "2024-11-21T20:15:56Z"},
                                                                                                                   "urls": [
                                                                                                                       "https:\u002F\u002Fwww.ncbi.nlm.nih.gov\u002Fpubmed\u002F39297304"],
                                                                                                                   "venue": {
                                                                                                                       "info": {
                                                                                                                           "name": "ACS APPLIED MATERIALS & INTERFACES"},
                                                                                                                       "issue": "39",
                                                                                                                       "volume": "16"},
                                                                                                                   "versions": [
                                                                                                                       {
                                                                                                                           "id": "66ec821701d2a3fbfc6b90ea",
                                                                                                                           "sid": "39297304",
                                                                                                                           "src": "pubmed",
                                                                                                                           "vsid": "ACS APPLIED MATERIALS & INTERFACES",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "66ed4e9d01d2a3fbfca1690d",
                                                                                                                           "sid": "10.1021\u002Facsami.4c10289",
                                                                                                                           "src": "crossref",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "6711c7dd01d2a3fbfc649478",
                                                                                                                           "sid": "WOS:001317109800001",
                                                                                                                           "src": "wos",
                                                                                                                           "vsid": "ACS APPLIED MATERIALS & INTERFACES",
                                                                                                                           "year": 2024}],
                                                                                                                   "year": 2024},
                                                                                                               {
                                                                                                                   "abstract": "High-performance perovskite solar cells (PSCs) typically require interfacial passivation, yet this is challenging for the buried interface, owing to the dissolution of passivation agents during the deposition of perovskites. Here, this limitation is overcome with in situ buried-interface passivation-achieved via directly adding a cyanoacrylic-acid-based molecular additive, namely BT-T, into the perovskite precursor solution. Classical and ab initio molecular dynamics simulations reveal that BT-T spontaneously may self-assemble at the buried interface during the formation of the perovskite layer on a nickel oxide hole-transporting layer. The preferential buried-interface passivation results in facilitated hole transfer and suppressed charge recombination. In addition, residual BT-T molecules in the perovskite layer enhance its stability and homogeneity. A power-conversion efficiency (PCE) of 23.48% for 1.0 cm(2) inverted-structure PSCs is reported. The encapsulated PSC retains 95.4% of its initial PCE following 1960 h maximum-power-point tracking under continuous light illumination at 65 degrees C (i.e., ISOS-L-2I protocol). The demonstration of operating-stable PSCs under accelerated ageing conditions represents a step closer to the commercialization of this emerging technology.",
                                                                                                                   "authors": [
                                                                                                                       {
                                                                                                                           "id": "632549b9128293c81ede5f15",
                                                                                                                           "name": "Lin Li",
                                                                                                                           "org": "Huazhong Univ Sci & Technol, Michael Gratzel Ctr Mesoscop Solar Cells, Wuhan Natl Lab Optoelect, Wuhan 430074, Peoples R China"},
                                                                                                                       {
                                                                                                                           "id": "54591780dabfaeb0fe2eec21",
                                                                                                                           "name": "Mingyang Wei",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne EPFL, Inst Chem Sci & Engn, Lab Photon & Interfaces, CH-1015 Lausanne, Switzerland",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c85c"},
                                                                                                                       {
                                                                                                                           "id": "62e4bc32d9f204418d70eecc",
                                                                                                                           "name": "Virginia Carnevali",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne EPFL, Inst Chem Sci & Engn, Lab Computat Chem & Biochem, CH-1015 Lausanne, Switzerland"},
                                                                                                                       {
                                                                                                                           "id": "63733c67ec88d95668d62399",
                                                                                                                           "name": "Haipeng Zeng",
                                                                                                                           "org": "Huazhong Univ Sci & Technol, Michael Gratzel Ctr Mesoscop Solar Cells, Wuhan Natl Lab Optoelect, Wuhan 430074, Peoples R China"},
                                                                                                                       {
                                                                                                                           "name": "Miaomiao Zeng",
                                                                                                                           "org": "Huazhong Univ Sci & Technol, Michael Gratzel Ctr Mesoscop Solar Cells, Wuhan Natl Lab Optoelect, Wuhan 430074, Peoples R China"},
                                                                                                                       {
                                                                                                                           "id": "64e927988a47b66603e4ad00",
                                                                                                                           "name": "Ranran Liu",
                                                                                                                           "org": "Huazhong Univ Sci & Technol, Michael Gratzel Ctr Mesoscop Solar Cells, Wuhan Natl Lab Optoelect, Wuhan 430074, Peoples R China"},
                                                                                                                       {
                                                                                                                           "id": "53f4cff5dabfaeeee1f8141a",
                                                                                                                           "name": "Nikolaos Lempesis",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne EPFL, Inst Chem Sci & Engn, Lab Computat Chem & Biochem, CH-1015 Lausanne, Switzerland"},
                                                                                                                       {
                                                                                                                           "id": "53f42e34dabfaee1c0a3e4f9",
                                                                                                                           "name": "Felix Thomas Eickemeyer",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne EPFL, Inst Chem Sci & Engn, Lab Photon & Interfaces, CH-1015 Lausanne, Switzerland",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c85c"},
                                                                                                                       {
                                                                                                                           "id": "6328d76630241ae3e5ac774e",
                                                                                                                           "name": "Long Luo",
                                                                                                                           "org": "Huazhong Univ Sci & Technol, Michael Gratzel Ctr Mesoscop Solar Cells, Wuhan Natl Lab Optoelect, Wuhan 430074, Peoples R China"},
                                                                                                                       {
                                                                                                                           "id": "562b46c345cedb33989e76c2",
                                                                                                                           "name": "Lorenzo Agosta",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne EPFL, Inst Chem Sci & Engn, Lab Computat Chem & Biochem, CH-1015 Lausanne, Switzerland"},
                                                                                                                       {
                                                                                                                           "id": "645c3a9d9bb9460001f70989",
                                                                                                                           "name": "Mathias Dankl",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne EPFL, Inst Chem Sci & Engn, Lab Computat Chem & Biochem, CH-1015 Lausanne, Switzerland"},
                                                                                                                       {
                                                                                                                           "id": "53f45043dabfaeecd69d3ade",
                                                                                                                           "name": "Shaik M. Zakeeruddin",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne EPFL, Inst Chem Sci & Engn, Lab Photon & Interfaces, CH-1015 Lausanne, Switzerland",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c85c"},
                                                                                                                       {
                                                                                                                           "email": "ursula.roethlisberger@epfl.ch",
                                                                                                                           "id": "5616deac45ce1e5963b3c153",
                                                                                                                           "name": "Ursula Roethlisberger",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne EPFL, Inst Chem Sci & Engn, Lab Computat Chem & Biochem, CH-1015 Lausanne, Switzerland"},
                                                                                                                       {
                                                                                                                           "id": "5440905edabfae7d84b8285f",
                                                                                                                           "name": "Michael Gratzel",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne EPFL, Inst Chem Sci & Engn, Lab Photon & Interfaces, CH-1015 Lausanne, Switzerland",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c85c"},
                                                                                                                       {
                                                                                                                           "email": "ygrong@whut.edu.cn",
                                                                                                                           "id": "5612d70c45cedb339796f88a",
                                                                                                                           "name": "Yaoguang Rong",
                                                                                                                           "org": "Wuhan Univ Technol, Sch Chem Chem Engn & Life Sci, Wuhan 430070, Peoples R China",
                                                                                                                           "orgid": "5f71b2d51c455f439fe3e951"},
                                                                                                                       {
                                                                                                                           "email": "xiongli@hust.edu.cn",
                                                                                                                           "id": "5dcc1aaa530c70d7ce5e4e68",
                                                                                                                           "name": "Xiong Li",
                                                                                                                           "org": "Huazhong Univ Sci & Technol, Michael Gratzel Ctr Mesoscop Solar Cells, Wuhan Natl Lab Optoelect, Wuhan 430074, Peoples R China"}],
                                                                                                                   "create_time": "2023-12-30T04:17:33.466Z",
                                                                                                                   "doi": "10.1002\u002Fadma.202303869",
                                                                                                                   "id": "64ec376c3fda6d7f063f3453",
                                                                                                                   "issn": "0935-9648",
                                                                                                                   "keywords": [
                                                                                                                       "cyanoacrylic-acid-based molecular additive",
                                                                                                                       "In situ buried-interface passivation",
                                                                                                                       "inverted perovskite solar cells",
                                                                                                                       "NiOx hole-transporting materials",
                                                                                                                       "stability"],
                                                                                                                   "lang": "en",
                                                                                                                   "num_citation": 0,
                                                                                                                   "title": "Buried-Interface Engineering Enables Efficient and 1960-Hour ISOS-L-2I Stable Inverted Perovskite Solar Cells",
                                                                                                                   "update_times": {
                                                                                                                       "u_a_t": "2024-11-22T00:23:50Z",
                                                                                                                       "u_v_t": "2024-11-22T00:23:50Z"},
                                                                                                                   "urls": [
                                                                                                                       "https:\u002F\u002Fopenalex.org\u002FW4386188968",
                                                                                                                       "https:\u002F\u002Fdoi.org\u002F10.1002\u002Fadma.202303869"],
                                                                                                                   "venue": {
                                                                                                                       "info": {
                                                                                                                           "name": "ADVANCED MATERIALS"},
                                                                                                                       "issue": "13",
                                                                                                                       "volume": "36"},
                                                                                                                   "venue_hhb_id": "5ea5749fedb6e7d53c03fc5c",
                                                                                                                   "versions": [
                                                                                                                       {
                                                                                                                           "id": "6578e9ed939a5f40828de28f",
                                                                                                                           "sid": "W4386188968",
                                                                                                                           "src": "openalex",
                                                                                                                           "vsid": "ADVANCED MATERIALS",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "666438e701d2a3fbfcb603bc",
                                                                                                                           "sid": "10.1002\u002Fadma.202303869",
                                                                                                                           "src": "crossref",
                                                                                                                           "year": 2023},
                                                                                                                       {
                                                                                                                           "id": "64ec376c3fda6d7f063f3453",
                                                                                                                           "sid": "37632843",
                                                                                                                           "src": "pubmed",
                                                                                                                           "vsid": "9885358",
                                                                                                                           "year": 2023},
                                                                                                                       {
                                                                                                                           "id": "65a1277f939a5f40820894d0",
                                                                                                                           "sid": "WOS:001134222300001",
                                                                                                                           "src": "wos",
                                                                                                                           "vsid": "ADVANCED MATERIALS",
                                                                                                                           "year": 2024}],
                                                                                                                   "year": 2024},
                                                                                                               {
                                                                                                                   "abstract": "Hybrid metal halide perovskites have demonstrated remarkable performances in modern photovoltaics, although their stabilities remain limited. We assess the capacity to advance their properties by relying on interfacial modulators featuring helical chirality based on P,M-(1-methylene-3-methyl-imidazolium)[6]helicene iodides. We investigate their characteristics, demonstrating comparable charge injection for enantiomers and the racemic mixture. Overall, they maintain the resulting photovoltaic performance while improving operational stability, challenging the role of helical chirality in the interfacial modulation of perovskite solar cells.",
                                                                                                                   "authors": [
                                                                                                                       {
                                                                                                                           "id": "65a43de58a47b62d65913661",
                                                                                                                           "name": "Masaud Almalki",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Inst Chem Sci & Engn, Lab Photon & Interfaces, Lausanne, Switzerland"},
                                                                                                                       {
                                                                                                                           "id": "64973e4ca88fbe7c0502609d",
                                                                                                                           "name": "Ghewa Alsabeh",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Inst Chem Sci & Engn, Lab Photon & Interfaces, Lausanne, Switzerland"},
                                                                                                                       {
                                                                                                                           "id": "637ad372f789b382bea3fc0a",
                                                                                                                           "name": "Marco A. Ruiz-Preciado",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Inst Chem Sci & Engn, Lab Photon & Interfaces, Lausanne, Switzerland"},
                                                                                                                       {
                                                                                                                           "id": "562f947345cedb33997160c2",
                                                                                                                           "name": "Hong Zhang",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Inst Chem Sci & Engn, Lab Photon & Interfaces, Lausanne, Switzerland"},
                                                                                                                       {
                                                                                                                           "name": "Melodie Galerne",
                                                                                                                           "org": "Univ Strasbourg, CNRS, SAMS Res Grp, Inst Charles Sadron,UPR22, F-67000 Strasbourg, France"},
                                                                                                                       {
                                                                                                                           "id": "53f43942dabfaeb1a7c0f4c5",
                                                                                                                           "name": "Emilie Moulin",
                                                                                                                           "org": "Univ Strasbourg, CNRS, SAMS Res Grp, Inst Charles Sadron,UPR22, F-67000 Strasbourg, France"},
                                                                                                                       {
                                                                                                                           "id": "53f42e34dabfaee1c0a3e4f9",
                                                                                                                           "name": "Felix Thomas Eickemeyer",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Inst Chem Sci & Engn, Lab Photon & Interfaces, Lausanne, Switzerland"},
                                                                                                                       {
                                                                                                                           "id": "53f45043dabfaeecd69d3ade",
                                                                                                                           "name": "Shaik M. Zakeeruddin",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Inst Chem Sci & Engn, Lab Photon & Interfaces, Lausanne, Switzerland"},
                                                                                                                       {
                                                                                                                           "email": "jovana.milic@unifr.ch",
                                                                                                                           "id": "56141b0045ce1e5963323c5e",
                                                                                                                           "name": "Jovana V. Milic",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Inst Chem Sci & Engn, Lab Photon & Interfaces, Lausanne, Switzerland"},
                                                                                                                       {
                                                                                                                           "email": "giuseppone@unistra.fr",
                                                                                                                           "id": "53f42bb5dabfaedd74d1d424",
                                                                                                                           "name": "Nicolas Giuseppone",
                                                                                                                           "org": "Univ Strasbourg, CNRS, SAMS Res Grp, Inst Charles Sadron,UPR22, F-67000 Strasbourg, France"},
                                                                                                                       {
                                                                                                                           "id": "5440905edabfae7d84b8285f",
                                                                                                                           "name": "Michael Gratzel",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Inst Chem Sci & Engn, Lab Photon & Interfaces, Lausanne, Switzerland"}],
                                                                                                                   "create_time": "2024-07-12T03:11:45.954Z",
                                                                                                                   "doi": "10.1039\u002Fd4na00027g",
                                                                                                                   "id": "66594d7901d2a3fbfc13b49d",
                                                                                                                   "issn": "2196-7350",
                                                                                                                   "keywords": [
                                                                                                                       "hybrid perovskite photovoltaics",
                                                                                                                       "molecular charge transport",
                                                                                                                       "supramolecular modulation",
                                                                                                                       "triarylamine"],
                                                                                                                   "lang": "en",
                                                                                                                   "num_citation": 0,
                                                                                                                   "title": "Helical Interfacial Modulation for Perovskite Photovoltaics",
                                                                                                                   "update_times": {
                                                                                                                       "u_a_t": "2024-11-21T21:21:15Z",
                                                                                                                       "u_v_t": "2024-11-21T21:21:15Z"},
                                                                                                                   "urls": [
                                                                                                                       "https:\u002F\u002Fapi.crossref.org\u002Fworks\u002F10.1039\u002Fd4na00027g",
                                                                                                                       "http:\u002F\u002Fdx.doi.org\u002F10.1039\u002Fd4na00027g",
                                                                                                                       "https:\u002F\u002Fxlink.rsc.org\u002F?DOI=D4NA00027G"],
                                                                                                                   "venue": {
                                                                                                                       "info": {
                                                                                                                           "name": "ADVANCED MATERIALS INTERFACES"}},
                                                                                                                   "venue_hhb_id": "5ea57076edb6e7d53c03efa9",
                                                                                                                   "versions": [
                                                                                                                       {
                                                                                                                           "id": "66594d7901d2a3fbfc13b49d",
                                                                                                                           "sid": "10.1039\u002Fd4na00027g",
                                                                                                                           "src": "crossref",
                                                                                                                           "vsid": "ADVANCED MATERIALS INTERFACES",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "666b503201d2a3fbfc5793c3",
                                                                                                                           "sid": "38868831",
                                                                                                                           "src": "pubmed",
                                                                                                                           "vsid": "101738708",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "6674f4ed01d2a3fbfc3057e8",
                                                                                                                           "sid": "10.1002\u002Fadmi.202301053",
                                                                                                                           "src": "crossref",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "6678ab7c01d2a3fbfcba4174",
                                                                                                                           "sid": "WOS:001234997800001",
                                                                                                                           "src": "wos",
                                                                                                                           "vsid": "NANOSCALE ADVANCES",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "669a1a5901d2a3fbfc8583a1",
                                                                                                                           "sid": "S2516023024002193",
                                                                                                                           "src": "sciencedirect",
                                                                                                                           "vsid": "nanoscale-advances",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "66cd8eb401d2a3fbfcb13736",
                                                                                                                           "sid": "W4399176068",
                                                                                                                           "src": "openalex",
                                                                                                                           "vsid": "S4210240921",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "66ddd51d01d2a3fbfc8e72a4",
                                                                                                                           "sid": "W4399871430",
                                                                                                                           "src": "openalex",
                                                                                                                           "vsid": "S2764385675",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "668f93d601d2a3fbfca0b435",
                                                                                                                           "sid": "WOS:001250311200001",
                                                                                                                           "src": "wos",
                                                                                                                           "vsid": "ADVANCED MATERIALS INTERFACES",
                                                                                                                           "year": 2024}],
                                                                                                                   "year": 2024},
                                                                                                               {
                                                                                                                   "abstract": "Light-induced degradation in metal halide perovskites is a major concern that can potentially hamper the commercialization of perovskite optoelectronic devices.",
                                                                                                                   "authors": [
                                                                                                                       {
                                                                                                                           "id": "62e48b65d9f204418d6a30cd",
                                                                                                                           "name": "Jeremy Hieulle",
                                                                                                                           "org": "Univ Luxembourg, Dept Phys & Mat Sci, L-1511 Luxembourg, Luxembourg",
                                                                                                                           "orgid": "5f71b3711c455f439fe42edd"},
                                                                                                                       {
                                                                                                                           "id": "62e47bcad9f204418d689b33",
                                                                                                                           "name": "Anurag Krishna",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Inst Chem Sci & Engn, Lab Photomol Sci, CH-1015 Lausanne, Switzerland",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c85c"},
                                                                                                                       {
                                                                                                                           "id": "62e48cbbd9f204418d6a7280",
                                                                                                                           "name": "Ariadni Boziki",
                                                                                                                           "org": "Univ Luxembourg, Dept Phys & Mat Sci, L-1511 Luxembourg, Luxembourg",
                                                                                                                           "orgid": "5f71b3711c455f439fe42edd"},
                                                                                                                       {
                                                                                                                           "id": "53f43571dabfaec09f174e80",
                                                                                                                           "name": "Jean-Nicolas Audinot",
                                                                                                                           "org": "Luxembourg Inst Sci & Technol LIST, Mat Res & Technol MRT, Adv Instrumentat Nanoanalyt AINA, L-4362 Esch Sur Alzette, Luxembourg"},
                                                                                                                       {
                                                                                                                           "id": "65d9faa78a47b621f782a2f1",
                                                                                                                           "name": "Muhammad Uzair Farooq",
                                                                                                                           "org": "Univ Luxembourg, Dept Phys & Mat Sci, L-1511 Luxembourg, Luxembourg",
                                                                                                                           "orgid": "5f71b3711c455f439fe42edd"},
                                                                                                                       {
                                                                                                                           "id": "6592b6edb2e21a410e269a0c",
                                                                                                                           "name": "Joana Ferreira Machado",
                                                                                                                           "org": "Univ Luxembourg, Dept Phys & Mat Sci, L-1511 Luxembourg, Luxembourg",
                                                                                                                           "orgid": "5f71b3711c455f439fe42edd"},
                                                                                                                       {
                                                                                                                           "id": "562b958945cedb3398ac2878",
                                                                                                                           "name": "Marko Mladenovic",
                                                                                                                           "org": "ETH, Dept Informat Technol & Elect Engn, Integrated Syst Lab, CH-8092 Zurich, Switzerland",
                                                                                                                           "orgid": "62331e350a6eb147dca8a805"},
                                                                                                                       {
                                                                                                                           "id": "65cb58fb8a47b621f75ef9cd",
                                                                                                                           "name": "Himanshu Phirke",
                                                                                                                           "org": "Univ Luxembourg, Dept Phys & Mat Sci, L-1511 Luxembourg, Luxembourg",
                                                                                                                           "orgid": "5f71b3711c455f439fe42edd"},
                                                                                                                       {
                                                                                                                           "id": "64cc9cf370d44317c2e36156",
                                                                                                                           "name": "Ajay Singh",
                                                                                                                           "org": "Univ Luxembourg, Dept Phys & Mat Sci, L-1511 Luxembourg, Luxembourg",
                                                                                                                           "orgid": "5f71b3711c455f439fe42edd"},
                                                                                                                       {
                                                                                                                           "id": "53f42cb7dabfaeb1a7b8129d",
                                                                                                                           "name": "Tom Wirtz",
                                                                                                                           "org": "Luxembourg Inst Sci & Technol LIST, Mat Res & Technol MRT, Adv Instrumentat Nanoanalyt AINA, L-4362 Esch Sur Alzette, Luxembourg"},
                                                                                                                       {
                                                                                                                           "id": "53f445c3dabfaee0d9bb0958",
                                                                                                                           "name": "Alexandre Tkatchenko",
                                                                                                                           "org": "Univ Luxembourg, Dept Phys & Mat Sci, L-1511 Luxembourg, Luxembourg",
                                                                                                                           "orgid": "5f71b3711c455f439fe42edd"},
                                                                                                                       {
                                                                                                                           "id": "5440905edabfae7d84b8285f",
                                                                                                                           "name": "Michael Graetzel",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Inst Chem Sci & Engn, Lab Photon & Interfaces, CH-1015 Lausanne, Switzerland",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c85c"},
                                                                                                                       {
                                                                                                                           "id": "5406768bdabfae44f0834db8",
                                                                                                                           "name": "Anders Hagfeldt",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Inst Chem Sci & Engn, Lab Photomol Sci, CH-1015 Lausanne, Switzerland",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c85c"},
                                                                                                                       {
                                                                                                                           "email": "alex.redinger@uni.lu",
                                                                                                                           "id": "53f43504dabfaee1c0a916c1",
                                                                                                                           "name": "Alex Redinger",
                                                                                                                           "org": "Univ Luxembourg, Dept Phys & Mat Sci, L-1511 Luxembourg, Luxembourg",
                                                                                                                           "orgid": "5f71b3711c455f439fe42edd"}],
                                                                                                                   "create_time": "2024-05-10T15:13:17.123Z",
                                                                                                                   "doi": "10.1039\u002Fd3ee03511e",
                                                                                                                   "id": "65a126d6939a5f4082074093",
                                                                                                                   "issn": "1754-5692",
                                                                                                                   "lang": "en",
                                                                                                                   "num_citation": 0,
                                                                                                                   "pages": {
                                                                                                                       "end": "295",
                                                                                                                       "start": "284"},
                                                                                                                   "pdf": "https:\u002F\u002Fstatic.aminer.cn\u002Fupload\u002Fpdf\u002F277\u002F1252\u002F1241\u002F65a126d6939a5f4082074093_0.pdf",
                                                                                                                   "title": "Understanding and Decoupling the Role of Wavelength and Defects in Light-Induced Degradation of Metal-Halide Perovskites",
                                                                                                                   "update_times": {
                                                                                                                       "u_a_t": "2024-11-09T06:12:12Z",
                                                                                                                       "u_v_t": "2024-11-09T06:12:12Z"},
                                                                                                                   "urls": [
                                                                                                                       "http:\u002F\u002Fwww.webofknowledge.com\u002F"],
                                                                                                                   "venue": {
                                                                                                                       "info": {
                                                                                                                           "name": "ENERGY & ENVIRONMENTAL SCIENCE"},
                                                                                                                       "issue": "1",
                                                                                                                       "volume": "17"},
                                                                                                                   "venue_hhb_id": "5ea552daedb6e7d53c036a29",
                                                                                                                   "versions": [
                                                                                                                       {
                                                                                                                           "id": "65a126d6939a5f4082074093",
                                                                                                                           "sid": "WOS:001111600900001",
                                                                                                                           "src": "wos",
                                                                                                                           "vsid": "ENERGY & ENVIRONMENTAL SCIENCE",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "6662dc3d01d2a3fbfc60ebc2",
                                                                                                                           "sid": "10.1039\u002Fd3ee03511e",
                                                                                                                           "src": "crossref",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "65b690ae939a5f4082540040",
                                                                                                                           "sid": "W4389225611",
                                                                                                                           "src": "openalex",
                                                                                                                           "vsid": "S117082959",
                                                                                                                           "year": 2024}],
                                                                                                                   "year": 2024},
                                                                                                               {
                                                                                                                   "abstract": "In this work we study in-depth the antireflection and filtering properties of ultrathin-metal-film-based transparent electrodes (MTEs) integrated in thin-film solar cells. Based on numerical optimization of the MTE design and the experimental characterization of thin-film perovskite solar cell (PSC) samples, we show that reflection in the visible spectrum can be strongly suppressed, in contrast to common belief (due to the compact metal layer). The optical loss of the optimized electrode (~ 2.9%), composed of a low-resistivity metal and an insulator, is significantly lower than that of a conventional transparent conductive oxide (TCO ~ 6.3%), thanks to the very high transmission of visible light within the cell (\u003E 91%) and low thickness (\u003C 70 nm), whereas the reflection of infrared light (~ 70%) improves by \u003E 370%. To assess the application potentials, integrated current density \u003E 25 mA\u002Fcm2, power conversion efficiency \u003E 20%, combined with vastly reduced device heat load by 177.1 W\u002Fm2 was achieved in state-of-the-art PSCs. Our study aims to set the basis for a novel interpretation of composite electrodes\u002Fstructures, such as TCO–metal–TCO, dielectric–metal–dielectric or insulator–metal–insulator, and hyperbolic metamaterials, in high-efficiency optoelectronic devices, such as solar cells, semi-transparent, and concentrated systems, and other electro-optical components including smart windows, light-emitting diodes, and displays.",
                                                                                                                   "authors": [
                                                                                                                       {
                                                                                                                           "email": "gperrakis@iesl.forth.gr",
                                                                                                                           "id": "62e4bda3d9f204418d715d1e",
                                                                                                                           "name": "George Perrakis",
                                                                                                                           "org": "Institute of Electronic Structure and Laser (IESL), Foundation for Research and Technology - Hellas (FORTH), 70013, Heraklion, Crete, Greece. gperrakis@iesl.forth.gr."},
                                                                                                                       {
                                                                                                                           "id": "56187a7d45ce1e5964074ba4",
                                                                                                                           "name": "Anna C. Tasolamprou",
                                                                                                                           "org": "Institute of Electronic Structure and Laser (IESL), Foundation for Research and Technology - Hellas (FORTH), 70013, Heraklion, Crete, Greece."},
                                                                                                                       {
                                                                                                                           "email": "kakavelakis@hmu.gr",
                                                                                                                           "id": "5612dd7d45ce1e5962e18959",
                                                                                                                           "name": "George Kakavelakis",
                                                                                                                           "org": "Department of Electronic Engineering, Hellenic Mediterranean University, Greece",
                                                                                                                           "orgid": "61e6994e68962734657381cc"},
                                                                                                                       {
                                                                                                                           "id": "63af8b2884ab04bd7fb6b0a0",
                                                                                                                           "name": "Konstantinos Petridis",
                                                                                                                           "org": "Department of Electronic Engineering, Hellenic Mediterranean University, Greece",
                                                                                                                           "orgid": "61e6994e68962734657381cc"},
                                                                                                                       {
                                                                                                                           "id": "5440905edabfae7d84b8285f",
                                                                                                                           "name": "Michael Graetzel",
                                                                                                                           "org": "Laboratory of Photonics and Interfaces, Institute of Chemical Sciences and Engineering, Ecole Polytechnique Fédérale de Lausanne, 1015, Lausanne, Switzerland."},
                                                                                                                       {
                                                                                                                           "id": "53f4b203dabfaedce564556f",
                                                                                                                           "name": "George Kenanakis",
                                                                                                                           "org": "Institute of Electronic Structure and Laser (IESL), Foundation for Research and Technology - Hellas (FORTH), 70013, Heraklion, Crete, Greece."},
                                                                                                                       {
                                                                                                                           "id": "53f438f2dabfaec22ba99ac7",
                                                                                                                           "name": "Stelios Tzortzakis",
                                                                                                                           "org": "Institute of Electronic Structure and Laser (IESL), Foundation for Research and Technology - Hellas (FORTH), 70013, Heraklion, Crete, Greece."},
                                                                                                                       {
                                                                                                                           "id": "53f45b37dabfaedd74e3ff03",
                                                                                                                           "name": "Maria Kafesaki",
                                                                                                                           "org": "Institute of Electronic Structure and Laser (IESL), Foundation for Research and Technology - Hellas (FORTH), 70013, Heraklion, Crete, Greece."}],
                                                                                                                   "create_time": "2024-05-11T06:06:41.07Z",
                                                                                                                   "doi": "10.1038\u002Fs41598-023-50988-3",
                                                                                                                   "id": "65972a88939a5f4082475440",
                                                                                                                   "issn": "2045-2322",
                                                                                                                   "keywords": [
                                                                                                                       "Perovskite Solar Cells",
                                                                                                                       "Metal-Insulator Transition"],
                                                                                                                   "lang": "en",
                                                                                                                   "num_citation": 0,
                                                                                                                   "title": "Infrared-reflective Ultrathin-Metal-film-based Transparent Electrode with Ultralow Optical Loss for High Efficiency in Solar Cells",
                                                                                                                   "update_times": {
                                                                                                                       "u_a_t": "2024-11-21T23:07:31Z",
                                                                                                                       "u_v_t": "2024-11-21T23:07:31Z"},
                                                                                                                   "urls": [
                                                                                                                       "https:\u002F\u002Fwww.nature.com\u002Farticles\u002Fs41598-023-50988-3"],
                                                                                                                   "venue": {
                                                                                                                       "info": {
                                                                                                                           "name": "SCIENTIFIC REPORTS"},
                                                                                                                       "issue": "1",
                                                                                                                       "volume": "14"},
                                                                                                                   "venue_hhb_id": "5ea556ddedb6e7d53c0373fc",
                                                                                                                   "versions": [
                                                                                                                       {
                                                                                                                           "id": "65972a88939a5f4082475440",
                                                                                                                           "sid": "s41598-023-50988-3",
                                                                                                                           "src": "nature",
                                                                                                                           "vsid": "SCIENTIFIC REPORTS",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "65979520939a5f4082da6d92",
                                                                                                                           "sid": "10.1038\u002Fs41598-023-50988-3",
                                                                                                                           "src": "springernature",
                                                                                                                           "vsid": "41598",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "659acab4939a5f40829187ac",
                                                                                                                           "sid": "148df8021e2c4c1e89766219c2bd6c61",
                                                                                                                           "src": "doaj",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "659bf8cf939a5f408277437b",
                                                                                                                           "sid": "38177236",
                                                                                                                           "src": "pubmed",
                                                                                                                           "vsid": "101563288",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "65d8f4ba939a5f40823e6387",
                                                                                                                           "sid": "W4390579631",
                                                                                                                           "src": "openalex",
                                                                                                                           "vsid": "S196734849",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "666440af01d2a3fbfcc294e4",
                                                                                                                           "sid": "10.1038\u002Fs41598-023-50988-3",
                                                                                                                           "src": "crossref",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "65e88b2b13fb2c6cf6a94b0b",
                                                                                                                           "sid": "WOS:001136960700047",
                                                                                                                           "src": "wos",
                                                                                                                           "vsid": "SCIENTIFIC REPORTS",
                                                                                                                           "year": 2024}],
                                                                                                                   "year": 2024},
                                                                                                               {
                                                                                                                   "abstract": "AbstractAccurately predicting the power conversion efficiency (PCE) in dye‐sensitized solar cells (DSSCs) represents a crucial challenge, one that is pivotal for the high throughput rational design and screening of promising dye sensitizers. This study presents precise, predictive, and interpretable machine learning (ML) models specifically designed for Zn‐porphyrin‐sensitized solar cells. The model leverages theoretically computable, effective, and reusable molecular descriptors (MDs) to address this challenge. The models achieve excellent performance on a “blind test” of 17 newly designed cells, with a mean absolute error (MAE) of 1.02%. Notably, 10 dyes are predicted within a 1% error margin. These results validate the ML models and their importance in exploring uncharted chemical spaces of Zn‐porphyrins. SHAP analysis identifies crucial MDs that align well with experimental observations, providing valuable chemical guidelines for the rational design of dyes in DSSCs. These predictive ML models enable efficient in silico screening, significantly reducing analysis time for photovoltaic cells. Promising Zn‐porphyrin‐based dyes with exceptional PCE are identified, facilitating high‐throughput virtual screening. The prediction tool is publicly accessible at https:\u002F\u002Fai‐meta.chem.ncu.edu.tw\u002Fdsc‐meta.",
                                                                                                                   "authors": [
                                                                                                                       {
                                                                                                                           "name": "Jian-Ming Liao",
                                                                                                                           "org": "Natl Cent Univ, Dept Chem, 300 Zhongda Rd, Taoyuan City 32001, Taiwan"},
                                                                                                                       {
                                                                                                                           "id": "561788ef45ce1e5963dfd075",
                                                                                                                           "name": "Yu-Hsuan Chen"},
                                                                                                                       {
                                                                                                                           "id": "65bfea4e8a47b62219fed8aa",
                                                                                                                           "name": "Hsuan-Wei Lee"},
                                                                                                                       {
                                                                                                                           "id": "560cd02045ce1e59609c436e",
                                                                                                                           "name": "Bo-Cheng Guo"},
                                                                                                                       {
                                                                                                                           "name": "Po-Cheng Su"},
                                                                                                                       {
                                                                                                                           "id": "6524daf955b3f8ac464fcf1c",
                                                                                                                           "name": "Lun-Hong Wang"},
                                                                                                                       {
                                                                                                                           "id": "560bb55a45ce1e596031b1fb",
                                                                                                                           "name": "Nagannagari Masi Reddy"},
                                                                                                                       {
                                                                                                                           "id": "5612404f45cedb33979157c1",
                                                                                                                           "name": "Aswani Yella"},
                                                                                                                       {
                                                                                                                           "name": "Zhao-Jie Zhang",
                                                                                                                           "org": "Natl Cent Univ, Dept Chem, 300 Zhongda Rd, Taoyuan City 32001, Taiwan"},
                                                                                                                       {
                                                                                                                           "name": "Chuan-Yung Chang",
                                                                                                                           "org": "Natl Cent Univ, Dept Chem, 300 Zhongda Rd, Taoyuan City 32001, Taiwan"},
                                                                                                                       {
                                                                                                                           "id": "53f454f9dabfaeee22a2efbd",
                                                                                                                           "name": "Chia-Yuan Chen",
                                                                                                                           "org": "Natl Cent Univ, Dept Chem, 300 Zhongda Rd, Taoyuan City 32001, Taiwan"},
                                                                                                                       {
                                                                                                                           "email": "shaik.zakeer@epfl.ch",
                                                                                                                           "name": "Shaik M. Zakeeruddin"},
                                                                                                                       {
                                                                                                                           "email": "hhtsai@cc.ncu.edu.tw",
                                                                                                                           "id": "563451da45cedb339af906bf",
                                                                                                                           "name": "Hui-Hsu Gavin Tsai",
                                                                                                                           "org": "Natl Cent Univ, Dept Chem, 300 Zhongda Rd, Taoyuan City 32001, Taiwan"},
                                                                                                                       {
                                                                                                                           "email": "cyyeh@dragon.nchu.edu.tw",
                                                                                                                           "name": "Chen-Yu Yeh"},
                                                                                                                       {
                                                                                                                           "id": "5440905edabfae7d84b8285f",
                                                                                                                           "name": "Michael Gratzel"}],
                                                                                                                   "create_time": "2024-09-25T04:12:08.59Z",
                                                                                                                   "doi": "10.1002\u002Fadvs.202407235",
                                                                                                                   "id": "66f31a0f01d2a3fbfcad006d",
                                                                                                                   "keywords": [
                                                                                                                       "design rules",
                                                                                                                       "dye-sensitized solar cells",
                                                                                                                       "high-throughput virtual screening",
                                                                                                                       "interpretable machine learning model",
                                                                                                                       "SHAP"],
                                                                                                                   "lang": "en",
                                                                                                                   "num_citation": 0,
                                                                                                                   "pages": {
                                                                                                                       "end": "e2407235",
                                                                                                                       "start": "e2407235"},
                                                                                                                   "title": "Advanced High-Throughput Rational Design of Porphyrin-Sensitized Solar Cells Using Interpretable Machine Learning",
                                                                                                                   "update_times": {
                                                                                                                       "u_a_t": "2024-11-23T05:05:58Z",
                                                                                                                       "u_v_t": "2024-11-23T05:05:58Z"},
                                                                                                                   "urls": [
                                                                                                                       "https:\u002F\u002Fapi.crossref.org\u002Fworks\u002F10.1002\u002Fadvs.202407235",
                                                                                                                       "http:\u002F\u002Fdx.doi.org\u002F10.1002\u002Fadvs.202407235",
                                                                                                                       "https:\u002F\u002Fonlinelibrary.wiley.com\u002Fdoi\u002F10.1002\u002Fadvs.202407235"],
                                                                                                                   "venue": {
                                                                                                                       "info": {
                                                                                                                           "name": "Advanced science (Weinheim, Baden-Wurttemberg, Germany)"},
                                                                                                                       "issue": "43",
                                                                                                                       "volume": "11"},
                                                                                                                   "versions": [
                                                                                                                       {
                                                                                                                           "id": "66f3f4a201d2a3fbfc4add1a",
                                                                                                                           "sid": "10.1002\u002Fadvs.202407235",
                                                                                                                           "src": "crossref",
                                                                                                                           "vsid": "101664569",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "6711c81501d2a3fbfc65ae13",
                                                                                                                           "sid": "WOS:001318600300001",
                                                                                                                           "src": "wos",
                                                                                                                           "vsid": "ADVANCED SCIENCE",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "673f211bae8580e7ff926721",
                                                                                                                           "sid": "080dc61c38d54a20ad42fc9b254f85f7",
                                                                                                                           "src": "doaj",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "66f31a0f01d2a3fbfcad006d",
                                                                                                                           "sid": "39316380",
                                                                                                                           "src": "pubmed",
                                                                                                                           "vsid": "101664569",
                                                                                                                           "year": 2024}],
                                                                                                                   "year": 2024},
                                                                                                               {
                                                                                                                   "abstract": "The presence of defects at the interface between the perovskite film and the carrier transport layer poses significant challenges to the performance and stability of perovskite solar cells (PSCs). Addressing this issue, we introduce a dual host-guest (DHG) complexation strategy to modulate both the bulk and interfacial properties of FAPbI3-rich PSCs. Through NMR spectroscopy, a synergistic effect of the dual treatment is observed. Additionally, electro-optical characterizations demonstrate that the DHG strategy not only passivates defects but also enhances carrier extraction and transport. Remarkably, employing the DHG strategy yields PSCs with power conversion efficiencies (PCE) of 25.89% (certified at 25.53%). Furthermore, these DHG-modified PSCs exhibit enhanced operational stability, retaining over 96.6% of their initial PCE of 25.55% after 1050 hours of continuous operation under one-sun illumination, which was the highest initial value in the recently reported articles. This work establishes a promising pathway for stabilizing high-efficiency perovskite photovoltaics through supramolecular engineering, marking a significant advancement in the field. The defects at the perovskite\u002Fcarrier transport layer interface pose significant challenges to the performance of perovskite solar cells. Here, the authors introduce a dual host-guest complexation strategy with Cs-crown-ether and ammonium salt, achieving a high PCE of 25.9% with superior stability.",
                                                                                                                   "authors": [
                                                                                                                       {
                                                                                                                           "id": "63c49a81df1d768b3c42bd9b",
                                                                                                                           "name": "Chenxu Zhao",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Lab Photon & Interfaces, Lausanne, Switzerland",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c85c"},
                                                                                                                       {
                                                                                                                           "email": "zwzhou@connect.hku.hk",
                                                                                                                           "id": "63248a79c03fbd5be1f92c2d",
                                                                                                                           "name": "Zhiwen Zhou",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Lab Photon & Interfaces, Lausanne, Switzerland",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c85c"},
                                                                                                                       {
                                                                                                                           "id": "65a43de58a47b62d65913661",
                                                                                                                           "name": "Masaud Almalki",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Lab Photon & Interfaces, Lausanne, Switzerland",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c85c"},
                                                                                                                       {
                                                                                                                           "id": "63156db2cd729caec6371e08",
                                                                                                                           "name": "Michael A. Hope",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Inst Chem Sci & Engn, Lab Magnet Resonance, Lausanne, Switzerland"},
                                                                                                                       {
                                                                                                                           "id": "63797627f789b382be9a53ae",
                                                                                                                           "name": "Jiashang Zhao",
                                                                                                                           "org": "Delft Univ Technol, Dept Chem Engn, Delft, Netherlands",
                                                                                                                           "orgid": "5f71b28a1c455f439fe3c93b"},
                                                                                                                       {
                                                                                                                           "id": "63156daecd729caec63678f9",
                                                                                                                           "name": "Thibaut Gallet",
                                                                                                                           "org": "Univ Luxembourg, Scanning Probe Microscopy Lab, Dept Phys & Mat Sci, Luxembourg, Luxembourg",
                                                                                                                           "orgid": "5f71b3711c455f439fe42edd"},
                                                                                                                       {
                                                                                                                           "id": "62e47bcad9f204418d689b33",
                                                                                                                           "name": "Anurag Krishna",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Lab Photon & Interfaces, Lausanne, Switzerland",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c85c"},
                                                                                                                       {
                                                                                                                           "id": "53f42d3adabfaee1c0a312f4",
                                                                                                                           "name": "Aditya Mishra",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Inst Chem Sci & Engn, Lab Magnet Resonance, Lausanne, Switzerland"},
                                                                                                                       {
                                                                                                                           "id": "53f42e34dabfaee1c0a3e4f9",
                                                                                                                           "name": "Felix T. Eickemeyer",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Lab Photon & Interfaces, Lausanne, Switzerland",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c85c"},
                                                                                                                       {
                                                                                                                           "id": "5430e1f6dabfaecb58732c7f",
                                                                                                                           "name": "Jia Xu",
                                                                                                                           "org": "State Key Laboratory of Alternate Electrical Power System with Renewable Energy Sources, Beijing Key Laboratory of Energy Safety and Clean Utilization, North China Electric Power University, Beijing, P. R. China."},
                                                                                                                       {
                                                                                                                           "id": "5617539945ce1e5963d4b990",
                                                                                                                           "name": "Yingguo Yang",
                                                                                                                           "org": "Fudan Univ, Sch Microelect, Shanghai, Peoples R China",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c861"},
                                                                                                                       {
                                                                                                                           "id": "53f45043dabfaeecd69d3ade",
                                                                                                                           "name": "Shaik M. Zakeeruddin",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Lab Photon & Interfaces, Lausanne, Switzerland",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c85c"},
                                                                                                                       {
                                                                                                                           "id": "53f43504dabfaee1c0a916c1",
                                                                                                                           "name": "Alex Redinger",
                                                                                                                           "org": "Univ Luxembourg, Scanning Probe Microscopy Lab, Dept Phys & Mat Sci, Luxembourg, Luxembourg",
                                                                                                                           "orgid": "5f71b3711c455f439fe42edd"},
                                                                                                                       {
                                                                                                                           "id": "560f84a045ce1e5961c78424",
                                                                                                                           "name": "Tom J. Savenije",
                                                                                                                           "org": "Delft Univ Technol, Dept Chem Engn, Delft, Netherlands",
                                                                                                                           "orgid": "5f71b28a1c455f439fe3c93b"},
                                                                                                                       {
                                                                                                                           "id": "6145b6776750f861c0fc5b0b",
                                                                                                                           "name": "Lyndon Emsley",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Inst Chem Sci & Engn, Lab Magnet Resonance, Lausanne, Switzerland"},
                                                                                                                       {
                                                                                                                           "email": "jianxiyao@ncepu.edu.cn",
                                                                                                                           "id": "542c04eedabfae2b4e1cef7a",
                                                                                                                           "name": "Jianxi Yao",
                                                                                                                           "org": "State Key Laboratory of Alternate Electrical Power System with Renewable Energy Sources, Beijing Key Laboratory of Energy Safety and Clean Utilization, North China Electric Power University, Beijing, P. R. China. jianxiyao@ncepu.edu.cn."},
                                                                                                                       {
                                                                                                                           "email": "hzhangioe@fudan.edu.cn",
                                                                                                                           "id": "562f947345cedb33997160c2",
                                                                                                                           "name": "Hong Zhang",
                                                                                                                           "org": "State Key Laboratory of Photovoltaic Science and Technology, Shanghai Frontiers Science Research Base of Intelligent Optoelectronics and Perception, Institute of Optoelectronics, Fudan University, Shanghai, China. hzhangioe@fudan.edu.cn."},
                                                                                                                       {
                                                                                                                           "id": "5440905edabfae7d84b8285f",
                                                                                                                           "name": "Michael Graetzel",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Lab Photon & Interfaces, Lausanne, Switzerland",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c85c"}],
                                                                                                                   "create_time": "2024-08-22T19:31:05.897Z",
                                                                                                                   "doi": "10.1038\u002Fs41467-024-51550-z",
                                                                                                                   "id": "66c6479001d2a3fbfca0edf0",
                                                                                                                   "lang": "en",
                                                                                                                   "num_citation": 0,
                                                                                                                   "title": "Stabilization of Highly Efficient Perovskite Solar Cells with a Tailored Supramolecular Interface.",
                                                                                                                   "update_times": {
                                                                                                                       "u_a_t": "2024-11-22T00:10:39Z",
                                                                                                                       "u_v_t": "2024-11-22T00:10:39Z"},
                                                                                                                   "urls": [
                                                                                                                       "https:\u002F\u002Fwww.ncbi.nlm.nih.gov\u002Fpubmed\u002F39164254"],
                                                                                                                   "venue": {
                                                                                                                       "info": {
                                                                                                                           "name": "NATURE COMMUNICATIONS"},
                                                                                                                       "issue": "1",
                                                                                                                       "volume": "15"},
                                                                                                                   "versions": [
                                                                                                                       {
                                                                                                                           "id": "66c6479001d2a3fbfca0edf0",
                                                                                                                           "sid": "39164254",
                                                                                                                           "src": "pubmed",
                                                                                                                           "vsid": "NATURE COMMUNICATIONS",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "66cb1b9c01d2a3fbfcc073bb",
                                                                                                                           "sid": "e230ef10454b44fab23c80d9e7fc2fad",
                                                                                                                           "src": "doaj",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "66d5a29d01d2a3fbfc7e69af",
                                                                                                                           "sid": "s41467-024-51550-z",
                                                                                                                           "src": "nature",
                                                                                                                           "vsid": "ncomms",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "6738dd6d01d2a3fbfc8b6b62",
                                                                                                                           "sid": "W4401729342",
                                                                                                                           "src": "openalex",
                                                                                                                           "vsid": "S64187185",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "66ec652c01d2a3fbfc41ba67",
                                                                                                                           "sid": "WOS:001295167000011",
                                                                                                                           "src": "wos",
                                                                                                                           "vsid": "NATURE COMMUNICATIONS",
                                                                                                                           "year": 2024}],
                                                                                                                   "year": 2024},
                                                                                                               {
                                                                                                                   "abstract": "The cover image is based on the Review Updates on Hydrogen Value Chain: A Strategic Roadmap by Julio Garcia-Navarro et al., https:\u002F\u002Fdoi.org\u002F10.1002\u002Fgch2.202300073 Image Credit: Júlio Arvellos",
                                                                                                                   "authors": [
                                                                                                                       {
                                                                                                                           "id": "63afb54684ab04bd7fbbd39d",
                                                                                                                           "name": "Julio Cesar Garcia-Navarro",
                                                                                                                           "org": "New Energy Coalition",
                                                                                                                           "orgid": "61e6a0956896273465749734"},
                                                                                                                       {
                                                                                                                           "name": "Mark A. Isaacs",
                                                                                                                           "org": "Research Complex at Harwell",
                                                                                                                           "orgid": "61e69dda6896273465742b47"},
                                                                                                                       {
                                                                                                                           "id": "562bb42145cedb3398b0c0d6",
                                                                                                                           "name": "Marco Favaro",
                                                                                                                           "org": "Helmholtz-Zentrum Berlin für Materialien und Energie",
                                                                                                                           "orgid": "5f71b2bc1c455f439fe3de22"},
                                                                                                                       {
                                                                                                                           "id": "62e445cad9f204418d67a49e",
                                                                                                                           "name": "Dan Ren",
                                                                                                                           "org": "Xi'an Jiaotong University",
                                                                                                                           "orgid": "5f71b2b81c455f439fe3dc31"},
                                                                                                                       {
                                                                                                                           "name": "Wee‐Jun Ong",
                                                                                                                           "org": "Xiamen University Malaysia",
                                                                                                                           "orgid": "5f71b6c71c455f439fe5a5cd"},
                                                                                                                       {
                                                                                                                           "id": "5440905edabfae7d84b8285f",
                                                                                                                           "name": "Michaël Grätzel",
                                                                                                                           "org": "École Polytechnique Fédérale de Lausanne",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c85c"},
                                                                                                                       {
                                                                                                                           "id": "62e4bfecd9f204418d721d8e",
                                                                                                                           "name": "Pablo Jiménez‐Calvo",
                                                                                                                           "org": "Max Planck Institute of Colloids and Interfaces",
                                                                                                                           "orgid": "5f71b2b41c455f439fe3dac3"}],
                                                                                                                   "create_time": "2024-09-20T00:54:02.096Z",
                                                                                                                   "doi": "10.1002\u002Fgch2.202470085",
                                                                                                                   "id": "66e9b62801d2a3fbfc5768bc",
                                                                                                                   "issn": "2056-6646",
                                                                                                                   "lang": "en",
                                                                                                                   "num_citation": 0,
                                                                                                                   "title": "Updates on Hydrogen Value Chain: A Strategic Roadmap (global Challenges 6\u002F2024)",
                                                                                                                   "update_times": {
                                                                                                                       "u_a_t": "2024-09-20T00:54:02.096Z",
                                                                                                                       "u_v_t": "2024-09-20T00:54:02.096Z"},
                                                                                                                   "urls": [
                                                                                                                       "https:\u002F\u002Fopenalex.org\u002FW4399527594",
                                                                                                                       "https:\u002F\u002Fdoi.org\u002F10.1002\u002Fgch2.202470085"],
                                                                                                                   "venue": {
                                                                                                                       "info": {
                                                                                                                           "name": "Global challenges",
                                                                                                                           "publisher": "Wiley"},
                                                                                                                       "issue": "6",
                                                                                                                       "volume": "8"},
                                                                                                                   "versions": [
                                                                                                                       {
                                                                                                                           "id": "66e9b62801d2a3fbfc5768bc",
                                                                                                                           "sid": "W4399527594",
                                                                                                                           "src": "openalex",
                                                                                                                           "vsid": "S4210214099",
                                                                                                                           "year": 2024}],
                                                                                                                   "year": 2024},
                                                                                                               {
                                                                                                                   "abstract": "Abstract Interfacial space charges significantly influence transport and recombination of charge carriers in optoelectronic devices. Due to the mixed ionic‐electronic conducting properties of halide perovskites, not only electronic effects, but also ionic interactions at their interfaces need to be considered in the analysis of space charges. Understanding of these interactions and their control is currently missing. This study elucidates the ionic effects on space charge formation at the interface between methylammonium lead iodide (MAPI) and alumina, and its modulation through surface modification using organic molecules. Embedding insulating alumina nanoparticles within MAPI films leads to enhancement of the electronic conductivity. This effect is consistent with the formation of an interfacial inversion layer in MAPI and can only be explained on the basis of ionic interactions. Such an effect is attenuated by surface modification of the oxide via the chemisorption of organic molecules. Finally, the same trend is observed in solar cells, where reducing the potential of the distributed space charges within the composite active layer improves device performance. These findings emphasize the necessity of taking into account ionic interactions to control the space charge formation at interfaces involving mixed ionic‐electronic conductors, an essential aspect in the performance optimization of halide perovskite‐based devices.",
                                                                                                                   "authors": [
                                                                                                                       {
                                                                                                                           "id": "637998f3f789b382be9b4869",
                                                                                                                           "name": "Mina Jung",
                                                                                                                           "org": "Max Planck Inst Solid State Res, Heisenbergstr 1, D-70569 Stuttgart, Germany"},
                                                                                                                       {
                                                                                                                           "id": "65a43de58a47b62d65913661",
                                                                                                                           "name": "Masaud Almalki",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne EPFL, Inst Chem Sci & Engn, Lab Photon & Interfaces, CH-1015 Lausanne, Switzerland",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c85c"},
                                                                                                                       {
                                                                                                                           "id": "5440905edabfae7d84b8285f",
                                                                                                                           "name": "Michael Graetzel",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne EPFL, Inst Chem Sci & Engn, Lab Photon & Interfaces, CH-1015 Lausanne, Switzerland",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c85c"},
                                                                                                                       {
                                                                                                                           "email": "d.moia@fkf.mpg.de",
                                                                                                                           "id": "5631a8d145cedb3399ec40b3",
                                                                                                                           "name": "Davide Moia",
                                                                                                                           "org": "Max Planck Inst Solid State Res, Heisenbergstr 1, D-70569 Stuttgart, Germany"},
                                                                                                                       {
                                                                                                                           "id": "5602281245cedb3395f20f1a",
                                                                                                                           "name": "Joachim Maier",
                                                                                                                           "org": "Max Planck Inst Solid State Res, Heisenbergstr 1, D-70569 Stuttgart, Germany"}],
                                                                                                                   "create_time": "2024-05-28T12:45:01.128Z",
                                                                                                                   "doi": "10.1002\u002Fadmi.202300874",
                                                                                                                   "id": "65e8898613fb2c6cf6a5f796",
                                                                                                                   "issn": "2196-7350",
                                                                                                                   "keywords": [
                                                                                                                       "halide perovskites",
                                                                                                                       "interfaces",
                                                                                                                       "mixed ionic-electronic conductors",
                                                                                                                       "mobile ions",
                                                                                                                       "solid state ionics",
                                                                                                                       "space charge effects"],
                                                                                                                   "lang": "en",
                                                                                                                   "num_citation": 0,
                                                                                                                   "title": "Modulation of Ionically Generated Space Charge Effects at Hybrid Perovskite and Oxide Interfaces Via Surface Modification",
                                                                                                                   "update_times": {
                                                                                                                       "u_a_t": "2024-11-26T00:48:20Z",
                                                                                                                       "u_v_t": "2024-11-26T00:48:20Z"},
                                                                                                                   "urls": [
                                                                                                                       "http:\u002F\u002Fwww.webofknowledge.com\u002F"],
                                                                                                                   "venue": {
                                                                                                                       "info": {
                                                                                                                           "name": "ADVANCED MATERIALS INTERFACES"},
                                                                                                                       "issue": "11",
                                                                                                                       "volume": "11"},
                                                                                                                   "versions": [
                                                                                                                       {
                                                                                                                           "id": "65e8898613fb2c6cf6a5f796",
                                                                                                                           "sid": "WOS:001157900900001",
                                                                                                                           "src": "wos",
                                                                                                                           "vsid": "ADVANCED MATERIALS INTERFACES",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "661d162613fb2c6cf6c88fed",
                                                                                                                           "sid": "f706ec4c7ea34d229f3fb4de57afdc13",
                                                                                                                           "src": "doaj",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "6664094701d2a3fbfc675687",
                                                                                                                           "sid": "10.1002\u002Fadmi.202300874",
                                                                                                                           "src": "crossref",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "660d49ea13fb2c6cf6011225",
                                                                                                                           "sid": "W4391691205",
                                                                                                                           "src": "openalex",
                                                                                                                           "vsid": "S2764385675",
                                                                                                                           "year": 2024}],
                                                                                                                   "year": 2024},
                                                                                                               {
                                                                                                                   "abstract": "The systematic advances in the power conversion efficiency (PCE) and stability of perovskite solar cells (PSCs) have been driven by the developments of perovskite materials, electron transport layer (ETL) materials, and interfacial passivation between the relevant layers. While zinc oxide (ZnO) is a promising ETL in thin film photovoltaics, it is still highly desirable to develop novel synthetic methods that allow both fine‐tuning the versatility of ZnO nanomaterials and improving the ZnO\u002Fperovskite interface. Among various inorganic and organic additives, zwitterions have been effectively utilized to passivate the perovskite films. In this vein, we develop novel, well‐characterized betaine‐coated ZnO QDs and use them as an ETL in the planar n‐i‐p PSC architecture, combining the ZnO QDs‐based ETL with the ZnO\u002Fperovskite interface passivation by a series of ammonium halides (NH4X, where X = F, Cl, Br). The champion device with the NH4F passivation achieves one of the highest performances reported for ZnO‐based PSCs, exhibiting a maximum PCE of ~22% with a high fill factor of 80.3% and competitive stability, retaining ~78% of its initial PCE under 1 Sun illumination with maximum power tracking for 250 h.",
                                                                                                                   "authors": [
                                                                                                                       {
                                                                                                                           "id": "6403e1daadc7183bcb7ef1e6",
                                                                                                                           "name": "Rashmi Runjhun",
                                                                                                                           "org": "Polish Acad Sci, Inst Phys Chem, Kasprzaka 44-52, PL-01224 Warsaw, Poland",
                                                                                                                           "orgid": "5f71b2c51c455f439fe3e24c"},
                                                                                                                       {
                                                                                                                           "id": "6378cd9ad49364c9ac99eb91",
                                                                                                                           "name": "Essa A. Alharbi",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Inst Chem Sci & Engn, Sch Basic Sci, Lab Photon & Interfaces, CH-1015 Lausanne, Switzerland",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c85c"},
                                                                                                                       {
                                                                                                                           "name": "Zygmunt Druzynski",
                                                                                                                           "org": "Warsaw Univ Technol, Fac Chem, Noakowskiego 3, PL-00664 Warsaw, Poland",
                                                                                                                           "orgid": "5f71b2bc1c455f439fe3ddfc"},
                                                                                                                       {
                                                                                                                           "id": "62e47bcad9f204418d689b33",
                                                                                                                           "name": "Anurag Krishna",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Inst Chem Sci & Engn, Sch Basic Sci, Lab Photon & Interfaces, CH-1015 Lausanne, Switzerland",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c85c"},
                                                                                                                       {
                                                                                                                           "id": "62e47bcad9f204418d689b4c",
                                                                                                                           "name": "Malgorzata Wolska-Pietkiewicz",
                                                                                                                           "org": "Warsaw Univ Technol, Fac Chem, Noakowskiego 3, PL-00664 Warsaw, Poland",
                                                                                                                           "orgid": "5f71b2bc1c455f439fe3ddfc"},
                                                                                                                       {
                                                                                                                           "id": "652f33be712b454cfa46983a",
                                                                                                                           "name": "Viktor Skorjanc",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Inst Chem Sci & Engn, Sch Basic Sci, Lab Photon & Interfaces, CH-1015 Lausanne, Switzerland",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c85c"},
                                                                                                                       {
                                                                                                                           "id": "62e4be86d9f204418d71a66d",
                                                                                                                           "name": "Thomas P. Baumeler",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Inst Chem Sci & Engn, Sch Basic Sci, Lab Photon & Interfaces, CH-1015 Lausanne, Switzerland",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c85c"},
                                                                                                                       {
                                                                                                                           "id": "5612dd7d45ce1e5962e18959",
                                                                                                                           "name": "George Kakavelakis",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Inst Chem Sci & Engn, Sch Basic Sci, Lab Photon & Interfaces, CH-1015 Lausanne, Switzerland",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c85c"},
                                                                                                                       {
                                                                                                                           "id": "53f42e34dabfaee1c0a3e4f9",
                                                                                                                           "name": "Felix Eickemeyer",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Inst Chem Sci & Engn, Sch Basic Sci, Lab Photon & Interfaces, CH-1015 Lausanne, Switzerland",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c85c"},
                                                                                                                       {
                                                                                                                           "id": "53f3520adabfae4b3494c32b",
                                                                                                                           "name": "Mounir Mensi",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Inst Chem Sci & Engn, CH-1951 Sion, Switzerland"},
                                                                                                                       {
                                                                                                                           "id": "53f45043dabfaeecd69d3ade",
                                                                                                                           "name": "Shaik M. Zakeeruddin",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Inst Chem Sci & Engn, Sch Basic Sci, Lab Photon & Interfaces, CH-1015 Lausanne, Switzerland",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c85c"},
                                                                                                                       {
                                                                                                                           "email": "michael.graetzel@epfl.ch",
                                                                                                                           "id": "5440905edabfae7d84b8285f",
                                                                                                                           "name": "Michael Graetzel",
                                                                                                                           "org": "Ecole Polytech Fed Lausanne, Inst Chem Sci & Engn, Sch Basic Sci, Lab Photon & Interfaces, CH-1015 Lausanne, Switzerland",
                                                                                                                           "orgid": "5f71b2881c455f439fe3c85c"},
                                                                                                                       {
                                                                                                                           "email": "janusz.lewinski@pw.edu.pl",
                                                                                                                           "id": "53f42d7ddabfaeb22f40986b",
                                                                                                                           "name": "Janusz Lewinski",
                                                                                                                           "org": "Polish Acad Sci, Inst Phys Chem, Kasprzaka 44-52, PL-01224 Warsaw, Poland",
                                                                                                                           "orgid": "5f71b2c51c455f439fe3e24c"}],
                                                                                                                   "create_time": "2024-04-09T13:09:11.51Z",
                                                                                                                   "doi": "10.1002\u002Feem2.12720",
                                                                                                                   "id": "660cf46413fb2c6cf61d9e3a",
                                                                                                                   "keywords": [
                                                                                                                       "interface passivations",
                                                                                                                       "perovskites",
                                                                                                                       "quantum dots",
                                                                                                                       "solar cells",
                                                                                                                       "zinc oxide",
                                                                                                                       "zwitterions"],
                                                                                                                   "lang": "en",
                                                                                                                   "num_citation": 0,
                                                                                                                   "title": "High-Performance Perovskite Solar Cells with Zwitterion-Capped-ZnO Quantum Dots As Electron Transport Layer and NH4X (X = F, Cl, Br) Assisted Interfacial Engineering",
                                                                                                                   "update_times": {
                                                                                                                       "u_a_t": "2024-11-22T00:26:29Z",
                                                                                                                       "u_v_t": "2024-11-22T00:26:29Z"},
                                                                                                                   "urls": [
                                                                                                                       "https:\u002F\u002Fapi.crossref.org\u002Fworks\u002F10.1002\u002Feem2.12720",
                                                                                                                       "http:\u002F\u002Fdx.doi.org\u002F10.1002\u002Feem2.12720",
                                                                                                                       "https:\u002F\u002Fonlinelibrary.wiley.com\u002Fdoi\u002F10.1002\u002Feem2.12720"],
                                                                                                                   "venue": {
                                                                                                                       "info": {
                                                                                                                           "name": "ENERGY & ENVIRONMENTAL MATERIALS"},
                                                                                                                       "issue": "5",
                                                                                                                       "volume": "7"},
                                                                                                                   "venue_hhb_id": "5ebab7c7edb6e7d53c103d5b",
                                                                                                                   "versions": [
                                                                                                                       {
                                                                                                                           "id": "6664b70e01d2a3fbfc7bd784",
                                                                                                                           "sid": "10.1002\u002Feem2.12720",
                                                                                                                           "src": "crossref",
                                                                                                                           "vsid": "ENERGY & ENVIRONMENTAL MATERIALS",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "6668f94501d2a3fbfc267803",
                                                                                                                           "sid": "W4392375279",
                                                                                                                           "src": "openalex",
                                                                                                                           "vsid": "S4210219471",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "66f597c301d2a3fbfc16a82c",
                                                                                                                           "sid": "nyyhjcl-e202405031",
                                                                                                                           "src": "wf",
                                                                                                                           "vsid": "nyyhjcl-e",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "660cf46413fb2c6cf61d9e3a",
                                                                                                                           "sid": "WOS:001179320500001",
                                                                                                                           "src": "wos",
                                                                                                                           "vsid": "ENERGY & ENVIRONMENTAL MATERIALS",
                                                                                                                           "year": 2024}],
                                                                                                                   "year": 2024}],
                                                                                               "profilePubsTotal": 1696,
                                                                                               "profilePatentsPage": 0,
                                                                                               "profilePatents": None,
                                                                                               "profilePatentsTotal": None,
                                                                                               "profilePatentsEnd": False,
                                                                                               "profileProjectsPage": 1,
                                                                                               "profileProjects": {
                                                                                                   "success": True,
                                                                                                   "msg": "",
                                                                                                   "data": None,
                                                                                                   "log_id": "2pQWyWO2djgAJJEcgU7wF9eu3yU"},
                                                                                               "profileProjectsTotal": 0,
                                                                                               "newInfo": None,
                                                                                               "checkDelPubs": []}}

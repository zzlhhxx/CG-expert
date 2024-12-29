import time

from until.sql_tools import mysql_db_conn, getStrAsMD5
from until.config import he

from lxml import etree
from urllib.parse import unquote
import random
import requests
import json
import os



import requests
params = {
    'a': 'getPerson__personapi.get___',
}

json_data = [
    {
        'action': 'personapi.get',
        'parameters': {
            'ids': [
                '53f43464dabfaee4dc76fc7c',
            ],
        },
        'schema': {
            'person': [
                'id',
                'name',
                'name_zh',
                'avatar',
                'num_view',
                'is_follow',
                'work',
                'work_zh',
                'hide',
                'nation',
                'language',
                'bind',
                'acm_citations',
                'links',
                'educations',
                'tags',
                'tags_zh',
                'num_view',
                'num_follow',
                'is_upvoted',
                'num_upvoted',
                'is_downvoted',
                'is_lock',
                {
                    'indices': [
                        'hindex',
                        'gindex',
                        'pubs',
                        'citations',
                        'newStar',
                        'risingStar',
                        'activity',
                        'diversity',
                        'sociability',
                    ],
                },
                {
                    'profile': [
                        'position',
                        'position_zh',
                        'affiliation',
                        'affiliation_zh',
                        'work',
                        'work_zh',
                        'gender',
                        'lang',
                        'homepage',
                        'phone',
                        'email',
                        'fax',
                        'bio',
                        'bio_zh',
                        'edu',
                        'edu_zh',
                        'address',
                        'note',
                        'homepage',
                        'title',
                        'titles',
                    ],
                },
            ],
        },
    },
]

response = requests.post('https://apiv2.aminer.cn/magic', params=params, data=json.dumps(json_data))
print(response.text)

a = {"global": {"collapsed": false, "preventRender": false, "isCompanyIp": false}, "profile": {"transitionState": false,
                                                                                               "profile": {
                                                                                                   "avatar": "https:\u002F\u002Fstatic.aminer.cn\u002Fupload\u002Favatar\u002F255\u002F820\u002F174\u002F53f43464dabfaee4dc76fc7c_1.jpg",
                                                                                                   "bind": false,
                                                                                                   "id": "53f43464dabfaee4dc76fc7c",
                                                                                                   "indices": {
                                                                                                       "activity": 386.9494,
                                                                                                       "citations": 42184,
                                                                                                       "diversity": 3.4398,
                                                                                                       "gindex": 200,
                                                                                                       "hindex": 111,
                                                                                                       "newStar": 52.3072,
                                                                                                       "pubs": 447,
                                                                                                       "risingStar": 52.3072,
                                                                                                       "sociability": 6.8134},
                                                                                                   "links": {"gs": {
                                                                                                       "type": "gs",
                                                                                                       "url": "https:\u002F\u002Fscholar.google.com.hk\u002Fcitations?user=OmC5JowAAAAJ&hl=zh-CN&oi=sra"},
                                                                                                             "resource": {
                                                                                                                 "resource_link": [
                                                                                                                     {
                                                                                                                         "id": "hp",
                                                                                                                         "url": "https:\u002F\u002Fchem.xmu.edu.cn\u002Finfo\u002F1416\u002F1236.htm"},
                                                                                                                     {
                                                                                                                         "id": "dblp",
                                                                                                                         "url": ""}]}},
                                                                                                   "name": "Nanfeng Zheng",
                                                                                                   "name_zh": "郑南峰",
                                                                                                   "num_followed": 0,
                                                                                                   "num_upvoted": 0,
                                                                                                   "num_viewed": 861,
                                                                                                   "profile": {
                                                                                                       "address": "福建省厦门市思明南路422号厦门大学化学化工学院卢嘉锡楼328室",
                                                                                                       "affiliation": "College of Chemistry and Chemical Engineering, Xiamen University",
                                                                                                       "affiliation_zh": "厦门大学化学化工学院",
                                                                                                       "bio": "",
                                                                                                       "bio_zh": "主要从事表界面配位化学研究，致力于在分子水平上理解金属纳米材料化学性能调控的本质。针对金属表界面化学研究的长期挑战，在发展金属表界面模型材料构筑新方法的基础上，破解典型金属-有机界面和金属-载体界面的分子层面结构，研究无机\u002F有机配位小分子修饰通过形成定向界面电子转移和特异界面空间效应实现对金属纳米材料催化和防腐性能精准控制的规律，并开发具有应用价值的高选择性催化和铜防腐新技术。担任国家重点研发计划项目首席科学家，积极推动表界面配位化学基础研究到实际应用的全链条化。部分催化剂已被工业应用于重要精细化工品的绿色生产，源头上实现污染物大幅减排；发展的铜抗氧化防腐表面配位原创方法正在形成可替代银浆的铜浆技术。",
                                                                                                       "edu": "",
                                                                                                       "edu_zh": "1994.9-1998.7 厦门大学化学系，本科学生\u003Cbr\u003E2001.9-2005.6 美国加州大学河滨分校，博士生",
                                                                                                       "email": "\u002Fmagic?W3siYWN0aW9uIjogInBlcnNvbi5UZXh0VG9JbWFnZSIsInBhcmFtZXRlcnMiOnsiaWRzIjogWyJlNkhzcjFoVVBzN1hWT1RydWUrb05ObEN2bE5KanFFOFZScmZTSDk1aDlScVlRPT0iXX19XQ==",
                                                                                                       "fax": "（0592）2183047",
                                                                                                       "gender": "male",
                                                                                                       "homepage": "https:\u002F\u002Fchem.xmu.edu.cn\u002Finfo\u002F1416\u002F1236.htm",
                                                                                                       "lang": "chinese",
                                                                                                       "note": "主页论文已添加。（厦门大学能源材料化学协同创新中心主页：http:\u002F\u002F2011-ichem.xmu.edu.cn\u002Fmem.asp?classid=73&ca=3&id=870页面论文已加）\u003Cbr\u003E固体表面物理化学国家重点实验室主页：https:\u002F\u002Fpcss.xmu.edu.cn\u002Finfo\u002F1017\u002F1855.htm",
                                                                                                       "phone": "（0592）2186821",
                                                                                                       "position": "Professor",
                                                                                                       "position_zh": "教授",
                                                                                                       "work": "",
                                                                                                       "work_zh": "2005.8-2007.7 加州大学圣芭芭拉分校，博士后\u003Cbr\u003E2005-2007年，美国加州大学圣芭芭拉分校Prof. Galen D. Stucky课题组担任研究助理\u003Cbr\u003E2007.8-至今 厦门大学教授\u003Cbr\u003E厦门大学特聘教授\u003Cbr\u003E嘉庚创新实验室常务副主任\u003Cbr\u003E国家地方纳米材料制备技术工程研究中心主任"},
                                                                                                   "tags": ["Palladium",
                                                                                                            "Heterogeneous Catalysis",
                                                                                                            "Catalysis",
                                                                                                            "Nanoparticles",
                                                                                                            "Noble Metal Nanoclusters",
                                                                                                            "Nanoclusters",
                                                                                                            "Nanocrystals",
                                                                                                            "Cluster Compounds",
                                                                                                            "Perovskite Solar Cells",
                                                                                                            "Selective Hydrogenation",
                                                                                                            "Noble Metal",
                                                                                                            "Platinum",
                                                                                                            "Microporous Materials",
                                                                                                            "Hydrogenation",
                                                                                                            "Photothermal Therapy",
                                                                                                            "Electrocatalysis",
                                                                                                            "Science",
                                                                                                            "Multidisciplinary",
                                                                                                            "Humanities And Social Sciences",
                                                                                                            "Chirality"],
                                                                                                   "tags_score": [22,
                                                                                                                  15,
                                                                                                                  14,
                                                                                                                  14,
                                                                                                                  14,
                                                                                                                  13,
                                                                                                                  12,
                                                                                                                  12,
                                                                                                                  12,
                                                                                                                  12,
                                                                                                                  11,
                                                                                                                  11,
                                                                                                                  10,
                                                                                                                  10, 9,
                                                                                                                  9, 9,
                                                                                                                  9, 9,
                                                                                                                  9],
                                                                                                   "tags_zh": ["钯",
                                                                                                               "润滑剂",
                                                                                                               "铂",
                                                                                                               "尺寸选择性催化",
                                                                                                               "熔合",
                                                                                                               "纳米晶体",
                                                                                                               "测试方法",
                                                                                                               "中空核壳结构",
                                                                                                               "一氧化碳",
                                                                                                               "波分设备",
                                                                                                               "催化氢化",
                                                                                                               "形貌控制",
                                                                                                               "聚氯乙烯",
                                                                                                               "反相胶束",
                                                                                                               "多功能纳米催化剂",
                                                                                                               "核壳结构"]},
                                                                                               "profileID": "53f43464dabfaee4dc76fc7c",
                                                                                               "profilePubsPage": 1,
                                                                                               "profilePubs": [{
                                                                                                                   "abstract": "Chirality is pervasive in nature, yet chiral separation continues to be a real challenge. Herein we report the synthesis and structure of [Pd4S2(dppm)3(CNtBu)2][H(OAc)2]2 (abbre. Pd4S2, HOAc = acetic acid), with an intrinsically chiral Pd-S core. The as-prepared clusters are racemates crystallized in the centric space group P21\u002Fn or as twins of acentric space groups P43212 and P41212, both with co-crystallized acetic acid molecules. Surprisingly, when re-crystallized from glacial acetic acid, optically pure enantiomeric crystals of P43212 or P41212 were obtained simultaneously, with the same amount in one pot. In this regard, glacial acetic acid functions both as a recrystallization solvent and as a resolution agent. It also effectively eliminates twinning. This unexpected finding suggests an easy and economical way to separate a racemic mixture into enantiomers which may find applications in chiral separation technologies. Glacial acetic acid as a resolution solvent for the intrinsically chiral Pd-S nanocluster [Pd4S2(dppm)3(CNtBu)2]2+ is reported, which may find applications in chiral separation technologies.",
                                                                                                                   "authors": [
                                                                                                                       {
                                                                                                                           "id": "6530f8198a47b6492316e106",
                                                                                                                           "name": "Hongwen Deng"},
                                                                                                                       {
                                                                                                                           "name": "Peng Yuan"},
                                                                                                                       {
                                                                                                                           "name": "Kejie Lao"},
                                                                                                                       {
                                                                                                                           "name": "Qijun Fu"},
                                                                                                                       {
                                                                                                                           "email": "boonkteo@xmu.edu.cn",
                                                                                                                           "name": "Boon K. Teo"},
                                                                                                                       {
                                                                                                                           "email": "nfzheng@xmu.edu.cn",
                                                                                                                           "id": "53f43464dabfaee4dc76fc7c",
                                                                                                                           "name": "Nanfeng Zheng"}],
                                                                                                                   "create_time": "2024-10-10T18:50:07.954Z",
                                                                                                                   "doi": "10.1039\u002Fd4qi01944j",
                                                                                                                   "id": "6707ae6601d2a3fbfc72f5d6",
                                                                                                                   "issn": "2052-1553",
                                                                                                                   "lang": "en",
                                                                                                                   "num_citation": 0,
                                                                                                                   "title": "Glacial Acetic Acid As a Resolution Solvent for Growing Enantiopure Crystals from Racemic Mixtures",
                                                                                                                   "update_times": {
                                                                                                                       "u_a_t": "2024-11-21T21:33:53Z",
                                                                                                                       "u_v_t": "2024-11-21T21:33:53Z"},
                                                                                                                   "urls": [
                                                                                                                       "https:\u002F\u002Fapi.crossref.org\u002Fworks\u002F10.1039\u002Fd4qi01944j",
                                                                                                                       "http:\u002F\u002Fdx.doi.org\u002F10.1039\u002Fd4qi01944j",
                                                                                                                       "http:\u002F\u002Fpubs.rsc.org\u002Fen\u002FContent\u002FArticleLanding\u002F2024\u002FQI\u002FD4QI01944J"],
                                                                                                                   "venue": {
                                                                                                                       "info": {
                                                                                                                           "name": "INORGANIC CHEMISTRY FRONTIERS"}},
                                                                                                                   "versions": [
                                                                                                                       {
                                                                                                                           "id": "6707ae6601d2a3fbfc72f5d6",
                                                                                                                           "sid": "10.1039\u002Fd4qi01944j",
                                                                                                                           "src": "crossref",
                                                                                                                           "vsid": "INORGANIC CHEMISTRY FRONTIERS",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "673f2240ae8580e7ff9c1ebb",
                                                                                                                           "sid": "WOS:001334699200001",
                                                                                                                           "src": "wos",
                                                                                                                           "vsid": "INORGANIC CHEMISTRY FRONTIERS",
                                                                                                                           "year": 2024}],
                                                                                                                   "year": 2024},
                                                                                                               {
                                                                                                                   "abstract": "Although X-ray diffraction (XRD) technology has played an essential role in studying the lattice strain of perovskite solar cells (PSCs), accurate construction of the relationship between strains and PSC performance remains challenging due to its limitations. This study investigates the spatial strain distributions of perovskite films on electron transport layers (ETLs) with different surface free energies (γss) through confocal micro-Raman spectroscopy (CMRS) mapping and XRD technology. Results showed that CMRS mapping could more effectively reflect the distribution and size of spatial strain. Uniformed spatial strain with larger grain and preferred orientations can be realized over substrates with optimized γs, corresponding to recombination suppression and interfacial carrier extraction enhancement and significantly reducing open-circuit voltage (VOC) deficits. Optimized PSCs achieve the power conversion efficiency (PCE) of 24.64% and demonstrate excellent compatibility toward large-area or flexible applications, with 20.66% and 22.13% PCEs based on perovskite mini-module and flexible PSCs, respectively.",
                                                                                                                   "authors": [
                                                                                                                       {
                                                                                                                           "id": "640521777691d561fb484a16",
                                                                                                                           "name": "Qiu Xiong",
                                                                                                                           "org": "State Key Laboratory of Structural Chemistry, Fujian Institute of Research on the Structure of Matter, Chinese Academy of Sciences, Fuzhou 350002, China",
                                                                                                                           "orgid": "5f71b29f1c455f439fe3d25c"},
                                                                                                                       {
                                                                                                                           "id": "5609335745ce1e595f68793e",
                                                                                                                           "name": "Xiaofeng Huang",
                                                                                                                           "org": "State Key Laboratory for Physical Chemistry of Solid Surfaces, College of Chemistry and Chemical Engineering, Xiamen University, Xiamen 361005, China",
                                                                                                                           "orgid": "5f71b2bd1c455f439fe3deb7"},
                                                                                                                       {
                                                                                                                           "id": "56cb188ec35f4f3c65650bc4",
                                                                                                                           "name": "Can Wang",
                                                                                                                           "org": "State Key Laboratory of Structural Chemistry, Fujian Institute of Research on the Structure of Matter, Chinese Academy of Sciences, Fuzhou 350002, China",
                                                                                                                           "orgid": "5f71b29f1c455f439fe3d25c"},
                                                                                                                       {
                                                                                                                           "id": "56cb18afc35f4f3c6565b9f6",
                                                                                                                           "name": "Qin Zhou",
                                                                                                                           "org": "State Key Laboratory of Structural Chemistry, Fujian Institute of Research on the Structure of Matter, Chinese Academy of Sciences, Fuzhou 350002, China",
                                                                                                                           "orgid": "5f71b29f1c455f439fe3d25c"},
                                                                                                                       {
                                                                                                                           "name": "Yong Gang",
                                                                                                                           "org": "Xiamen Univ, Pen Tung Sah Inst Micronano Sci & Technol, Xiamen 361005, Peoples R China",
                                                                                                                           "orgid": "5f71b2bd1c455f439fe3deb7"},
                                                                                                                       {
                                                                                                                           "id": "65178a87768b11dc72aaca1d",
                                                                                                                           "name": "Tinghao Li",
                                                                                                                           "org": "State Key Laboratory of Structural Chemistry, Fujian Institute of Research on the Structure of Matter, Chinese Academy of Sciences, Fuzhou 350002, China",
                                                                                                                           "orgid": "5f71b29f1c455f439fe3d25c"},
                                                                                                                       {
                                                                                                                           "id": "654426308a47b64923345ee5",
                                                                                                                           "name": "Chongzhu Hu",
                                                                                                                           "org": "State Key Laboratory of Structural Chemistry, Fujian Institute of Research on the Structure of Matter, Chinese Academy of Sciences, Fuzhou 350002, China",
                                                                                                                           "orgid": "5f71b29f1c455f439fe3d25c"},
                                                                                                                       {
                                                                                                                           "id": "64e2bdd28a47b6778578b3b1",
                                                                                                                           "name": "Ni Zhang",
                                                                                                                           "org": "State Key Laboratory of Structural Chemistry, Fujian Institute of Research on the Structure of Matter, Chinese Academy of Sciences, Fuzhou 350002, China",
                                                                                                                           "orgid": "5f71b29f1c455f439fe3d25c"},
                                                                                                                       {
                                                                                                                           "id": "5e0e47cc01caee6214ea61da",
                                                                                                                           "name": "Xiaobing Wang",
                                                                                                                           "org": "Engineering Research Center of Environment-Friendly Functional Materials, Ministry of Education, Fujian Provincial Key Laboratory of Photoelectric Functional Materials, Institute of Materials Physical Chemistry, Huaqiao University, Xiamen 361021, China"},
                                                                                                                       {
                                                                                                                           "id": "542d054ddabfae489b9790f6",
                                                                                                                           "name": "Jihuai Wu",
                                                                                                                           "org": "Engineering Research Center of Environment-Friendly Functional Materials, Ministry of Education, Fujian Provincial Key Laboratory of Photoelectric Functional Materials, Institute of Materials Physical Chemistry, Huaqiao University, Xiamen 361021, China"},
                                                                                                                       {
                                                                                                                           "id": "63b0067184ab04bd7fc27e61",
                                                                                                                           "name": "Zhenhuang Su",
                                                                                                                           "org": "Shanghai Synchrotron Radiation Facility (SSRF), Shanghai Advanced Research Institute, Chinese Academy of Sciences, Shanghai 201204, China",
                                                                                                                           "orgid": "5f71b29f1c455f439fe3d25c"},
                                                                                                                       {
                                                                                                                           "id": "56cb18c3c35f4f3c65661797",
                                                                                                                           "name": "Xingyu Gao",
                                                                                                                           "org": "Shanghai Synchrotron Radiation Facility (SSRF), Shanghai Advanced Research Institute, Chinese Academy of Sciences, Shanghai 201204, China",
                                                                                                                           "orgid": "5f71b29f1c455f439fe3d25c"},
                                                                                                                       {
                                                                                                                           "id": "542a9d5edabfae2b4e12208d",
                                                                                                                           "name": "Xin Li",
                                                                                                                           "org": "Xiamen Univ, Pen Tung Sah Inst Micronano Sci & Technol, Xiamen 361005, Peoples R China",
                                                                                                                           "orgid": "5f71b2bd1c455f439fe3deb7"},
                                                                                                                       {
                                                                                                                           "id": "53f43464dabfaee4dc76fc7c",
                                                                                                                           "name": "Nanfeng Zheng",
                                                                                                                           "org": "State Key Laboratory for Physical Chemistry of Solid Surfaces, College of Chemistry and Chemical Engineering, Xiamen University, Xiamen 361005, China",
                                                                                                                           "orgid": "5f71b2bd1c455f439fe3deb7"},
                                                                                                                       {
                                                                                                                           "email": "peng.gao@fjirsm.ac.cn",
                                                                                                                           "id": "612f4a84e554229f2393e07a",
                                                                                                                           "name": "Peng Gao",
                                                                                                                           "org": "State Key Laboratory of Structural Chemistry, Fujian Institute of Research on the Structure of Matter, Chinese Academy of Sciences, Fuzhou 350002, China",
                                                                                                                           "orgid": "5f71b29f1c455f439fe3d25c"}],
                                                                                                                   "create_time": "2024-03-07T06:26:44.805Z",
                                                                                                                   "doi": "10.1016\u002Fj.joule.2024.01.016",
                                                                                                                   "id": "65e6c3bd13fb2c6cf6249759",
                                                                                                                   "issn": "2542-4351",
                                                                                                                   "keywords": [
                                                                                                                       "perovskite",
                                                                                                                       "strain uniformity",
                                                                                                                       "confocal micro-Raman spectroscopy",
                                                                                                                       "trap state",
                                                                                                                       "energy deficit"],
                                                                                                                   "lang": "en",
                                                                                                                   "num_citation": 1,
                                                                                                                   "title": "Managed Spatial Strain Uniformity for Efficient Perovskite Photovoltaics Enables Minimized Energy Deficit",
                                                                                                                   "update_times": {
                                                                                                                       "u_a_t": "2024-11-21T20:22:22Z",
                                                                                                                       "u_c_t": "2024-06-05T11:57:10.71Z",
                                                                                                                       "u_v_t": "2024-11-21T20:22:22Z"},
                                                                                                                   "urls": [
                                                                                                                       "https:\u002F\u002Fwww.sciencedirect.com\u002Fscience\u002Farticle\u002Fabs\u002Fpii\u002FS2542435124000436"],
                                                                                                                   "venue": {
                                                                                                                       "info": {
                                                                                                                           "name": "JOULE"},
                                                                                                                       "issue": "3",
                                                                                                                       "volume": "8"},
                                                                                                                   "versions": [
                                                                                                                       {
                                                                                                                           "id": "65e6c3bd13fb2c6cf6249759",
                                                                                                                           "sid": "S2542435124000436",
                                                                                                                           "src": "sciencedirect",
                                                                                                                           "vsid": "JOULE",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "6618670813fb2c6cf6f4769d",
                                                                                                                           "sid": "W4391563559",
                                                                                                                           "src": "openalex",
                                                                                                                           "vsid": "S2898305631",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "6662d4f301d2a3fbfc53b18f",
                                                                                                                           "sid": "10.1016\u002Fj.joule.2024.01.016",
                                                                                                                           "src": "crossref",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "6679886f01d2a3fbfc151bae",
                                                                                                                           "sid": "WOS:001216096800001",
                                                                                                                           "src": "wos",
                                                                                                                           "vsid": "JOULE",
                                                                                                                           "year": 2024}],
                                                                                                                   "year": 2024},
                                                                                                               {
                                                                                                                   "abstract": "A full selectivity control over the catalytic hydrogenation of nitroaromatics leads to the production of six possible products, i.e., nitroso, hydroxylamine, azoxy, azo, hydrazo or aniline compounds, which has however not been achieved in the field of heterogeneous catalysis. Currently, there is no sufficient evidence to support that the catalytic hydrogenation of nitroaromatics with the use of heterogeneous metal catalysts would follow the Haber's mechanistic scheme based on electrochemical reduction. We now demonstrate in this work that it is possible to fully control the catalytic hydrogenation of nitroaromatics into their all six products using a single catalytic system under various conditions. Employing SnO2‐supported Pt nanoparticles facilitated by the surface coordination of ethylenediamine and vanadium species enabled this unprecedented selectivity control. Through systematic investigation into the controlled production of all products and their chemical reactivities, we have constructed a detailed reaction network for the catalytic hydrogenation of nitroaromatics. Crucially, the application of oxygen‐isolated characterization techniques proved indispensable in identifying unstable compounds such as nitroso, hydroxylamine, hydrazo compounds. The insights gained from this research offer invaluable guidance for selectively transforming nitroaromatics into a wide array of functional N‐containing compounds, both advancing fundamental understanding and fostering practical applications in various fields.",
                                                                                                                   "authors": [
                                                                                                                       {
                                                                                                                           "id": "63737da09bb5705eda8ab61a",
                                                                                                                           "name": "Qingyuan Wu",
                                                                                                                           "org": "Innovation Laboratory for Sciences and Technologies of Energy Materials of Fujian Province (IKKEM), Xiamen, 361102, China."},
                                                                                                                       {
                                                                                                                           "name": "Wang Su"},
                                                                                                                       {
                                                                                                                           "id": "560ac6b845cedb33971ab3f2",
                                                                                                                           "name": "Rui Huang"},
                                                                                                                       {
                                                                                                                           "id": "5409518fdabfae450f476d54",
                                                                                                                           "name": "Hui Shen",
                                                                                                                           "org": "Inner Mongolia Univ, Coll Energy Mat & Chem, Hohhot 010021, Peoples R China",
                                                                                                                           "orgid": "5f71b2c81c455f439fe3e365"},
                                                                                                                       {
                                                                                                                           "id": "62e4be9ad9f204418d71ae4d",
                                                                                                                           "name": "Mengfei Qiao"},
                                                                                                                       {
                                                                                                                           "id": "62e4977dd9f204418d6bd7ef",
                                                                                                                           "name": "Ruixuan Qin",
                                                                                                                           "org": "Innovation Laboratory for Sciences and Technologies of Energy Materials of Fujian Province (IKKEM), Xiamen, 361102, China."},
                                                                                                                       {
                                                                                                                           "email": "nfzheng@xmu.edu.cn",
                                                                                                                           "id": "53f43464dabfaee4dc76fc7c",
                                                                                                                           "name": "Nanfeng Zheng",
                                                                                                                           "org": "Innovation Laboratory for Sciences and Technologies of Energy Materials of Fujian Province (IKKEM), Xiamen, 361102, China."}],
                                                                                                                   "create_time": "2024-06-28T19:09:45.925Z",
                                                                                                                   "doi": "10.1002\u002Fanie.202408731",
                                                                                                                   "id": "667cc1db01d2a3fbfc018c93",
                                                                                                                   "issn": "1433-7851",
                                                                                                                   "keywords": [
                                                                                                                       "Heterogeneous catalysis",
                                                                                                                       "Hydrogenation",
                                                                                                                       "Catalytic selectivity",
                                                                                                                       "Coordination chemistry",
                                                                                                                       "Nitroaromatics"],
                                                                                                                   "lang": "en",
                                                                                                                   "num_citation": 0,
                                                                                                                   "title": "Full Selectivity Control over the Catalytic Hydrogenation of Nitroaromatics into Six Products",
                                                                                                                   "update_times": {
                                                                                                                       "u_a_t": "2024-11-21T20:22:15Z",
                                                                                                                       "u_v_t": "2024-11-21T20:22:15Z"},
                                                                                                                   "urls": [
                                                                                                                       "https:\u002F\u002Fapi.crossref.org\u002Fworks\u002F10.1002\u002Fanie.202408731",
                                                                                                                       "http:\u002F\u002Fdx.doi.org\u002F10.1002\u002Fanie.202408731",
                                                                                                                       "https:\u002F\u002Fonlinelibrary.wiley.com\u002Fdoi\u002F10.1002\u002Fanie.202408731"],
                                                                                                                   "venue": {
                                                                                                                       "info": {
                                                                                                                           "name": "ANGEWANDTE CHEMIE-INTERNATIONAL EDITION"},
                                                                                                                       "issue": "38",
                                                                                                                       "volume": "63"},
                                                                                                                   "versions": [
                                                                                                                       {
                                                                                                                           "id": "667cc1db01d2a3fbfc018c93",
                                                                                                                           "sid": "10.1002\u002Fanie.202408731",
                                                                                                                           "src": "crossref",
                                                                                                                           "vsid": "ANGEWANDTE CHEMIE-INTERNATIONAL EDITION",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "667cdc9501d2a3fbfc4bf209",
                                                                                                                           "sid": "10.1002\u002Fange.202408731",
                                                                                                                           "src": "crossref",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "667dc53f01d2a3fbfc7d3442",
                                                                                                                           "sid": "38923097",
                                                                                                                           "src": "pubmed",
                                                                                                                           "vsid": "0370543",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "66d3e5ee01d2a3fbfc3ae48e",
                                                                                                                           "sid": "W4400047556",
                                                                                                                           "src": "openalex",
                                                                                                                           "vsid": "S4210200754",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "66ddd72401d2a3fbfc93430b",
                                                                                                                           "sid": "W4400047590",
                                                                                                                           "src": "openalex",
                                                                                                                           "vsid": "S67393510",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "66ec648601d2a3fbfc3f1aa5",
                                                                                                                           "sid": "WOS:001290274300001",
                                                                                                                           "src": "wos",
                                                                                                                           "vsid": "ANGEWANDTE CHEMIE-INTERNATIONAL EDITION",
                                                                                                                           "year": 2024}],
                                                                                                                   "year": 2024},
                                                                                                               {
                                                                                                                   "abstract": "The study of the structures, applications, and structure-property relationships of atomically precise metal nanoclusters relies heavily on their controlled synthesis. Although great progress has been made in the controlled synthesis of Group 11 (Cu, Ag, Au) metal nanoclusters, the preparation of Pd nanoclusters remains a grand challenge. Herein, a new, simple, and versatile synthetic strategy for the controlled synthesis of Pd nanoclusters is reported with tailorable structures and functions. The synthesis strategy involves the controllable transformations of Pd4(CO)4(CH3COO)4 in air, allowing the discovery of a family of Pd nanoclusters with well-defined structure and high yield. For example, by treating the Pd4(CO)4(CH3COO)4 with 2,2-dipyridine ligands, two clusters of Pd4 and Pd10 whose metal framework describes the growth of vertex-sharing tetrahedra have been selectively isolated. Interestingly, chiral Pd4 nanoclusters can be gained by virtue of customized chiral pyridine-imine ligands, thus representing a pioneering example to shed light on the hierarchical chiral nanostructures of Pd. This synthetic methodology also tolerates a wide variety of ligands and affords phosphine-ligated Pd nanoclusters in a simple way. It is believed that the successful exploration of the synthetic strategy would simulate the research enthusiasm on both the synthesis and application of atomically precise Pd nanoclusters. Direct reduction method gives a diversity of group 11 metal nanoclusters but plays a limited role in constructing Pd nanoclusters. Demonstrated here is a versatile strategy for Pd nanoclusters with Pd4(CH3COO)4(CO)4 as a precursor followed by controlled structural transformation. Five novel clusters are exampled with different ligated ligands and functions in a high yield and high purity. image",
                                                                                                                   "authors": [
                                                                                                                       {
                                                                                                                           "id": "65d45aaa8a47b621f77734a2",
                                                                                                                           "name": "Xiongkai Tang",
                                                                                                                           "org": "Xiamen Univ, Coll Chem & Chem Engn, Collaborat Innovat Ctr Chem Energy Mat, New Cornerstone Sci Lab,State Key Lab Phys Chem So, Xiamen 361005, Peoples R China"},
                                                                                                                       {
                                                                                                                           "id": "5409518fdabfae450f476d54",
                                                                                                                           "name": "Hui Shen",
                                                                                                                           "org": "Xiamen Univ, Coll Chem & Chem Engn, Collaborat Innovat Ctr Chem Energy Mat, New Cornerstone Sci Lab,State Key Lab Phys Chem So, Xiamen 361005, Peoples R China"},
                                                                                                                       {
                                                                                                                           "name": "Huayu Huang",
                                                                                                                           "org": "Xiamen Univ, Coll Chem & Chem Engn, Collaborat Innovat Ctr Chem Energy Mat, New Cornerstone Sci Lab,State Key Lab Phys Chem So, Xiamen 361005, Peoples R China"},
                                                                                                                       {
                                                                                                                           "id": "655c96eb33d15b6ea6a83639",
                                                                                                                           "name": "Lei Li",
                                                                                                                           "org": "Xiamen Univ, Coll Chem & Chem Engn, Collaborat Innovat Ctr Chem Energy Mat, New Cornerstone Sci Lab,State Key Lab Phys Chem So, Xiamen 361005, Peoples R China"},
                                                                                                                       {
                                                                                                                           "name": "Fan Luo",
                                                                                                                           "org": "Xiamen Univ, Coll Chem & Chem Engn, Collaborat Innovat Ctr Chem Energy Mat, New Cornerstone Sci Lab,State Key Lab Phys Chem So, Xiamen 361005, Peoples R China"},
                                                                                                                       {
                                                                                                                           "id": "6523decf55b3f8ac462b72a3",
                                                                                                                           "name": "Guolong Tian",
                                                                                                                           "org": "Xiamen Univ, Coll Chem & Chem Engn, Collaborat Innovat Ctr Chem Energy Mat, New Cornerstone Sci Lab,State Key Lab Phys Chem So, Xiamen 361005, Peoples R China"},
                                                                                                                       {
                                                                                                                           "id": "54592c42dabfaeb0fe337ad9",
                                                                                                                           "name": "Hongwen Deng",
                                                                                                                           "org": "Xiamen Univ, Coll Chem & Chem Engn, Collaborat Innovat Ctr Chem Energy Mat, New Cornerstone Sci Lab,State Key Lab Phys Chem So, Xiamen 361005, Peoples R China"},
                                                                                                                       {
                                                                                                                           "id": "54342c2bdabfaebba584ad3a",
                                                                                                                           "name": "Boon K. Teo",
                                                                                                                           "org": "Xiamen Univ, Coll Chem & Chem Engn, Collaborat Innovat Ctr Chem Energy Mat, New Cornerstone Sci Lab,State Key Lab Phys Chem So, Xiamen 361005, Peoples R China"},
                                                                                                                       {
                                                                                                                           "email": "nfzheng@xmu.edu.cn",
                                                                                                                           "id": "53f43464dabfaee4dc76fc7c",
                                                                                                                           "name": "Nanfeng Zheng",
                                                                                                                           "org": "Xiamen Univ, Coll Chem & Chem Engn, Collaborat Innovat Ctr Chem Energy Mat, New Cornerstone Sci Lab,State Key Lab Phys Chem So, Xiamen 361005, Peoples R China"}],
                                                                                                                   "create_time": "2024-05-14T01:09:46.47Z",
                                                                                                                   "doi": "10.1002\u002Fsmtd.202400040",
                                                                                                                   "id": "662f9be901d2a3fbfc5710b5",
                                                                                                                   "issn": "2366-9608",
                                                                                                                   "keywords": [
                                                                                                                       "nanoclusters",
                                                                                                                       "palladium",
                                                                                                                       "structural transformations",
                                                                                                                       "synthetic methods",
                                                                                                                       "two-step synthesis"],
                                                                                                                   "lang": "en",
                                                                                                                   "num_citation": 0,
                                                                                                                   "title": "A Versatile Strategy for the Controlled Synthesis of Atomically Precise Palladium Nanoclusters",
                                                                                                                   "update_times": {
                                                                                                                       "u_a_t": "2024-12-15T12:35:38Z",
                                                                                                                       "u_c_t": "2024-06-05T11:57:16.376Z",
                                                                                                                       "u_v_t": "2024-12-15T12:35:38Z"},
                                                                                                                   "urls": [
                                                                                                                       "https:\u002F\u002Fapi.crossref.org\u002Fworks\u002F10.1002\u002Fsmtd.202400040",
                                                                                                                       "http:\u002F\u002Fdx.doi.org\u002F10.1002\u002Fsmtd.202400040",
                                                                                                                       "https:\u002F\u002Fonlinelibrary.wiley.com\u002Fdoi\u002F10.1002\u002Fsmtd.202400040"],
                                                                                                                   "venue": {
                                                                                                                       "info": {
                                                                                                                           "name": "Small Methods",
                                                                                                                           "publisher": "Wiley"}},
                                                                                                                   "venue_hhb_id": "5ea56ef9edb6e7d53c03e58b",
                                                                                                                   "versions": [
                                                                                                                       {
                                                                                                                           "id": "662f9be901d2a3fbfc5710b5",
                                                                                                                           "sid": "10.1002\u002Fsmtd.202400040",
                                                                                                                           "src": "crossref",
                                                                                                                           "vsid": "S4210232622",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "66314e8001d2a3fbfc5b6e3c",
                                                                                                                           "sid": "38682590",
                                                                                                                           "src": "pubmed",
                                                                                                                           "vsid": "101724536",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "663c4bb401d2a3fbfc159256",
                                                                                                                           "sid": "WOS:001209853400001",
                                                                                                                           "src": "wos",
                                                                                                                           "vsid": "SMALL METHODS",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "66b81ecd01d2a3fbfcb079cc",
                                                                                                                           "sid": "W4395959971",
                                                                                                                           "src": "openalex",
                                                                                                                           "vsid": "S4210232622",
                                                                                                                           "year": 2024}],
                                                                                                                   "year": 2024},
                                                                                                               {
                                                                                                                   "abstract": "The widespread application of proton exchange membrane water electrolyzers (PEMWEs) is hampered by insufficient lifetime caused by degradation of the anode catalyst layer (ACL). Here, an important degradation mechanism has been identified, attributed to poor mechanical stability causing the mass transfer channels to be blocked by ionomers under operating conditions. By using liquid-phase atomic force microscopy, we directly observed that the ionomers were randomly distributed (RD) in the ACL, which occupied the mass transfer channels due to swelling, creeping, and migration properties. Interestingly, we found that alternating treatments of the ACL in different water\u002Ftemperature environments resulted in forming three-dimensional ionomer networks (3D INs) in the ACL, which increased the mechanical strength of microstructures by 3 times. Benefitting from the efficient and stable mass transfer channels, the lifetime was improved by 19 times. A low degradation rate of approximately 3.0 mu V\u002Fh at 80 C-degrees and a high current density of 2.0 A\u002Fcm(2) was achieved on a 50 cm(2) electrolyzer. These data demonstrated a forecasted lifetime of 80 000 h, approaching the 2026 DOE lifetime target. This work emphasizes the importance of the mechanical stability of the ACL and offers a general strategy for designing and developing a durable PEMWE.",
                                                                                                                   "authors": [
                                                                                                                       {
                                                                                                                           "id": "63254a09128293c81ede6154",
                                                                                                                           "name": "Han Liu",
                                                                                                                           "org": "Xiamen Univ, Collaborat Innovat Ctr Chem Energy Mat, State Key Lab Phys Chem Solid Surfaces, Xiamen 361005, Peoples R China",
                                                                                                                           "orgid": "5f71b2bd1c455f439fe3deb7"},
                                                                                                                       {
                                                                                                                           "name": "Yang"},
                                                                                                                       {
                                                                                                                           "name": "Jiawei Liu",
                                                                                                                           "org": "Xiamen Univ, Collaborat Innovat Ctr Chem Energy Mat, State Key Lab Phys Chem Solid Surfaces, Xiamen 361005, Peoples R China",
                                                                                                                           "orgid": "5f71b2bd1c455f439fe3deb7"},
                                                                                                                       {
                                                                                                                           "name": "Meiquan Huang",
                                                                                                                           "org": "Xiamen Univ, Collaborat Innovat Ctr Chem Energy Mat, State Key Lab Phys Chem Solid Surfaces, Xiamen 361005, Peoples R China",
                                                                                                                           "orgid": "5f71b2bd1c455f439fe3deb7"},
                                                                                                                       {
                                                                                                                           "id": "666283b263efbd4c54772a5c",
                                                                                                                           "name": "Kejie Lao",
                                                                                                                           "org": "Xiamen Univ, Collaborat Innovat Ctr Chem Energy Mat, State Key Lab Phys Chem Solid Surfaces, Xiamen 361005, Peoples R China",
                                                                                                                           "orgid": "5f71b2bd1c455f439fe3deb7"},
                                                                                                                       {
                                                                                                                           "name": "Yaping Pan",
                                                                                                                           "org": "Xiamen Univ, Collaborat Innovat Ctr Chem Energy Mat, State Key Lab Phys Chem Solid Surfaces, Xiamen 361005, Peoples R China",
                                                                                                                           "orgid": "5f71b2bd1c455f439fe3deb7"},
                                                                                                                       {
                                                                                                                           "id": "5448b9eddabfae87b7e6daef",
                                                                                                                           "name": "Xinhui Wang",
                                                                                                                           "org": "Xiamen Univ, Collaborat Innovat Ctr Chem Energy Mat, State Key Lab Phys Chem Solid Surfaces, Xiamen 361005, Peoples R China",
                                                                                                                           "orgid": "5f71b2bd1c455f439fe3deb7"},
                                                                                                                       {
                                                                                                                           "name": "Tian Hu",
                                                                                                                           "org": "Xiamen Univ, Collaborat Innovat Ctr Chem Energy Mat, State Key Lab Phys Chem Solid Surfaces, Xiamen 361005, Peoples R China",
                                                                                                                           "orgid": "5f71b2bd1c455f439fe3deb7"},
                                                                                                                       {
                                                                                                                           "id": "666283a55cc239717cbdc0ff",
                                                                                                                           "name": "Linrui Wen",
                                                                                                                           "org": "IKKEM, Innovat Lab Sci & Technol Energy Mat Fujian Prov, Xiamen 361005, Peoples R China"},
                                                                                                                       {
                                                                                                                           "id": "650564808a47b65bc5bf21a2",
                                                                                                                           "name": "Shuwen Xu",
                                                                                                                           "org": "Xiamen Univ, Collaborat Innovat Ctr Chem Energy Mat, State Key Lab Phys Chem Solid Surfaces, Xiamen 361005, Peoples R China",
                                                                                                                           "orgid": "5f71b2bd1c455f439fe3deb7"},
                                                                                                                       {
                                                                                                                           "id": "53f47397dabfaedd74e9dd5f",
                                                                                                                           "name": "Shuirong Li",
                                                                                                                           "org": "Xiamen Univ, Coll Energy, Xiamen 361005, Peoples R China",
                                                                                                                           "orgid": "5f71b2bd1c455f439fe3deb7"},
                                                                                                                       {
                                                                                                                           "id": "53f386c6dabfae4b34a17bb3",
                                                                                                                           "name": "Xiaoliang Fang",
                                                                                                                           "org": "Xiamen Univ, Coll Energy, Xiamen 361005, Peoples R China",
                                                                                                                           "orgid": "5f71b2bd1c455f439fe3deb7"},
                                                                                                                       {
                                                                                                                           "email": "w.lin@lboro.ac.uk",
                                                                                                                           "id": "53f4d62ddabfaef467f811ee",
                                                                                                                           "name": "Wen-Feng Lin",
                                                                                                                           "org": "Loughborough Univ, Dept Chem Engn, Loughborough LE11 3TU, England",
                                                                                                                           "orgid": "5f71b29c1c455f439fe3d0d7"},
                                                                                                                       {
                                                                                                                           "email": "nfzheng@xmu.edu.cn",
                                                                                                                           "id": "53f43464dabfaee4dc76fc7c",
                                                                                                                           "name": "Nanfeng Zheng",
                                                                                                                           "org": "Xiamen Univ, Collaborat Innovat Ctr Chem Energy Mat, State Key Lab Phys Chem Solid Surfaces, Xiamen 361005, Peoples R China",
                                                                                                                           "orgid": "5f71b2bd1c455f439fe3deb7"},
                                                                                                                       {
                                                                                                                           "email": "hbtao@xmu.edu.cn",
                                                                                                                           "id": "65e53f3ff54ee14c01fc809b",
                                                                                                                           "name": "Hua Bing Tao",
                                                                                                                           "org": "Xiamen Univ, Collaborat Innovat Ctr Chem Energy Mat, State Key Lab Phys Chem Solid Surfaces, Xiamen 361005, Peoples R China",
                                                                                                                           "orgid": "5f71b2bd1c455f439fe3deb7"}],
                                                                                                                   "create_time": "2024-05-20T07:00:03.617Z",
                                                                                                                   "doi": "10.1021\u002Facsami.4c03318",
                                                                                                                   "id": "65fab14713fb2c6cf6ce59f9",
                                                                                                                   "issn": "1944-8244",
                                                                                                                   "keywords": [
                                                                                                                       "PEM water electrolysis",
                                                                                                                       "stability in hydrogen production",
                                                                                                                       "anode catalyst layer",
                                                                                                                       "three-dimensional ionomer networks",
                                                                                                                       "thermal and water cycles"],
                                                                                                                   "lang": "en",
                                                                                                                   "num_citation": 0,
                                                                                                                   "pages": {
                                                                                                                       "end": "16417",
                                                                                                                       "start": "16408"},
                                                                                                                   "title": "Constructing Robust 3D Ionomer Networks in the Catalyst Layer to Achieve Stable Water Electrolysis for Green Hydrogen Production",
                                                                                                                   "update_times": {
                                                                                                                       "u_a_t": "2024-11-22T01:48:51Z",
                                                                                                                       "u_c_t": "2024-06-05T11:57:10.833Z",
                                                                                                                       "u_v_t": "2024-11-22T01:48:51Z"},
                                                                                                                   "urls": [
                                                                                                                       "https:\u002F\u002Fapi.crossref.org\u002Fworks\u002F10.1021\u002Facsami.4c03318",
                                                                                                                       "http:\u002F\u002Fdx.doi.org\u002F10.1021\u002Facsami.4c03318",
                                                                                                                       "https:\u002F\u002Fpubs.acs.org\u002Fdoi\u002F10.1021\u002Facsami.4c03318"],
                                                                                                                   "venue": {
                                                                                                                       "info": {
                                                                                                                           "name": "ACS APPLIED MATERIALS & INTERFACES"},
                                                                                                                       "issue": "13",
                                                                                                                       "volume": "16"},
                                                                                                                   "versions": [
                                                                                                                       {
                                                                                                                           "id": "65fab14713fb2c6cf6ce59f9",
                                                                                                                           "sid": "10.1021\u002Facsami.4c03318",
                                                                                                                           "src": "crossref",
                                                                                                                           "vsid": "ACS APPLIED MATERIALS & INTERFACES",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "65fb41f213fb2c6cf642440e",
                                                                                                                           "sid": "38502312",
                                                                                                                           "src": "pubmed",
                                                                                                                           "vsid": "101504991",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "6668e26a01d2a3fbfcdeeda8",
                                                                                                                           "sid": "W4392949055",
                                                                                                                           "src": "openalex",
                                                                                                                           "vsid": "S164001016",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "660cf24e13fb2c6cf6159c1c",
                                                                                                                           "sid": "WOS:001187624600001",
                                                                                                                           "src": "wos",
                                                                                                                           "vsid": "ACS APPLIED MATERIALS & INTERFACES",
                                                                                                                           "year": 2024}],
                                                                                                                   "year": 2024},
                                                                                                               {
                                                                                                                   "abstract": "Li-TFSI doped spiro-OMeTAD is widely recognized as a beneficial hole transport layer (HTL) in perovskite solar cells (PSCs), contributing to high device efficiencies. However, the uncontrolled migration of lithium ions (Li+) during device operation has impeded its broad adoption in scalable and stable photovoltaic modules. Herein, an additive strategy is proposed by employing ferrocenium hexafluorophosphate (FcPF6) as a relay medium to enhance the hole extraction capability of the spiro-OMeTAD via the instant oxidation function. Besides, the novel Fc-Li interaction effectively restricts the movement of Li+. Simultaneously, the dissociative hexafluorophosphate group is cleverly exploited to regulate the unstable iodide species on the perovskite surface, further inhibiting the formation of migration channels and stabilizing the interfaces. This modification leads to power conversion efficiencies (PCEs) reaching 22.13% and 20.27% in 36 cm2 (active area of 18 cm2) and 100 cm2 (active area of 56 cm2) perovskite solar modules (PSMs), respectively, with exceptional operational stability obtained for over 1000 h under the ISOS-L-1 procedure. The novel FcPF6-based engineering approach is pivotal for advancing the industrialization of PSCs, particularly those relying on high-performance spiro-OMeTAD- based HTLs.",
                                                                                                                   "authors": [
                                                                                                                       {
                                                                                                                           "id": "5616859145cedb3397b47045",
                                                                                                                           "name": "Qing Chang"},
                                                                                                                       {
                                                                                                                           "id": "65af33c28a47b62da8e0e0a2",
                                                                                                                           "name": "Yikai Yun",
                                                                                                                           "org": "Xiamen Univ, Sch Elect Sci & Engn, Xiamen 361102, Peoples R China",
                                                                                                                           "orgid": "5f71b2bd1c455f439fe3deb7"},
                                                                                                                       {
                                                                                                                           "id": "6379590cf789b382be998db6",
                                                                                                                           "name": "Kexin Cao",
                                                                                                                           "org": "Innovat Lab Sci & Technol Energy Mat Fujian Prov I, Xiamen 361102, Peoples R China"},
                                                                                                                       {
                                                                                                                           "name": "Wenlong Yao"},
                                                                                                                       {
                                                                                                                           "id": "5609335745ce1e595f68793e",
                                                                                                                           "name": "Xiaofeng Huang",
                                                                                                                           "org": "Innovat Lab Sci & Technol Energy Mat Fujian Prov I, Xiamen 361102, Peoples R China"},
                                                                                                                       {
                                                                                                                           "name": "Peng He",
                                                                                                                           "org": "Innovat Lab Sci & Technol Energy Mat Fujian Prov I, Xiamen 361102, Peoples R China"},
                                                                                                                       {
                                                                                                                           "id": "6325a1b1f5ee9683ec775b15",
                                                                                                                           "name": "Yang Shen",
                                                                                                                           "org": "Innovat Lab Sci & Technol Energy Mat Fujian Prov I, Xiamen 361102, Peoples R China"},
                                                                                                                       {
                                                                                                                           "id": "637a746bf789b382bea16466",
                                                                                                                           "name": "Zhengjing Zhao",
                                                                                                                           "org": "Huaneng Clean Energy Res Inst, Beijing 102209, Peoples R China",
                                                                                                                           "orgid": "61e69fe86896273465747dc6"},
                                                                                                                       {
                                                                                                                           "id": "5617090845ce1e5963c01778",
                                                                                                                           "name": "Mengyu Chen",
                                                                                                                           "org": "Xiamen Univ, Sch Elect Sci & Engn, Xiamen 361102, Peoples R China",
                                                                                                                           "orgid": "5f71b2bd1c455f439fe3deb7"},
                                                                                                                       {
                                                                                                                           "id": "542a68b2dabfae2b4e1002f7",
                                                                                                                           "name": "Cheng Li",
                                                                                                                           "org": "Xiamen Univ, Sch Elect Sci & Engn, Xiamen 361102, Peoples R China",
                                                                                                                           "orgid": "5f71b2bd1c455f439fe3deb7"},
                                                                                                                       {
                                                                                                                           "id": "53f45c75dabfaefedbb657f3",
                                                                                                                           "name": "Binghui Wu"},
                                                                                                                       {
                                                                                                                           "email": "jyin@xmu.edu.cn",
                                                                                                                           "id": "5613297645cedb339799e818",
                                                                                                                           "name": "Jun Yin"},
                                                                                                                       {
                                                                                                                           "email": "zg_zhao@qny.chng.com.cn",
                                                                                                                           "id": "63273e20a95e4d1d05564259",
                                                                                                                           "name": "Zhiguo Zhao",
                                                                                                                           "org": "Huaneng Clean Energy Res Inst, Beijing 102209, Peoples R China",
                                                                                                                           "orgid": "61e69fe86896273465747dc6"},
                                                                                                                       {
                                                                                                                           "email": "lijing@xmu.edu.cn",
                                                                                                                           "id": "5429f967dabfaec7081d0cfc",
                                                                                                                           "name": "Jing Li"},
                                                                                                                       {
                                                                                                                           "id": "53f43464dabfaee4dc76fc7c",
                                                                                                                           "name": "Nanfeng Zheng",
                                                                                                                           "org": "Innovat Lab Sci & Technol Energy Mat Fujian Prov I, Xiamen 361102, Peoples R China"}],
                                                                                                                   "create_time": "2024-09-07T20:43:37.032Z",
                                                                                                                   "doi": "10.1002\u002Fadma.202406296",
                                                                                                                   "id": "66da0dc001d2a3fbfc4bc30c",
                                                                                                                   "issn": "0935-9648",
                                                                                                                   "keywords": [
                                                                                                                       "ferrocenium hexafluorophosphate",
                                                                                                                       "ions migration",
                                                                                                                       "multifunctional dopant",
                                                                                                                       "perovskite solar modules"],
                                                                                                                   "lang": "en",
                                                                                                                   "num_citation": 0,
                                                                                                                   "title": "Highly Efficient and Stable Perovskite Solar Modules Based on FcPF6 Engineered Spiro-OMeTAD Hole Transporting Layer",
                                                                                                                   "update_times": {
                                                                                                                       "u_a_t": "2024-12-03T16:01:06Z",
                                                                                                                       "u_v_t": "2024-12-03T16:01:06Z"},
                                                                                                                   "urls": [
                                                                                                                       "https:\u002F\u002Fwww.ncbi.nlm.nih.gov\u002Fpubmed\u002F39233551"],
                                                                                                                   "venue": {
                                                                                                                       "info": {
                                                                                                                           "name": "Advanced Materials",
                                                                                                                           "publisher": "Wiley"}},
                                                                                                                   "versions": [
                                                                                                                       {
                                                                                                                           "id": "66da0dc001d2a3fbfc4bc30c",
                                                                                                                           "sid": "39233551",
                                                                                                                           "src": "pubmed",
                                                                                                                           "vsid": "S99352657",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "66da553601d2a3fbfcfc318c",
                                                                                                                           "sid": "10.1002\u002Fadma.202406296",
                                                                                                                           "src": "crossref",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "6711ec5a01d2a3fbfc2e5492",
                                                                                                                           "sid": "WOS:001306106600001",
                                                                                                                           "src": "wos",
                                                                                                                           "vsid": "ADVANCED MATERIALS",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "674eb9aaae8580e7ff7be422",
                                                                                                                           "sid": "W4402281669",
                                                                                                                           "src": "openalex",
                                                                                                                           "vsid": "S99352657",
                                                                                                                           "year": 2024}],
                                                                                                                   "year": 2024},
                                                                                                               {
                                                                                                                   "abstract": "By mimicking nanoscale galvanic reactions, this study focuses on optimizing catalytic hydrogenation by introducing two spatially separated sites for the activation of H2 into proton and electron pairs and the selective reduction of –NO2. The catalyst system is designed with the co-deposition of Pt and Fe2O3 nanoparticles on conductive carbon nanotubes, establishing an electron-transferring pathway. Protic solvents facilitate proton transport. Upon activation of H2 molecules into proton and electron pairs on Pt, modified with ammonia or amines, these active species are efficiently transferred to Fe2O3 nanoparticles for the selective reduction of –NO2 into amines without affecting other functional groups. Compared with Pt\u002FCNT, which easily hydrogenates both C=C and –NO2 groups of 4-nitrostyrene, the Pt&Fe2O3\u002FCNT catalyst modified by NH3 exhibits higher activity and selectivity for –NO2 hydrogenation. Electrochemically, Pt functions as the anode for the hydrogen oxidation reaction, while Fe2O3 acts as the cathode, selectively reducing –NO2.",
                                                                                                                   "authors": [
                                                                                                                       {
                                                                                                                           "id": "62e4be9ad9f204418d71ae4d",
                                                                                                                           "name": "Mengfei Qiao",
                                                                                                                           "org": "New Cornerstone Science Laboratory, State Key Laboratory for Physical Chemistry of Solid Surfaces, Collaborative Innovation Center of Chemistry for Energy Materials, and National & Local Joint Engineering Research Center of Preparation Technology of Nanomaterials, College of Chemistry and Chemical Engineering, Xiamen University, Xiamen 361005, China",
                                                                                                                           "orgs": [
                                                                                                                               "New Cornerstone Science Laboratory, State Key Laboratory for Physical Chemistry of Solid Surfaces, Collaborative Innovation Center of Chemistry for Energy Materials, and National & Local Joint Engineering Research Center of Preparation Technology of Nanomaterials, College of Chemistry and Chemical Engineering, Xiamen University, Xiamen 361005, China"]},
                                                                                                                       {
                                                                                                                           "id": "63737da09bb5705eda8ab61a",
                                                                                                                           "name": "Qingyuan Wu",
                                                                                                                           "org": "New Cornerstone Science Laboratory, State Key Laboratory for Physical Chemistry of Solid Surfaces, Collaborative Innovation Center of Chemistry for Energy Materials, and National & Local Joint Engineering Research Center of Preparation Technology of Nanomaterials, College of Chemistry and Chemical Engineering, Xiamen University, Xiamen 361005, China",
                                                                                                                           "orgs": [
                                                                                                                               "New Cornerstone Science Laboratory, State Key Laboratory for Physical Chemistry of Solid Surfaces, Collaborative Innovation Center of Chemistry for Energy Materials, and National & Local Joint Engineering Research Center of Preparation Technology of Nanomaterials, College of Chemistry and Chemical Engineering, Xiamen University, Xiamen 361005, China"]},
                                                                                                                       {
                                                                                                                           "id": "56057eab45cedb33966447be",
                                                                                                                           "name": "Ying Wang",
                                                                                                                           "org": "New Cornerstone Science Laboratory, State Key Laboratory for Physical Chemistry of Solid Surfaces, Collaborative Innovation Center of Chemistry for Energy Materials, and National & Local Joint Engineering Research Center of Preparation Technology of Nanomaterials, College of Chemistry and Chemical Engineering, Xiamen University, Xiamen 361005, China",
                                                                                                                           "orgs": [
                                                                                                                               "New Cornerstone Science Laboratory, State Key Laboratory for Physical Chemistry of Solid Surfaces, Collaborative Innovation Center of Chemistry for Energy Materials, and National & Local Joint Engineering Research Center of Preparation Technology of Nanomaterials, College of Chemistry and Chemical Engineering, Xiamen University, Xiamen 361005, China"]},
                                                                                                                       {
                                                                                                                           "name": "Shanshan Gao",
                                                                                                                           "org": "New Cornerstone Science Laboratory, State Key Laboratory for Physical Chemistry of Solid Surfaces, Collaborative Innovation Center of Chemistry for Energy Materials, and National & Local Joint Engineering Research Center of Preparation Technology of Nanomaterials, College of Chemistry and Chemical Engineering, Xiamen University, Xiamen 361005, China",
                                                                                                                           "orgs": [
                                                                                                                               "New Cornerstone Science Laboratory, State Key Laboratory for Physical Chemistry of Solid Surfaces, Collaborative Innovation Center of Chemistry for Energy Materials, and National & Local Joint Engineering Research Center of Preparation Technology of Nanomaterials, College of Chemistry and Chemical Engineering, Xiamen University, Xiamen 361005, China"]},
                                                                                                                       {
                                                                                                                           "email": "qinrx@xmu.edu.cn",
                                                                                                                           "id": "62e4977dd9f204418d6bd7ef",
                                                                                                                           "name": "Ruixuan Qin",
                                                                                                                           "org": "New Cornerstone Science Laboratory, State Key Laboratory for Physical Chemistry of Solid Surfaces, Collaborative Innovation Center of Chemistry for Energy Materials, and National & Local Joint Engineering Research Center of Preparation Technology of Nanomaterials, College of Chemistry and Chemical Engineering, Xiamen University, Xiamen 361005, China",
                                                                                                                           "orgs": [
                                                                                                                               "New Cornerstone Science Laboratory, State Key Laboratory for Physical Chemistry of Solid Surfaces, Collaborative Innovation Center of Chemistry for Energy Materials, and National & Local Joint Engineering Research Center of Preparation Technology of Nanomaterials, College of Chemistry and Chemical Engineering, Xiamen University, Xiamen 361005, China"]},
                                                                                                                       {
                                                                                                                           "id": "5614d01745ce1e596350853c",
                                                                                                                           "name": "Shengjie Liu",
                                                                                                                           "org": "New Cornerstone Science Laboratory, State Key Laboratory for Physical Chemistry of Solid Surfaces, Collaborative Innovation Center of Chemistry for Energy Materials, and National & Local Joint Engineering Research Center of Preparation Technology of Nanomaterials, College of Chemistry and Chemical Engineering, Xiamen University, Xiamen 361005, China",
                                                                                                                           "orgs": [
                                                                                                                               "New Cornerstone Science Laboratory, State Key Laboratory for Physical Chemistry of Solid Surfaces, Collaborative Innovation Center of Chemistry for Energy Materials, and National & Local Joint Engineering Research Center of Preparation Technology of Nanomaterials, College of Chemistry and Chemical Engineering, Xiamen University, Xiamen 361005, China"]},
                                                                                                                       {
                                                                                                                           "name": "Kehong Ding",
                                                                                                                           "org": "Jiangsu Yangnong Chemical Group Co., Ltd., Yangzhou 225002, China",
                                                                                                                           "orgs": [
                                                                                                                               "Jiangsu Yangnong Chemical Group Co., Ltd., Yangzhou 225002, China"]},
                                                                                                                       {
                                                                                                                           "id": "64ccaa19d6fcf4e735043713",
                                                                                                                           "name": "Dongyuan Zhao",
                                                                                                                           "org": "School of Chemistry and Materials, Laboratory of Advanced Materials, Department of Chemistry, Fudan University, Shanghai, China",
                                                                                                                           "orgs": [
                                                                                                                               "School of Chemistry and Materials, Laboratory of Advanced Materials, Department of Chemistry, Fudan University, Shanghai, China"]},
                                                                                                                       {
                                                                                                                           "email": "nfzheng@xmu.edu.cn",
                                                                                                                           "id": "53f43464dabfaee4dc76fc7c",
                                                                                                                           "name": "Nanfeng Zheng",
                                                                                                                           "org": "New Cornerstone Science Laboratory, State Key Laboratory for Physical Chemistry of Solid Surfaces, Collaborative Innovation Center of Chemistry for Energy Materials, and National & Local Joint Engineering Research Center of Preparation Technology of Nanomaterials, College of Chemistry and Chemical Engineering, Xiamen University, Xiamen 361005, China",
                                                                                                                           "orgs": [
                                                                                                                               "New Cornerstone Science Laboratory, State Key Laboratory for Physical Chemistry of Solid Surfaces, Collaborative Innovation Center of Chemistry for Energy Materials, and National & Local Joint Engineering Research Center of Preparation Technology of Nanomaterials, College of Chemistry and Chemical Engineering, Xiamen University, Xiamen 361005, China",
                                                                                                                               "Innovation Laboratory for Sciences and Technologies of Energy Materials of Fujian Province (IKKEM), Xiamen 361102, China"]}],
                                                                                                                   "create_time": "2024-07-31T23:45:23.809Z",
                                                                                                                   "doi": "10.1016\u002Fj.chempr.2024.06.030",
                                                                                                                   "hashs": {
                                                                                                                       "h1": "shcen",
                                                                                                                       "h3": "gr"},
                                                                                                                   "id": "66a06d5a01d2a3fbfc14fba5",
                                                                                                                   "issn": "2451-9294",
                                                                                                                   "keywords": [
                                                                                                                       "selective hydrogenation",
                                                                                                                       "hydrogenation of nitroaromatics",
                                                                                                                       "nanoscale galvanic reaction",
                                                                                                                       "electrochemical reduction",
                                                                                                                       "poisoning resistance"],
                                                                                                                   "num_citation": 0,
                                                                                                                   "title": "Selective hydrogenation catalysis enabled by nanoscale galvanic reactions",
                                                                                                                   "urls": [
                                                                                                                       "https:\u002F\u002Fwww.sciencedirect.com\u002Fscience\u002Farticle\u002Fabs\u002Fpii\u002FS2451929424003097"],
                                                                                                                   "venue": {
                                                                                                                       "info": {
                                                                                                                           "name": "Chem"}},
                                                                                                                   "versions": [
                                                                                                                       {
                                                                                                                           "id": "66a06d5a01d2a3fbfc14fba5",
                                                                                                                           "sid": "S2451929424003097",
                                                                                                                           "src": "sciencedirect"}],
                                                                                                                   "year": 2024},
                                                                                                               {
                                                                                                                   "abstract": "The high cost of proton exchange membrane water electrolysis (PEMWE) originates from the usage of precious materials, insufficient efficiency, and lifetime. In this work, an important degradation mechanism of PEMWE caused by dynamics of ionomers over time in anode catalyst layer (ACL), which is a purely mechanical degradation of microstructure, is identified. Contrary to conventional understanding that the microstructure of ACL is static, the micropores are inclined to be occupied by ionomers due to the localized swelling\u002Fcreep\u002Fmigration, especially near the ACL\u002FPTL (porous transport layer) interface, where they form transport channels of reactant\u002Fproduct couples. Consequently, the ACL with increased ionomers at PTL\u002FACL interface exhibit rapid and continuous degradation. In addition, a close correlation between the microstructure of ACL and the catalyst ink is discovered. Specifically, if more ionomers migrate to the top layer of the ink, more ionomers accumulate at the ACL\u002FPEM interface, leaving fewer ionomers at the ACL\u002FPTL interface. Therefore, the ionomer distribution in ACL is successfully optimized, which exhibits reduced ionomers at the ACL\u002FPTL interface and enriches ionomers at the ACL\u002FPEM interface, reducing the decay rate by a factor of three when operated at 2.0 A cm-2 and 80 degrees C. The findings provide a general way to achieve low-cost hydrogen production. The anode catalyst layer (ACL) is the key to determining the lifetime of proton exchange membrane water electrolysis. In this work, an efficient gradient ionomer distributed ACL structure is fabricated through optimizing the catalyst ink, which improves the durability by a factor of three compared to the normal ACL when operating at 2.0 A cm-2 and 80 degrees C. image",
                                                                                                                   "authors": [
                                                                                                                       {
                                                                                                                           "id": "63254a09128293c81ede6154",
                                                                                                                           "name": "Han Liu",
                                                                                                                           "org": "State Key Laboratory for Physical Chemistry of Solid Surfaces, Collaborative Innovation Center of Chemistry for Energy Materials, and College of Chemistry and Chemical Engineering, Xiamen University, Xiamen, 361005, China."},
                                                                                                                       {
                                                                                                                           "id": "5448b9eddabfae87b7e6daef",
                                                                                                                           "name": "Xinhui Wang",
                                                                                                                           "org": "State Key Laboratory for Physical Chemistry of Solid Surfaces, Collaborative Innovation Center of Chemistry for Energy Materials, and College of Chemistry and Chemical Engineering, Xiamen University, Xiamen, 361005, China."},
                                                                                                                       {
                                                                                                                           "id": "666283b263efbd4c54772a5c",
                                                                                                                           "name": "Kejie Lao",
                                                                                                                           "org": "State Key Laboratory for Physical Chemistry of Solid Surfaces, Collaborative Innovation Center of Chemistry for Energy Materials, and College of Chemistry and Chemical Engineering, Xiamen University, Xiamen, 361005, China."},
                                                                                                                       {
                                                                                                                           "id": "666283a55cc239717cbdc0ff",
                                                                                                                           "name": "Linrui Wen",
                                                                                                                           "org": "Innovat Lab Sci & Technol Energy Mat Fujian Prov I, Xiamen 361005, Peoples R China"},
                                                                                                                       {
                                                                                                                           "name": "Meiquan Huang",
                                                                                                                           "org": "State Key Laboratory for Physical Chemistry of Solid Surfaces, Collaborative Innovation Center of Chemistry for Energy Materials, and College of Chemistry and Chemical Engineering, Xiamen University, Xiamen, 361005, China."},
                                                                                                                       {
                                                                                                                           "name": "Jiawei Liu",
                                                                                                                           "org": "State Key Laboratory for Physical Chemistry of Solid Surfaces, Collaborative Innovation Center of Chemistry for Energy Materials, and College of Chemistry and Chemical Engineering, Xiamen University, Xiamen, 361005, China."},
                                                                                                                       {
                                                                                                                           "name": "Tian Hu",
                                                                                                                           "org": "State Key Laboratory for Physical Chemistry of Solid Surfaces, Collaborative Innovation Center of Chemistry for Energy Materials, and College of Chemistry and Chemical Engineering, Xiamen University, Xiamen, 361005, China."},
                                                                                                                       {
                                                                                                                           "email": "hbtao@xmu.edu.cn",
                                                                                                                           "name": "Bo Hu",
                                                                                                                           "org": "Innovat Lab Sci & Technol Energy Mat Fujian Prov I, Xiamen 361005, Peoples R China"},
                                                                                                                       {
                                                                                                                           "id": "5433b391dabfaeba807d9919",
                                                                                                                           "name": "Shunji Xie",
                                                                                                                           "org": "State Key Laboratory for Physical Chemistry of Solid Surfaces, Collaborative Innovation Center of Chemistry for Energy Materials, and College of Chemistry and Chemical Engineering, Xiamen University, Xiamen, 361005, China."},
                                                                                                                       {
                                                                                                                           "id": "53f47397dabfaedd74e9dd5f",
                                                                                                                           "name": "Shuirong Li",
                                                                                                                           "org": "Xiamen Univ, Coll Energy, Xiamen 361005, Peoples R China",
                                                                                                                           "orgid": "5f71b2bd1c455f439fe3deb7"},
                                                                                                                       {
                                                                                                                           "id": "53f386c6dabfae4b34a17bb3",
                                                                                                                           "name": "Xiaoliang Fang",
                                                                                                                           "org": "State Key Laboratory for Physical Chemistry of Solid Surfaces, Collaborative Innovation Center of Chemistry for Energy Materials, and College of Chemistry and Chemical Engineering, Xiamen University, Xiamen, 361005, China."},
                                                                                                                       {
                                                                                                                           "email": "nfzheng@xmu.edu.cn",
                                                                                                                           "id": "53f43464dabfaee4dc76fc7c",
                                                                                                                           "name": "Nanfeng Zheng",
                                                                                                                           "org": "State Key Laboratory for Physical Chemistry of Solid Surfaces, Collaborative Innovation Center of Chemistry for Energy Materials, and College of Chemistry and Chemical Engineering, Xiamen University, Xiamen, 361005, China."},
                                                                                                                       {
                                                                                                                           "id": "65e53f3ff54ee14c01fc809b",
                                                                                                                           "name": "Hua Bing Tao",
                                                                                                                           "org": "State Key Laboratory for Physical Chemistry of Solid Surfaces, Collaborative Innovation Center of Chemistry for Energy Materials, and College of Chemistry and Chemical Engineering, Xiamen University, Xiamen, 361005, China."}],
                                                                                                                   "create_time": "2024-07-19T10:19:58.319Z",
                                                                                                                   "doi": "10.1002\u002Fadma.202402780",
                                                                                                                   "id": "662ab67401d2a3fbfc385f39",
                                                                                                                   "issn": "0935-9648",
                                                                                                                   "keywords": [
                                                                                                                       "anode catalyst layer",
                                                                                                                       "catalyst ink",
                                                                                                                       "gradient ionomer distribution",
                                                                                                                       "interface",
                                                                                                                       "PEM water electrolysis"],
                                                                                                                   "lang": "en",
                                                                                                                   "num_citation": 0,
                                                                                                                   "pdf": "https:\u002F\u002Fstatic.aminer.cn\u002Fupload\u002Fpdf\u002F1210\u002F2009\u002F117\u002F662ab67401d2a3fbfc385f39_0.pdf",
                                                                                                                   "title": "Optimizing Ionomer Distribution in Anode Catalyst Layer for Stable Proton Exchange Membrane Water Electrolysis.",
                                                                                                                   "update_times": {
                                                                                                                       "u_a_t": "2024-11-22T01:52:44Z",
                                                                                                                       "u_c_t": "2024-06-05T11:57:10.946Z",
                                                                                                                       "u_v_t": "2024-11-22T01:52:44Z"},
                                                                                                                   "urls": [
                                                                                                                       "https:\u002F\u002Fwww.ncbi.nlm.nih.gov\u002Fpubmed\u002F38661112"],
                                                                                                                   "venue": {
                                                                                                                       "info": {
                                                                                                                           "name": "ADVANCED MATERIALS"},
                                                                                                                       "issue": "28",
                                                                                                                       "volume": "36"},
                                                                                                                   "venue_hhb_id": "5ea5749fedb6e7d53c03fc5c",
                                                                                                                   "versions": [
                                                                                                                       {
                                                                                                                           "id": "662ab67401d2a3fbfc385f39",
                                                                                                                           "sid": "38661112",
                                                                                                                           "src": "pubmed",
                                                                                                                           "vsid": "ADVANCED MATERIALS",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "662b20b601d2a3fbfc734bc7",
                                                                                                                           "sid": "10.1002\u002Fadma.202402780",
                                                                                                                           "src": "crossref",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "66d951c901d2a3fbfc1df42e",
                                                                                                                           "sid": "W4395452770",
                                                                                                                           "src": "openalex",
                                                                                                                           "vsid": "S99352657",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "6678a3ba01d2a3fbfc8b9192",
                                                                                                                           "sid": "WOS:001216826500001",
                                                                                                                           "src": "wos",
                                                                                                                           "vsid": "ADVANCED MATERIALS",
                                                                                                                           "year": 2024}],
                                                                                                                   "year": 2024},
                                                                                                               {
                                                                                                                   "abstract": "In recent years, the concept of Frustrated Lewis Pairs (FLPs), which consist of a combination of Lewis acid (LA) and Lewis base (LB) active sites arranged in a suitable geometric configuration, has been widely utilized in homogeneous catalytic reactions. This concept has also been extended to solid supports such as zeolites, metal oxide surfaces, and metal\u002Fcovalent organic frameworks, resulting in a diverse range of heterogeneous FLP catalysts that have demonstrated notable efficiency and recyclability in activating small molecules. This study presents the successful immobilization of FLP active sites onto the surface of ligand-stabilized copper nanoclusters with atomic precision, leading to the development of copper nanocluster FLP catalysts characterized by high reactivity, stability, and selectivity. Specifically, thiol ligands containing 2-methoxyl groups were strategically designed to stabilize the surface of [Cu34S7(RS)18(PPh3)4]2+ (where RSH = 2-methoxybenzenethiol), facilitating the formation of FLPs between the surface copper atoms (LA) and ligand oxygen atoms (LB). Experimental and theoretical investigations have demonstrated that these FLPs on the cluster surface can efficiently activate H2 through a heterolytic pathway, resulting in superior catalytic performance in the hydrogenation of alkenes under mild conditions. Notably, the intricate yet precise surface coordination structures of the cluster, reminiscent of enzyme catalysts, enable the hydrogenation process to proceed with nearly 100% selectivity. This research offers valuable insights into the design of FLP catalysts with enhanced activity and selectivity by leveraging surface\u002Finterface coordination chemistry of ligand-stabilized atomically precise metal nanoclusters.",
                                                                                                                   "authors": [
                                                                                                                       {
                                                                                                                           "id": "651c9986768b11dc72b11895",
                                                                                                                           "name": "Simin Li",
                                                                                                                           "org": "Inner Mongolia Univ, Coll Energy Mat & Chem, Hohhot 010021, Peoples R China",
                                                                                                                           "orgid": "5f71b2c81c455f439fe3e365"},
                                                                                                                       {
                                                                                                                           "id": "63737da09bb5705eda8ab61a",
                                                                                                                           "name": "Qingyuan Wu"},
                                                                                                                       {
                                                                                                                           "name": "Xuexin You",
                                                                                                                           "org": "Inner Mongolia Univ, Sch Phys Sci & Technol, Hohhot 010021, Peoples R China",
                                                                                                                           "orgid": "5f71b2c81c455f439fe3e365"},
                                                                                                                       {
                                                                                                                           "name": "Xiaofei Ren",
                                                                                                                           "org": "Inner Mongolia Univ, Coll Energy Mat & Chem, Hohhot 010021, Peoples R China",
                                                                                                                           "orgid": "5f71b2c81c455f439fe3e365"},
                                                                                                                       {
                                                                                                                           "id": "6170696460a965737d74e1bb",
                                                                                                                           "name": "Peilin Du",
                                                                                                                           "org": "Inner Mongolia Univ, Coll Energy Mat & Chem, Hohhot 010021, Peoples R China",
                                                                                                                           "orgid": "5f71b2c81c455f439fe3e365"},
                                                                                                                       {
                                                                                                                           "email": "fengyuli@imu.edu.cn",
                                                                                                                           "id": "542c51a1dabfae1ad8960d9f",
                                                                                                                           "name": "Fengyu Li",
                                                                                                                           "org": "Inner Mongolia Univ, Sch Phys Sci & Technol, Hohhot 010021, Peoples R China",
                                                                                                                           "orgid": "5f71b2c81c455f439fe3e365"},
                                                                                                                       {
                                                                                                                           "email": "nfzheng@xmu.edu.cn",
                                                                                                                           "id": "53f43464dabfaee4dc76fc7c",
                                                                                                                           "name": "Nanfeng Zheng"},
                                                                                                                       {
                                                                                                                           "email": "shen@imu.edu.cn",
                                                                                                                           "id": "5409518fdabfae450f476d54",
                                                                                                                           "name": "Hui Shen",
                                                                                                                           "org": "Inner Mongolia Univ, Coll Energy Mat & Chem, Hohhot 010021, Peoples R China",
                                                                                                                           "orgid": "5f71b2c81c455f439fe3e365"}],
                                                                                                                   "create_time": "2024-10-02T00:10:12.158Z",
                                                                                                                   "doi": "10.1021\u002Fjacs.4c10251",
                                                                                                                   "id": "66fc1bea01d2a3fbfc434b27",
                                                                                                                   "issn": "0002-7863",
                                                                                                                   "lang": "en",
                                                                                                                   "num_citation": 0,
                                                                                                                   "pages": {
                                                                                                                       "end": "27860",
                                                                                                                       "start": "27852"},
                                                                                                                   "title": "Anchoring Frustrated Lewis Pair Active Sites on Copper Nanoclusters for Regioselective Hydrogenation",
                                                                                                                   "update_times": {
                                                                                                                       "u_a_t": "2024-11-21T21:55:19Z",
                                                                                                                       "u_v_t": "2024-11-21T21:55:19Z"},
                                                                                                                   "urls": [
                                                                                                                       "https:\u002F\u002Fapi.crossref.org\u002Fworks\u002F10.1021\u002Fjacs.4c10251",
                                                                                                                       "http:\u002F\u002Fdx.doi.org\u002F10.1021\u002Fjacs.4c10251",
                                                                                                                       "https:\u002F\u002Fpubs.acs.org\u002Fdoi\u002F10.1021\u002Fjacs.4c10251"],
                                                                                                                   "venue": {
                                                                                                                       "info": {
                                                                                                                           "name": "JOURNAL OF THE AMERICAN CHEMICAL SOCIETY"},
                                                                                                                       "issue": "40",
                                                                                                                       "volume": "146"},
                                                                                                                   "versions": [
                                                                                                                       {
                                                                                                                           "id": "66fc1bea01d2a3fbfc434b27",
                                                                                                                           "sid": "10.1021\u002Fjacs.4c10251",
                                                                                                                           "src": "crossref",
                                                                                                                           "vsid": "JOURNAL OF THE AMERICAN CHEMICAL SOCIETY",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "66fc545a01d2a3fbfc910508",
                                                                                                                           "sid": "39352212",
                                                                                                                           "src": "pubmed",
                                                                                                                           "vsid": "7503056",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "673f2548ae8580e7ffb51276",
                                                                                                                           "sid": "WOS:001326699200001",
                                                                                                                           "src": "wos",
                                                                                                                           "vsid": "JOURNAL OF THE AMERICAN CHEMICAL SOCIETY",
                                                                                                                           "year": 2024}],
                                                                                                                   "year": 2024},
                                                                                                               {
                                                                                                                   "abstract": "Na metal batteries (NMBs) stand at the forefront of advancing energy storage technologies, but are severely hampered by Na dendrite issues, especially when using carbonate electrolytes. Suppressing the growth of Na dendrites through constructing NaF-rich solid-electrolyte-interphase (SEI) is a commonly-used strategy to prolong the lifespan of NMBs. In contrast, fluorinated organic SEI components are often underutilized. Inspired by unveiling the adsorption configuration of fluorinated organic compounds on the surface of Na metal, an optimized SEI architecture for stabilizing NMBs is proposed by investigating the C4H9SO2F-\u002FC4F9SO2F-treated Na metal anodes. It is revealed that the SEI built on a fluorinated inorganic\u002Forganic hybrid layer exhibit favorable Na passivation capability, significantly improving Na deposition behavior. As a result, the NMB with a high-loading cathode (15 mg cm-2) and a negative\u002Fpositive capacity ratio (N\u002FP) ratio of 4 shows a long-term life span over 1000 cycles with 92.8% capacity retention at 2 C. This work opens a new pathway for developing robust and high-energy-density NMBs. Stabilizing Na metal anodes is successfully achieved by using perfluoroalkane sulfonyl fluoride. Mechanism investigation reveals that constructing the SEI with a fluorinated inorganic\u002Forganic hybrid layer is beneficial to suppressing Na dendrite formation. The resulting Na metal anode enables the Na|Na3V2(PO4)3 full cell to deliver a remarkably enhanced cycling stability under high Na3V2(PO4)3 loading and low Na excess conditions. image",
                                                                                                                   "authors": [
                                                                                                                       {
                                                                                                                           "id": "654554c08a47b64923372ed9",
                                                                                                                           "name": "Chaozhi Wang",
                                                                                                                           "org": "Xiamen Univ, Coll Energy, Xiamen 361005, Fujian, Peoples R China",
                                                                                                                           "orgid": "5f71b2bd1c455f439fe3deb7"},
                                                                                                                       {
                                                                                                                           "id": "6334255f2fedb730e3a819de",
                                                                                                                           "name": "Shuqi Dai",
                                                                                                                           "org": "South China Univ Technol, Sch Emergent Soft Matter, Guangzhou 510640, Guangdong, Peoples R China"},
                                                                                                                       {
                                                                                                                           "name": "Kaihang Wu",
                                                                                                                           "org": "Xiamen Univ, Pen Tung Sah Inst Micronano Sci & Technol, Xiamen 361005, Fujian, Peoples R China",
                                                                                                                           "orgid": "5f71b2bd1c455f439fe3deb7"},
                                                                                                                       {
                                                                                                                           "name": "Shuchang Liu",
                                                                                                                           "org": "Xiamen Univ, Pen Tung Sah Inst Micronano Sci & Technol, Xiamen 361005, Fujian, Peoples R China",
                                                                                                                           "orgid": "5f71b2bd1c455f439fe3deb7"},
                                                                                                                       {
                                                                                                                           "id": "53f433e6dabfaee2a1ccddbd",
                                                                                                                           "name": "Jingqin Cui",
                                                                                                                           "org": "Xiamen Univ, Pen Tung Sah Inst Micronano Sci & Technol, Xiamen 361005, Fujian, Peoples R China",
                                                                                                                           "orgid": "5f71b2bd1c455f439fe3deb7"},
                                                                                                                       {
                                                                                                                           "id": "5612bf2245ce1e5962d8aa7c",
                                                                                                                           "name": "Yu Shi",
                                                                                                                           "org": "Chongqing Univ, Key Lab Low grade Energy Utilizat Technol & Syst, Chongqing 400030, Peoples R China",
                                                                                                                           "orgid": "5f71b2ad1c455f439fe3d768"},
                                                                                                                       {
                                                                                                                           "email": "xinruicao@xmu.edu.cn",
                                                                                                                           "id": "56294d4645ce1e5966347770",
                                                                                                                           "name": "Xinrui Cao",
                                                                                                                           "org": "Xiamen Univ, Dept Phys, Xiamen 361005, Fujian, Peoples R China",
                                                                                                                           "orgid": "5f71b2bd1c455f439fe3deb7"},
                                                                                                                       {
                                                                                                                           "id": "53f31a1edabfae9a8442fac7",
                                                                                                                           "name": "Qiulong Wei",
                                                                                                                           "org": "Xiamen Univ, Coll Mat, Xiamen 361005, Fujian, Peoples R China",
                                                                                                                           "orgid": "5f71b2bd1c455f439fe3deb7"},
                                                                                                                       {
                                                                                                                           "email": "x.l.fang@xmu.edu.cn",
                                                                                                                           "id": "53f386c6dabfae4b34a17bb3",
                                                                                                                           "name": "Xiaoliang Fang",
                                                                                                                           "org": "Xiamen Univ, Coll Energy, Xiamen 361005, Fujian, Peoples R China",
                                                                                                                           "orgid": "5f71b2bd1c455f439fe3deb7"},
                                                                                                                       {
                                                                                                                           "id": "53f43464dabfaee4dc76fc7c",
                                                                                                                           "name": "Nanfeng Zheng",
                                                                                                                           "org": "Fujian Sci & Technol Innovat Lab Energy Mat China, Xiamen 361005, Fujian, Peoples R China"}],
                                                                                                                   "create_time": "2024-10-01T15:40:10.041Z",
                                                                                                                   "doi": "10.1002\u002Faenm.202402711",
                                                                                                                   "id": "66fba4a401d2a3fbfc9fd4aa",
                                                                                                                   "issn": "1614-6832",
                                                                                                                   "keywords": [
                                                                                                                       "fluorinated organic components",
                                                                                                                       "sodium metal anodes",
                                                                                                                       "sodium metal batteries",
                                                                                                                       "solid electrolyte interphase"],
                                                                                                                   "lang": "en",
                                                                                                                   "num_citation": 0,
                                                                                                                   "title": "Highly Stable Sodium Metal Batteries Enabled by Manipulating the Fluorinated Organic Components of Solid-Electrolyte-Interphase",
                                                                                                                   "update_times": {
                                                                                                                       "u_a_t": "2024-11-21T21:48:24Z",
                                                                                                                       "u_v_t": "2024-11-21T21:48:24Z"},
                                                                                                                   "urls": [
                                                                                                                       "https:\u002F\u002Fapi.crossref.org\u002Fworks\u002F10.1002\u002Faenm.202402711",
                                                                                                                       "http:\u002F\u002Fdx.doi.org\u002F10.1002\u002Faenm.202402711",
                                                                                                                       "https:\u002F\u002Fonlinelibrary.wiley.com\u002Fdoi\u002F10.1002\u002Faenm.202402711"],
                                                                                                                   "venue": {
                                                                                                                       "info": {
                                                                                                                           "name": "ADVANCED ENERGY MATERIALS"}},
                                                                                                                   "versions": [
                                                                                                                       {
                                                                                                                           "id": "66fba4a401d2a3fbfc9fd4aa",
                                                                                                                           "sid": "10.1002\u002Faenm.202402711",
                                                                                                                           "src": "crossref",
                                                                                                                           "vsid": "ADVANCED ENERGY MATERIALS",
                                                                                                                           "year": 2024},
                                                                                                                       {
                                                                                                                           "id": "6711c83301d2a3fbfc677dd1",
                                                                                                                           "sid": "WOS:001321612600001",
                                                                                                                           "src": "wos",
                                                                                                                           "vsid": "ADVANCED ENERGY MATERIALS",
                                                                                                                           "year": 2024}],
                                                                                                                   "year": 2024}],
                                                                                               "profilePubsTotal": 443,
                                                                                               "profilePatentsPage": 0,
                                                                                               "profilePatents": null,
                                                                                               "profilePatentsTotal": null,
                                                                                               "profilePatentsEnd": false,
                                                                                               "profileProjectsPage": 1,
                                                                                               "profileProjects": {
                                                                                                   "success": true,
                                                                                                   "msg": "", "data": [
                                                                                                       {"country": "CN",
                                                                                                        "end_date": {
                                                                                                            "seconds": 1325289600},
                                                                                                        "fund_amount": 370000,
                                                                                                        "fund_currency": "CNY",
                                                                                                        "id": "60b8bdde6023d0724eb1dc45",
                                                                                                        "project_source": "NSFC",
                                                                                                        "start_date": {
                                                                                                            "seconds": 1230768000},
                                                                                                        "titles": [{
                                                                                                                       "contents": [
                                                                                                                           "大尺寸分立金属硫族纳米团簇的合成、组装及性能研究"],
                                                                                                                       "language": "ZH"}]},
                                                                                                       {"country": "CN",
                                                                                                        "end_date": {
                                                                                                            "seconds": 1483142400},
                                                                                                        "fund_amount": 2800000,
                                                                                                        "fund_currency": "CNY",
                                                                                                        "id": "60b8be226023d0724eb30420",
                                                                                                        "project_source": "NSFC",
                                                                                                        "start_date": {
                                                                                                            "seconds": 1325376000},
                                                                                                        "titles": [{
                                                                                                                       "contents": [
                                                                                                                           "贵金属催化材料的多级纳米结构调控与性能优化"],
                                                                                                                       "language": "ZH"}]},
                                                                                                       {"country": "CN",
                                                                                                        "end_date": {
                                                                                                            "seconds": 1577750400},
                                                                                                        "fund_amount": 2700000,
                                                                                                        "fund_currency": "CNY",
                                                                                                        "id": "60b8be906023d0724eb468cb",
                                                                                                        "project_source": "NSFC",
                                                                                                        "start_date": {
                                                                                                            "seconds": 1420070400},
                                                                                                        "titles": [{
                                                                                                                       "contents": [
                                                                                                                           "大尺寸金属纳米团簇及其在研究金属纳米颗粒表界面化学中的应用"],
                                                                                                                       "language": "ZH"}]},
                                                                                                       {"country": "CN",
                                                                                                        "end_date": {
                                                                                                            "seconds": 1388448000},
                                                                                                        "fund_amount": 2000000,
                                                                                                        "fund_currency": "CNY",
                                                                                                        "id": "60b8bde76023d0724eb2059f",
                                                                                                        "project_source": "NSFC",
                                                                                                        "start_date": {
                                                                                                            "seconds": 1262304000},
                                                                                                        "titles": [{
                                                                                                                       "contents": [
                                                                                                                           "纳米团簇、颗粒及其超结构的化学构建与应用"],
                                                                                                                       "language": "ZH"}]}],
                                                                                                   "total": 4,
                                                                                                   "log_id": "2qHwp4wcoF9btTobW2FV516kMV4"},
                                                                                               "profileProjectsTotal": 0,
                                                                                               "newInfo": null,
                                                                                               "checkDelPubs": []}};

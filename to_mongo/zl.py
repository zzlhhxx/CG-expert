from until.sql_tools import mongo_client, mysql_db_conn
import re
import json
from until.time_tool import timestamp_to_date_str
import datetime
conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()

mongo_db = mongo_client('cg')
c = mongo_db['zjwl_zl']
sql = 'select id,zl_id,zl_detail_path from aminer_zl where is_donwload_path=1 and is_to_mongo=0  order by id asc '
cur.execute(sql)
data = cur.fetchall()
print(len(data))
for item in data:
    ids, zl_id, zl_detail_path = item

    address = 'Z:/' + zl_detail_path

    # print(address)
    try:
        data = open(address, 'r', encoding='utf-8').read()

        json_data =json.loads(data)

        if json_data:

            patents = json_data['data'][0]
            if not patents:
                print('不完整')
                continue
            title = ''
            if patents.get("title"):
                for k1, v1 in patents['title'].items():

                    if k1 == 'en':
                        title = v1[0]
                    elif k1 == 'zh':
                        title = v1[0]
                    else:
                        title = v1[0]
                        # print(k1)
            summary = ''
            if patents.get("abstract"):
                for k2, v2 in patents['abstract'].items():
                    if k2 == 'en':
                        summary = v2[0]
                    elif k2 == 'zh':
                        summary = v2[0]
                    else:
                        summary = v2[0]
                        # print(k1)

            claims = ''

            if patents.get("claims"):
                for k3, v3 in patents['claims'].items():
                    if k3 == 'en':
                        claims = v3
                        # print(v3)
                    elif k3 == 'zh':
                        claims = v3
                    else:
                        claims = v3
                    if claims:
                        if len(claims):
                            claims = "\n".join(claims).strip()
            keywords = []

            kind = patents['pub_kind'] if patents.get('pub_kind') else ''  # 专利种类
            country = patents['country'] if patents.get("country") else ''

            pub_num = patents['pub_num'] if patents.get("pub_num") else ''  # 公开发布号

            country_ = ''
            for cc in country:
                country_ += cc.capitalize()  # 首字母大写

            num = country_ + pub_num + kind  # 专利号

            # 发明人和发明机构  设置列表append函数放入列表

            inventor_list = []
            if patents.get("inventor"):
                for inv in patents['inventor']:
                    inv_div = {
                        "name": inv['name'],
                        "organs": [],
                    }
                    if inv.get("person_id"):
                        person_id = inv['person_id']
                        inv_div['person_id'] = person_id

                    inventor_list.append(inv_div)
            ipc_list = []
            ipcs = patents.get("ipc")  # ipc
            if ipcs:
                for ipc in ipcs:
                    if not ipc.get("l4"):
                        continue
                    ipc_h = ipc['l4']
                    ipc_list.append({
                        'num': ipc_h,
                    })
            cpc_list = []
            cpcs = patents.get("cpc")  # ipc
            if cpcs:
                for cpc in cpcs:
                    if cpc.get("raw"):
                        cpc_h = cpc['raw']
                    else:
                        cpc_h = cpc['l4']
                    cpc_list.append({
                        'num': cpc_h,
                    })
            pub_date = ''
            if patents.get('pub_date'):
                pub_date = patents['pub_date']['seconds']

                if pub_date>0:
                    pub_date = timestamp_to_date_str(pub_date, '%Y-%m-%d')
                else:
                    pub_date = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=pub_date)
                print(pub_date)

            app_num = patents['app_num'] if patents.get("app_num") else ''  # 申请号
            app_date = patents.get("app_date")

            if app_date:
                app_date=app_date['seconds']

                if app_date>0:

                    if type(app_date)==type(1):

                        app_date = timestamp_to_date_str(app_date, '%Y-%m-%d')
                    else:
                        app_date = timestamp_to_date_str(app_date['seconds'], '%Y-%m-%d')
                else:
                    app_date = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=app_date)

            assignee = []
            if patents.get("assignee"):
                assignee_names = patents['assignee']  #
                for ass in assignee_names:
                    assignee.append({
                        "name": ass['name'],
                        "organs": [],
                    })
            applicant = []
            if patents.get("applicant"):
                applicant_names = patents['applicant']  #
                for appl in applicant_names:
                    applicant.append({
                        "name": appl['name'],
                        "organs": [],
                    })
                # print(applicant_names)
            law_status = ''  #
            cited_count_total = 0  # 申请人名
            net_address = f"https://www.aminer.cn/patent/{patents['id']}"
            pub_date=str(pub_date)
            app_date=str(app_date)
            pub_date=pub_date.replace("00:00:00","")
            app_date=app_date.replace("00:00:00","")
            print(pub_date,app_num)
            au_patent = {
                "_id": patents['id'],
                "title": title,
                "summary": summary,
                "claim": claims,
                "keywords": keywords,
                "num": num,
                "kind": kind,
                "country": country_,
                "inventors": inventor_list,
                "patentees": assignee,
                "ipc": ipc_list,
                "cpc": cpc_list,
                "pub_num": pub_num,
                "pub_date": pub_date,
                "app_num": app_num,
                "app_date": app_date,
                "assignee": applicant,
                "law_status": law_status,
                "cited_count_total": cited_count_total,
                "net_address": [net_address],
            }
            if not c.find_one({"_id": patents['id']}):
                c.insert_one(au_patent)
            update_ = 'update aminer_zl set is_to_mongo=1 where id=%s'
            cur.execute(update_, (ids,))
            conn.commit()
        else:
            print(zl_id, data)

    except Exception as e:
        print(e, ' ', address, ids,app_date)

# import requests
#
# url = f'https://backend.aminer.cn/api/v0/dataCenterPro/gateway/api/v3/patent/detail?id=63eac1d0675b80cf8c6cf347'
#
# # res = requests.get(url=url, headers=he, proxies=proxy, timeout=10)
# res = requests.get(url=url, timeout=10)
# print(res.json())

dddd = {'global': {'collapsed': False, 'preventRender': False, 'isCompanyIp': False}, 'patent': {'patent': {
    'abstract': {'en': [
        'A method of modifying the structure of a perovskite film prepared on a substrate, wherein an organic or inorganic salt crown ether complex is applied on a free surface of the so-prepared perovskite film. A perovskite solar cell, wherein a perovskite layer of said perovskite solar cell contains an organic or inorganic salt presenting a graded concentration within said perovskite layer , the highest concentration of said organic or inorganic salt existing in vicinity of the perovskite layer surface distal to the substrate of said perovskite layer .']},
    'all_kind_versions': [{'id': '62b18d9be1382377b20508c2', 'pub_kind': 'A1'},
                          {'id': '655d83465443cf554be323c2', 'pub_kind': 'B1'}],  # 版本
    'app_date': {'seconds': 1594684800},
    'app_num': '20185783',
    'applicant': [{'name': 'Ecole Polytechnique Fédérale de Lausanne (EPFL)', 'sequence': 1}],
    'assignee': [{'name': 'EPFL ECOLE POLYTECHNIQUE FEDERALE LAUSAN (EPFL-C)', 'sequence': 1}],
    'claims': {'en': [
        'A method of modifying the structure of a perovskite film prepared on a substrate, characterised by the fact that an organic or inorganic salt crown ether complex is provided and that said organic or inorganic salt crown ether complex is applied on a free surface of the so-prepared perovskite film.',
        'Method according to claim 1, characterised by the fact that said organic or inorganic salt comprises an inorganic cation selected from the group consisting of: Tl + , Ag + , Li + , Na + , K + , Rb + , Cs + , Mg 2+ , Ca 2+ , Sr 2+ , Ba 2+ , Zn 2+ , Cu 2+ , Ni 2+ , Co 2+ , Cd 2+ , Ge 2+ , Sn 2+ , Pb 2+ , Hg 2+ , Al 3+ , Ga 3+ , In 3+ , Bi 3+ , Al 3+ , La 3+ , Ce 3+ , Eu 3+ , Th 4+ .',
        'Method according to claim 1 or 2, characterised by the fact that said organic or inorganic salt comprises an organic cation selected from the group consisting of: wherein any of R 1 , R 2 , R 3 , R 4 , R 5 , R 6 is independently selected from: - H, provided that at least one of R 1 , R 2 , R 3 , R 4 , R 5 , R 6 connected to a heteroatom is not H; - a straight alkyl or branched alkyl containing 1-20 carbon atoms; or, - straight alkenyl or branched alkenyl containing 2-20 carbon atoms and one or more double bonds; - a straight alkynyl or branched alkynyl containing 2-20 carbon atoms and one or more triple bonds; - a saturated, partial saturated or completely unsaturated cyclic alkyl containing 3-7 carbon atom.',
        'Method according to claim 3, characterised by the fact that said substituents R 1 , R 2 , R 3 , R 4 , R 5 , R 6 of the organic cations may be independently selected from -H, -CH 3 , - C 2 H 5 , -C 3 H 7 , -CH(CH 3 ) 2 , -C 4 H 9 , -C(CH 3 ) 3 , -C 5 H 11 , -C 6 H 13 , -C 7 H 15 , -C 8 H 17 , -C 9 H 19 , - C 10 H 21 , -C 12 H 25 , -C 20 H 41 , -OCH 3 , -OCH(CH 3 ) 2 , -CH 2 OCH 3 , -C 2 H 4 OCH(CH 3 ) 2 , -SCH 3 , - SCH(CH 3 ) 2 , -C 2 H 4 SC 2 H 5 , -C 2 H 4 SCH(CH 3 ) 2 , -S(O)CH 3 , -SO 2 CH 3 , -SO 2 C 2 H 5 , -SO 2 C 3 H 7 , - SO 2 CH(CH 3 ) 2 , -CH 2 SO 2 CH 3 , -OSO 2 CH 3 , -OSO 2 CF 3 , -CH 2 NHC 2 H 5 , -N(CH 3 )C 3 H 5 , - N(CH 3 )CF 3 , -O-C 4 H 8 -O-C 4 H 9 , -S-C 2 H 4 -N(C 4 H 9 ) 2 , -OCF 3 , -S(O)CF 3 , -SO 2 CF 3 , -CF 3 , - C 2 F 5 , -C 3 F 7 , -C 4 F 9 , -C(CF 3 ) 3 , -CF 2 SO 2 CF 3 , -C 2 F 4 N(C 2 F 5 )C 2 F 5 , -CF=CF 2 , -C(CF 3 )=CFCF 3 , -CF 2 CF=CFCF 3 , -CF=CFN(CF 3 )CF 3 , -CFH 2 , -CHF 2 , -CH 2 CF 3 , -C 2 F 2 H 3 , -C 3 FH 6 , - CH 2 C 3 F 7 , -C(CFH 2 ) 3 , -CHO, -C(O)OH, -CHC(O)OH, -CH 2 C(O)C 2 H 5 , -CH 2 C(O)OCH 3 , - CH 2 C(O)OC 2 H 5 , -C(O)CH 3 , -C(O)OCH 3 ,',
        'Method according to one of the preceding claims,, characterised by the fact that said organic or inorganic salt comprises an anion selected from the group consisting of: F - , I - , Br - , Cl - , [N(CN) 2 ] - , [N(SO 2 CF 3 ) 2 ] - , [PF 6 ] - , [BF 4 ] - , [NO 3 ] - , [C(CN) 3 ] - , [B(CN) 4 ] - , [CF 3 COO] - , [ClO 4 ] - , [RSO 3 ] - , [(RSO 2 ) 2 N] - , [(RSO 2 ) 3 C], [(FSO 2 ) 3 C] - , [RCH 2 OSO 3 ] - , [RC(O)O] - , [CCl 3 C(O)O] - , [(CN) 2 CR] - , [(R 1 O(O)C) 2 CR] - , [P(C n F 2n+1-m H m ) y F 6-y ] - , [P(C 6 H 5 ) y F 6-y ] - , [R 1 2 P(O)O] - , [R 1 P(O)O 2 ] 2- , [(R 1 O) 2 P(O)O] - , [(R 1 O)P(O)O 2 ] 2- , [(R 1 O)(R 1 )P(O)O] - , [R 2 P(O)O] - , [RP(O)O 2 ] - , [BP 2 R 4-Z ] - , [BF Z (CN) 4-Z ] - , [B(C 6 F 5 ) 4 ] - , [B(OR 1 ) 4 ] - , [N(CF 3 ) 2 ] - , [AlCl 4 ] - or [SiF 6 ] 2- ; wherein: - n is an integer 1-20; m is 0, 1, 2, or 3; y is 0, 1, 2, 3 or 4; z is 0, 1, 2, or 3; R and R 1 are independently selected from: - completely fluorinated alkyl containing 1-20 carbon atoms; - completely fluorinated alkenyl containing 2-20 carbon atoms and one or more double bonds; or, - completely fluorinated phenyl; or, saturated, partially unsaturated and or completely unsaturated cycloalkyl; or saturated, partially unsaturated and/ or completely unsaturated perfluoroalkyl.',
        'Method according to one of the preceding claims,, characterised by the fact that said crown ether is selected from the group consisting of: 12-crown-[4], 15-crown-[5], 18-crown-[6], benzo-18-crown-[6], dibenzo-18-crown-[6], [2,4]-dibenzo-18-crown-[6], dibenzo-21-crown-[7], dibenzo-24-crown-[8], dibenzo-30-crown-[10], dicyclohexyl-18-crown-[6], N-phenylaza-15-crown-[5], 4\',4"(5")-di-tert-butyldicyclohexano-18-crown-[6], 1,4,8,12-tetraazacyclopentadecane, 1,4,8,11-tetrathiacyclotetradecane, hexacyclen, 1,5,9,13-Tetrathiacyclohexadecane, 1-aza-18-crown-[6], diaza-18-crown-[6], hexaza-18-crown-[6], hexathia-18-crown-[6] and a mixture thereof.',
        'Method according to one of the preceding claims, characterised by the fact that said so prepared perovskite film is formed by depositing perovskite precursors in a first solution in a first solvent onto said substrate and thereafter submitting the substrate covered by said first solution to a first annealing step.',
        'Method according to one of the preceding claims, characterised by the fact that said organic or inorganic salt crown ether complex is applied in a second solution in a second solvent, wherein said second solvent is orthogonal to said first solvent versus said perovskite.',
        'Method according to the preceding claims, characterised by the fact that after the application step of said organic or inorganic salt crown ether complex, said substrate with said perovskite film and with said applied organic or inorganic salt crown ether complex is submitted to a second annealing step.',
        'Method according to one of the preceding claims, characterised by the fact that said substrate is part of an optoelectronic device selected from the group consisting of perovskite solar cells, perovskite light-emitting diodes, and perovskite photodetectors.',
        'Method according to one of the preceding claims, characterised by the fact that said perovskite material comprises FAPbI 3 .',
        'Method according to one of the preceding claims, characterised by the fact that said organic or inorganic salt is an alkali metal halide salt.',
        'Method according to the preceding claim, characterised by the fact that said alkali metal salt is CsI.',
        'Method according to one of the preceding claims, characterised by the fact that said crown ether is dibenzo-21-crown-[7] and said alkali metal halide is CsI.',
        'A perovskite solar cell, characterised by the fact that a perovskite layer of said perovskite solar cell contains an organic or inorganic salt presenting a graded concentration within said perovskite layer , the highest concentration of said organic or inorganic salt existing in vicinity of the perovskite layer surface distal to the substrate of said perovskite layer.',
        'A perovskite solar cell according to the preceding claim, characterised by the fact that said perovskite material comprises FAPbI 3 and said organic or inorganic salt is CsI.']},
    'country': 'ep', 'cpc': [{'l1': 'H', 'l2': 'H01', 'l3': 'H01L', 'l4': 'H01L51/4226',
                              'raw': 'H01L  51/4226      20130101 FI20201201BHEP'},
                             {'l1': 'H', 'l2': 'H01', 'l3': 'H01L', 'l4': 'H01L51/002',
                              'raw': 'H01L  51/002       20130101 LI20201201BHEP'}],
    'description': {'en': [
        "[0001]The project leading to this application has received funding from the European Union's Horizon 2020 research and innovation programme under grant agreements No 785219, 881603 and 764047.",
        'Field of the invention',
        '[0002]The field of the invention relates to perovskite layers in perovskite based optoelectronic devices, in particular in perovskite based solar cells (PSCs).',
        '[0003]More specifically, the present invention pertains to a method of modifying the structure of a perovskite film prepared on a substrate, said substrate intended as a part of such a perovskite based optoelectronic device.',
        '[0004]The present invention pertains also to an optoelectronic device, in particular a perovskite solar cell, comprising a perovskite layer modified as mentioned above.',
        'Background of the invention and state of the art',
        '[0005]Perovskite optoelectronic devices e.g., perovskite solar cells, perovskite light-emitting diodes, and perovskite photodetectors, have drawn enormous attention with remarkably high performance and prospective for low-cost fabrication. In particular, hybrid metal halide perovskite materials have been successfully used as light absorbing layer in solar cells due to their facile preparation process as well as their excellent optoelectronic properties [1] . The power conversion efficiency (PCE) of perovskite solar cells reached about 23-25% during the past few years. A new certificated efficiency of 25.2% has recently been achieved in perovskite solar cells, which enables them as a very promising candidate to be used for next-generation photovoltaics.',
        '[0006]However, perovskite optoelectronic devices still suffer from poor stability caused by defects on the surface of and in the bulk perovskite film. These defects are formed in particular by the volatilization of some organic compounds, e.g. methylamine, formamidinium and methylammonium, during the thermal annealing process step of perovskite formation. Conventional surface passivation is a partial solution to remove such defects from the surface of perovskite films. [8] However, a number of defects remain in the bulk and it would be beneficial to develop a method that can simultaneously address both surface and bulk defects.',
        '[0007]Formamidinium lead iodide (FAPbI 3 ) is considered to be one of the best perovskite materials for photovoltaic applications due to its narrow bandgap. [5] However, the photoactive black α phase readily transforms to the undesired wide-bandgap δ phase under ambient conditions at room temperature. To address the thermodynamic instability of α- FAPbI3, it has been shown that incorporation of Cs ions in the precursor solution helps to stabilize the black α phase. However, this comes at the expense of the optimal bandgap and it is accompanied by detrimental defects in the bulk as well as on the surface of perovskite films, which limits further improvement of performance.',
        '[0008]Also, doping by means of additives has been employed in the art to tune the optical and electrical properties of perovskite materials. The inventors have found that a small amount of cesium iodide (CsI) incorporated into a perovskite precursor solution could increase the fill factor; however, the open-current voltage ( V oc ) cannot be improved a lot by this strategy.',
        'Objectives of the invention',
        '[0009]It is the object of the present invention to overcome the above-mentioned difficulties and to realize perovskite layers and films free from such defects.',
        'Solution according to the invention',
        '[0010]To this effect, the present invention proposes a method of modifying the structure of a perovskite film prepared on a substrate, wherein an organic or inorganic salt crown ether complex is applied on a free surface of the so-prepared perovskite film.',
        '[0011]The invention proposes thus a method to passivate the above-mentioned defects, in a post-deposition treatment on the as-formed perovskite films, by an organic or inorganic salt comprising an organic or inorganic cationic entity and an organic or inorganic anionic entity.',
        '[0012]Preferably, an inorganic cationic entity is selected from the group consisting of the following cations: Tl + , Ag + , Li + , Na + , K + , Rb + , Cs + , Mg 2+ , Ca 2+ , Sr 2+ , Ba 2+ , Zn 2+ , Cu 2+ , Ni 2+ , Co 2+ , Cd 2+ , Ge 2+ , Sn 2+ , Pb 2+ , Hg 2+ , Al 3+, Ga 3+ , In 3+ , Bi 3+ , Al 3+, La 3+ , Ce 3+ , Eu 3+ , Th 4+ . Preferably, an organic cationic entity of the component salt is selected from the group consisting of: wherein any R1, R2, R3, R4, R5, R6 is, independently one from the others: H, provided that at least one of R1, R2, R3, R4, R5, R6 connected to a heteroatom is not H; or a straight alkyl or branched alkyl containing 1-20 carbon atoms; or, straight alkenyl or branched alkenyl containing 2-20 carbon atoms and one or more double bonds; or a straight alkynyl or branched alkynyl containing 2-20 carbon atoms and one or more triple bonds; or a saturated, partial saturated or completely unsaturated cyclic alkyl containing 3-7 carbon atoms.',
        '[0013]Preferred substituents R1, R2, R3, R4, R5, R6 of the organic cations may be independently selected from -H, -CH 3 , -C 2 H 5 , -C 3 H 7 , -CH(CH 3 ) 2 , -C 4 H 9 , -C(CH 3 ) 3 , -C 5 H 11 , -C 6 H 13 , - C 7 H 15 , -C 8 H 17 , -C 9 H 19 , -C 10 H 21 , -C 12 H 25 , -C 20 H 41 , -OCH 3 , -OCH(CH 3 ) 2 , -CH 2 OCH 3 , - C 2 H 4 OCH(CH 3 ) 2 , -SCH 3 , -SCH(CH 3 ) 2 , -C 2 H 4 SC 2 H 5 , -C 2 H 4 SCH(CH 3 ) 2 , -S(O)CH 3 , - SO 2 CH 3 , -SO 2 C 2 H 5 , -SO 2 C 3 H 7 , -SO 2 CH(CH 3 ) 2 , -CH 2 SO 2 CH 3 , -OSO 2 CH 3 , -OSO 2 CF 3 , - CH 2 NHC 2 H 5 , -N(CH 3 )C 3 H 5 , -N(CH 3 )CF 3 , -O-C 4 H 8 -O-C 4 H 9 , -S-C 2 H 4 -N(C 4 H 9 ) 2 , -OCF 3 , - S(O)CF 3 , -SO 2 CF 3 , -CF 3 , -C 2 F 5 , -C 3 F 7 , -C 4 F 9 , -C(CF 3 ) 3 , -CF 2 SO 2 CF 3 , -C 2 F 4 N(C 2 F 5 )C 2 F 5 , - CF=CF 2 , -C(CF 3 )=CFCF 3 , -CF 2 CF=CFCF 3 , -CF=CFN(CF 3 )CF 3 , -CFH 2 , -CHF 2 , -CH 2 CF 3 , -C 2 F 2 H 3 , -C 3 FH 6 , -CH 2 C 3 F 7 , -C(CFH 2 ) 3 , -CHO, -C(O)OH, -CHC(O)OH, -CH 2 C(O)C 2 H 5 , - CH 2 C(O)OCH 3 , -CH 2 C(O)OC 2 H 5 , -C(O)CH 3 , -C(O)OCH 3 ,',
        '[0014]Preferably the anionic entity is selected from the group consisting of: F - , I - , Br - , Cl - , [N(CN) 2 ] - , [N(SO 2 CF 3 ) 2 ] - , [PF 6 ] - , [BF 4 ] - , [NO 3 ] - , [C(CN) 3 ] - , [B(CN) 4 ] - , [CF 3 COO] - , [ClO 4 ] - , [RSO 3 ], [(RSO 2 ) 2 N] - , [(RSO 2 ) 3 C] - , [(FSO 2 ) 3 C] - , [RCH 2O SO 3 ] - , [RC(O)O] - , [CCl 3 C(O)O] - , [(CN) 2 CR] - , [(R 1 O(O)C) 2 CR] - , [P(C n F 2n+1-m H m ) y F 6-y ] - , [P(C 6 H 5 ) y F 6-y ] - , [R 1 2 P(O)O] - , [R 1 P(O)O 2 ] 2- , [(R 1 O) 2 P(O)O] - , [(R 1 O)P(O) 2 ] 2- , [(R 1 O)(R 1 )P(O)O] - , [R 2 P(O)O] - , [RP(O)O 2 ] - , [BF 2 R 4-Z ] - , [BF Z (CN) 4-Z ] - , [B(C 6 F 5 ) 4 ] - , [B(OR 1 ) 4 ] - , [N(CF 3 ) 2 ] - , [AlCl 4 ] - or [SiF 6 ] 2- ; wherein: n is an integer 1-20; m is 0, 1, 2, or 3; y is 0, 1, 2, 3 or 4; z is 0, 1, 2, or 3; R and R 1 are independently selected from: completely fluorinated alkyl containing 1-20 carbon atoms; completely fluorinated alkenyl containing 2-20 carbon atoms and one or more double bonds; or, completely fluorinated phenyl; or, saturated, partially unsaturated and/ or completely unsaturated cycloalkyl, or saturated, partially unsaturated and/ or completely unsaturated perfluoroalkyl.',
        '[0015]The terminology « post-deposition treatment » is used herein to designate a treatment effected after completion of a deposition process of a perovskite film on a substrate, said deposition process including both application of perovskite components on a substrate and annealing of the film. This post-deposition treatment is realized by treating the as-prepared perovskite films with an organic or inorganic salt crown ether complex in an appropriate solution. The organic or inorganic salt can separate thereafter from the complex and diffuse into the bulk film through thermal annealing, to form a vertically graded concentration of organic or inorganic salt incorporated in the perovskite film. The invention thus offers a method that addresses both surface and bulk defects through a post-deposition treatment that achieves simultaneous modulation of the surface and bulk composition in perovskite films by forming a gradient organic or inorganic salt concentration within said structure.',
        '[0016]In particular, whereas a perovskite film is formed by depositing perovskite precursors in a first solution in a first solvent onto said substrate and thereafter submitting the substrate covered by a film of said first solution to a first annealing step, said organic or inorganic salt crown ether complex is applied in a second solution in a second solvent, wherein said second solvent is orthogonal to said first solvent versus said perovskite. After the application step of said organic or inorganic salt crown ether complex, said substrate with said perovskite film and with said applied organic or inorganic salt crown ether complex is preferably submitted to a second annealing step.',
        '[0017]In another aspect, the invention offers an optoelectronic device, in particular a perovskite solar cell, wherein a perovskite layer contains an organic or inorganic salt presenting a graded concentration within said perovskite layer, the highest concentration of said organic or inorganic salt existing in vicinity of the perovskite layer surface distal to the substrate of said perovskite layer.',
        '[0018]Other features and advantages of the present invention are mentioned in the dependent claims as well as in the following detailed description disclosing, with reference to the figures, preferred embodiments of the invention in more detail.',
        'Short description of the figures',
        '[0019]The attached figures exemplarily and schematically illustrate the principles as well as several embodiments of the present invention. Figure 1 : is a scheme of an (AX)-crown ether complex treatment. Figure 2 : 1 H NMR spectra of dibenzo-21-crown-[7] dissolved in dichloromethane-d 2 (top), and CsI-crown ether complex dissolved in dichloromethane-d 2 (bottom). Figure 3 : XPS spectra for Cs 3d (a) and O 1s (b) core-level spectra. (c) XPS depth profiles of Cs 3d spectra. Figure 4 : Top-view, SEM images of perovskite without (a) and with (b) CsI crown ether complex post-deposition treatment. Figure 5 : (a) V OC , FF, J SC and PCE matrix of PSCs with and without CsI-post-deposition treatment. (b) J-V curves of PSCs with and without CsI- post-deposition treatment. The inset shows the maxium power point tracking data. (c) J-V curves and (d) IPCE spectra of FAPbI 3 PSCs with and without CsI- post-deposition treatment. Figure 6 : J-V curves of typical PSCs with and without CsX- post-deposition treatment (X=F, Cl, Br). Figure 7 : Ambient stability of control perovskite film; (a) and (b) target perovskite film. XRD patterns of the perovskite films stored in an ambient environment for various times. The humidity and temperature are 60 ± 10% and 25 ± 1 °C, respectively. (c) Maximum power point tracking measured with the unencapsulated target device under full solar illumination (AM 1.5 G, 100 mW/cm 2 in N2, 25°C). Figure 8 : J-V curves of typical PSCs with and without AI post-deposition treatment (A=Li, Na, K, Rb).',
        'Detailed description of the invention',
        '[0020]In the following, embodiments of the invention shall be described in detail with reference to the above-mentioned figures.',
        '[0021]In one aspect, the invention is a processing method to passivate defects of perovskite layers by means of an organic or inorganic salt treatment on the as-formed perovskite films.',
        '[0022]Inorganic cations embodying the invention are: Tl + , Ag + , Li + , Na + , K + , Rb + , Cs + , Mg 2+ , Ca 2+ , Sr 2+ , Ba 2+ , Zn 2+ , Cu 2+ , Ni 2+ , Co 2+ , Cd 2+ , Ge 2+ , Sn 2+ , Pb 2+ , Hg 2+ , Al 3+, Ga 3+ , In 3+ , Bi 3+ , Al 3+, La 3+ , Ce 3+ , Eu 3+ , Th 4+ may be used. 2) Organic cations of the component salts embodying the invention are: wherein any R 1 , R 2 , R 3 , R 4 , R 5 , R 6 is independently selected from: H, provided that at least one R connected to a heteroatom is not H; a straight alkyl or branched alkyl containing 1-20 carbon atoms; or, straight alkenyl or branched alkenyl containing 2-20 carbon atoms and one or more double bonds; a straight alkynyl or branched alkynyl containing 2-20 carbon atoms and one or more triple bonds; a saturated, partial saturated or completely unsaturated cyclic alkyl containing 3-7 carbon atom. Preferred substituents R 1 , R 2 , R 3 , R 4 , R 5 , R 6 of the organic cations are -H, -CH 3 , -C 2 H 5 , - C 3 H 7 , -CH(CH 3 ) 2 , -C 4 H 9 , -C(CH 3 ) 3 , -C 5 H 11 , -C 6 H 13 , -C 7 H 15 , -C 8 H 17 , -C 9 H 19 , -C 10 H 21 , - C 12 H 25 , -C 20 H 41 , -OCH 3 , -OCH(CH 3 ) 2 , -CH 2 OCH 3 , -C 2 H 4 OCH(CH 3 ) 2 , -SCH 3 , - SCH(CH 3 ) 2 , -C 2 H 4 SC 2 H 5 , -C 2 H 4 SCH(CH 3 ) 2 , -S(O)CH 3 , -SO 2 CH 3 , -SO 2 C 2 H 5 , -SO 2 C 3 H 7 , - SO 2 CH(CH 3 ) 2 , -CH 2 SO 2 CH 3 , -OSO 2 CH 3 , -OSO 2 CF 3 , -CH 2 NHC 2 H 5 , -N(CH 3 )C 3 H 5 , - N(CH 3 )CF 3 , -O-C 4 H 8 -O-C 4 H 9 , -S-C 2 H 4 -N(C 4 H 9 ) 2 , -OCF 3 , -S(O)CF 3 , -SO 2 CF 3 , -CF 3 , - C 2 F 5 , -C 3 F 7 , -C 4 F 9 , -C(CF 3 ) 3 , -CF 2 SO 2 CF 3 , -C 2 F 4 N(C 2 F 5 )C 2 F 5 , -CF=CF 2 , -C(CF 3 )=CFCF 3 , -CF 2 CF=CFCF 3 , -CF=CFN(CF 3 )CF 3 , -CFH 2 , -CHF 2 , -CH 2 CF 3 , -C 2 F 2 H 3 , -C 3 FH 6 , - CH 2 C 3 F 7 , -C(CFH 2 ) 3 , -CHO, -C(O)OH, -CHC(O)OH, -CH 2 C(O)C 2 H 5 , -CH 2 C(O)OCH 3 , - CH 2 C(O)OC 2 H 5 , -C(O)CH 3 , -C(O)OCH 3 , 3) Anions embodying the invention are F - , I - , Br - , Cl - , [N(CN) 2 ] - , [N(SO 2 CF 3 ) 2 ] - , [PF 6 ] - , [BF 4 ] - , [NO 3 ] - , [C(CN) 3 ] - , [B(CN) 4 ] - , [CF 3 COO] - , [ClO 4 ] - , [RSO 3 ] - , [(RSO 2 ) 2 N] - , [(RSO 2 ) 3 C] - , [(FSO 2 ) 3 C] - , [RCH 2 OSO 3 ] - , [RC(O)O] - , [CCl 3 C(O)O] - , [(CN) 2 CR] - , [(R 1 O(O)C) 2 CR] - , [P(C n F 2n+1-m H m ) y F 6-y ] - , [P(C 6 H 5 ) y F 6-y ] - [R 1 2 P(O)O] - , [R 1 P(O)O 2 ] 2- , [(R 1 O) 2 P(O)O] - , [(R 1 O)P(O)O 2 ] 2- , [(R 1 O)(R 1 )P(O)O] - , [R 2 P(O)O] - , [RP(O)O 2 ] - , [BF 2 R 4-Z ] - , [BF Z (CN) 4-Z ] - , [B(C 6 F 5 ) 4 ] - , [B(OR 1 ) 4 ] - , [N(CF 3 ) 2 ] - , [AlCl 4 ] - or [SiF 6 ] 2- ; wherein: n is an integer 1-20; m is 0, 1, 2, or 3; y is 0, 1, 2, 3 or 4; z is 0, 1, 2, or 3; R and R 1 are independently selected from: completely fluorinated alkyl containing 1-20 carbon atoms; completely fluorinated alkenyl containing 2-20 carbon atoms and one or more double bonds; or, completely fluorinated phenyl; or, saturated, partially unsaturated and or completely unsaturated cycloalkyl; said cycloalkyl can be replaced by perfluoroalkyl.',
        '[0023]This processing method is realized by treating the as-formed perovskite films with an organic or inorganic salt-crown ether complex in a solution. Thereafter the organic or inorganic salt is able to separate from the complex and diffuse into the bulk perovskite film through thermal annealing, to form a vertically graded organic or inorganic salt-incorporated perovskite film.',
        '[0024]In a particular embodiment, the invention proposes a method to passivate above mentioned defects , by means of a post-deposition treatment on the as-formed perovskite films, by an alkali metal halide AX, wherein A=Li, Na, K, Rb, or Cs and X= F, Cl, Br or I. Figure 1 illustrates this process.',
        '[0025]Preparations of perovskite films on substrates forming parts of optoelectronic devices are nowadays largely known in the art, so that a general description thereof is not necessary here. For exemplary purposes, a cursorily description of the preparation of a organic-inorganic hybrid or inorganic perovskite film (B C 1 Y 3 ) film on a substrate suitable as part of a PSC is given hereunder, where B is CH 3 NH 3 + , CH 3 CH 2 NH 3 + , HC(NH 2 ) 2 + , C(NH 2 ) 3 + , C 6 H 5 CH 2 CH 2 NH 3 + , CH 3 (CH 2 ) 3 NH 3 + , (CH 3 ) 2 CHCH 2 NH 3 + , Cs + , or a mixture of them; C 1 is Pb, Sn, Bi, or an alloy thereof; Y is I, Cl, Br, SCN, or a mixture thereof, though embodiments are not limited thereto. The implementation of the present invention does not preclude the simultaneous use of additives in precursor solutions of perovskite films for conventional surface passivation to remove bulk defects.',
        '[0026]The polar solvents that are commonly used for dissolving organic or inorganic salts (e.g., water, dimethylformamide, dimethyl sulfoxide, etc.) could dissolve or damage the perovskite film. Therefore, these polar solvents cannot be employed to dissolve such salts for the post-deposition treatment.',
        '[0027]Crown ethers are known to serve as shuttles in a host-guest relationship for different organic and metal cations, such as in phase-transfer catalysis, forming host-guest complexes via ion-dipole interactions between the oxygen atoms of the macrocycle and the metal or organic cation, with remarkable selectivity for certain alkali metal ions as determined by the size of the macrocycle. [9,10] This property is used in the framework of the present invention to transfer organic or inorganic salts, in particular AX salts, onto the perovskite film by dissolving the host-guest complex in an orthogonal non-polar solvent. For example, dibenzo-21-crown-7 (DB21C7) presents a good size complementarity of its cavity (3.4-4.3 Å) with Cs + cations (3.3 Å), forming a well-defined host-guest complex ( Fig. 2 ). The dibenzo-21-crown-[7] is rationally chosen because its cavity is of sufficient size (3.4-4.3 Å) to coordinate the Cs+ cations (3.3 Å) via weak van der Waals interactions with the lone electron pairs of the oxygen atoms within the ring structure, forming a CsI crown ether complex. Moreover, this complex is soluble in non-polar solvents, which is compatible with solution-processing of the perovskite film.',
        '[0028]Organic or inorganic salt crown ether complexes are synthesized by mixing a crown ether and an organic or inorganic salt in an ultra-dry solvent and stirring, preferably at a selected warm temperature as disclosed hereunder, for several days. Upon finish, the solution is preferably filtered and directly used for device fabrication. The concentration of organic or inorganic salt crown ether complex in the solution is controlled by the amount of crown ether. The synthesis of a CsI-DB21C7 complex is detailed as an example hereunder.',
        '[0029]The crown ether used in this method can be 12-crown-[4], 15-crown-[5], 18-crown-[6], benzo-18-crown-[6], dibenzo-18-crown-[6], [2,4]-dibenzo-18-crown-[6], dibenzo-21-crown-[7], dibenzo-24-crown-[8], dibenzo-30-crown-[10], dicyclohexyl-18-crown-[6], N- phenylaza-15-crown-[5], 4\', 4" (5")-di- tert -butyldicyclohexano-18-crown-[6], 1,4,8,12-tetraazacyclopentadecane, 1,4,8,11-tetrathiacyclotetradecane, hexacyclen, 1,5,9,13-Tetrathiacyclohexadecane, 1-aza-18-crown-[6], diaza-18-crown-[6], hexaza-18-crown-[6], hexathia-18-crown-[6] or a mixture thereof.',
        '[0030]The solvent used for the synthesis of an organic or inorganic salt crown ether complex , which is preferably also to be used in the deposition step of the inventive method can be toluene, n -hexane, chloroform, iodobenzene, chlorobenzene, anisole, ethyl acetate, methyl acetate, sec -butanol, acetonitrile, or a mixture thereof.',
        '[0031]The reaction duration time for the synthesis of organic or inorganic salt crown ether complex can be, for example, any of the following values, about any of the following values, at least any of the following values, no more than any of the following values, or within any range having any of the following values as endpoints (all values are in hours), though embodiments are not limited thereto: 1, 5, 10, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175 or 180.',
        '[0032]The reaction temperature for the synthesis of organic or inorganic salt crown ether complex can be, for example, any of the following values, about any of the following values, at least any of the following values, no more than any of the following values, or within any range having any of the following values as endpoints (all values are in Celsius degree), though embodiments are not limited thereto: 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145 or 150.',
        '[0033]The process of organic or inorganic salt crown ether complex treatment is schematically represented in Fig. 1 and is described as follows. Firstly, the organic or inorganic salt crown ether complex solution is coated on the as-prepared perovskite film. Several application methods may be implemented in applying said organic or inorganic salt crown ether complex onto the so-prepared perovskite film and may be chosen by those skilled in the art in particular among spin-coating, spray-coating, immersion, etc... After that, thermal annealing treatment is employed to promote the diffusion of the salt into the bulk of perovskite film for several minutes. This treatment significantly modifies the composition (both surface and bulk) and surface morphology of perovskite films. As a consequence, the performance and stability of perovskite solar cells are improved simultaneously.',
        '[0034]The thermal temperature of the organic or inorganic salt crown ether complex treated perovskite can be, for example, any of the following values, about any of the following values, at least any of the following values, no more than any of the following values, or within any range having any of the following values as endpoints (all values are in Celsius degree), though embodiments are not limited thereto: 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200, 205, 210, 215, 220, 225, 230, 235, 240, 245, 250, 255, 260, 265, 270, 275, 280, 285, 290, 295 or 300.',
        '[0035]The duration time of the organic or inorganic salt crown ether complex treatment can be, for example, any of the following values, about any of the following values, at least any of the following values, no more than any of the following values, or within any range having any of the following values as endpoints (all values are in minutes), though embodiments are not limited thereto: 1, 5, 10, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175 or 180.',
        '[0036]Thus, the whole post deposition treatment may be summarized as follows: Crown-ether + AX → AX(crown-ether)complex (1) x AX(crown ether) complex + BC 1 Y 3 → AX.BC 1 Y 3 + x crown ether (2)',
        '[0037]After the organic or inorganic salt crown ether complex treatment, additional layer with 2D materials can be coated. The 2D materials can be graphite, graphene, doped graphene, graphene oxide, doped graphene oxide, molybdenum disulfide, hafnium disulfide, tungsten diselenide, MXenes, graphitic carbon nitride.',
        'Example 1: treatment of a perovskite film with CsI', 'a) Preparation of a perovskite layer on a substrate.',
        '[0038]An F-doped SnO 2 FTO conductive glass substrate is cleaned with solvents, dried with compressed air, and UV-Ozone treatment for 15 min is applied for further cleaning. Compact TiO 2 (c-TiO 2 ) is deposited on top of FTO using spray pyrolysis. After spray pyrolysis, the FTO/c-TiO 2 substrate is allowed to heat at 450 °C for 30 min before cooling down. Mesoscopic TiO 2 (mp-TiO 2 ) is applied by spin-coating of a diluted solution of TiO 2 -30 NRD paste, then sintering at 450 °C for 60 minutes to obtain mp-TiO 2 substrate. A 0.1M LiTFSI solution is then coated on the mp-TiO 2 and another sintering process at 450 °C for 30 min is conducted. The Li-treated mp-TiO 2 substrate is transferred to a dry box for device fabrication intermediately.',
        '[0039]For a (FAPbI 3 ) 1- x (MAPbBr 3 ) x precursor solution preparation, a mixture of PbI 2 , formamidinium iodide (FAI), methylammonium lead tribromide (MAPbBr 3 ) and methylammonium chloride (MACl) is dissolved in a mixed solution of DMF and DMSO (volume ration of DMF/DMSO of 4:1). For pure FAPbI 3 precursor solution preparation, a mixture of PbI 2 , FAI and MACl is dissolved in a mixed solution of DMF and DMSO (volume ration of DMF/DMSO of 4:1). For a Cs homogeneously doped perovskite, a CsI solution in DMSO is added to the (FAPbI 3 ) 1- x (MAPbBr 3 ) x precursor solution. The perovskite active layer is deposited using antisolvent method. The perovskite precursor solution is deposited on the freshly prepared FTO/c-TiO 2 /mp-TiO 2 substrate with a two-step spin-coating method at 1000 rpm for 10s and followed by 5000 rpm for 25 s. An effective amount of diethyl ether is applied at the last 10s. After spin-coating, the substrate is allowed to anneal at 150 °C for 10 min, then 100 °C for 10 min. The whole procedure is done in dry air.',
        'b) Synthesis of CsI-DB21C7 complex.',
        '[0040]CsI-DB21C7 complex is synthesized by mixing DB21C7 and CsI with 1:1.2 mole ratio in dry chlorobenzene and stirring at 50 °C for 7 days. The solution is filtered and used for device fabrication directly. The concentration of CsI-DB21C7 complex solution is controlled by the amount of crown ether. The complexation is subsequently verified by proton nuclear magnetic resonance ( 1 H NMR), where weak chemical shifts of approximately Δδ +0.01-0.05 ppm are observed upon coordination ( Figure 2 ).',
        'c) Post-deposition treatment.',
        '[0041]This CsI-DB21C7 complex is dissolved in chlorobenzene, which is « friendly » to perovskite, since it does not dissolve the latter. This CsI crown ether solution is used to treat the as- prepared perovskite film. The CsI-DB21C7 treatment is conducted by coating the as-prepared perovskite with a solution of CsI-DB21C7 complex solution with various concentrations. The solutions are kept on surface of the perovskite film for 2 s, and substantially spin-coated at 4000 rpm for 30 seconds. The treated perovskite films are allowed to anneal at 100 °C for 5 min. After, the treated perovskite films are washed with chlorobenzene for several times.',
        'd) Structural features of treated perovskite film.',
        '[0042]The surface and bulk composition of perovskite without and with cesium iodide induced post-deposition treatment were investigated by x-ray photoelectron spectroscopy (XPS). The Cs 3d spectra in Fig 3a shows obvious difference between control and target film. There is no Cs 3d signal in control film, while two peaks Cs 3 d 3/2 at 739.0 and Cs 3 d 5/2 at 725.0 eV exist in target film, which verifies that CsI has been successfully transferred onto treated perovskite film via the help of crown ether. The new peak of Ols at 533.1 eV (CO) in Fig. 3b exists in the target film, indicates some crown ether species still left on the surface of treated perovskite film. To confirm whether Cs diffuses into the bulk or not, depth profiles of XPS were conducted. As shown in Fig. 3c , the Cs 3d signals could be detected after sputtering of approximately 450 nm (level 13) in the perovskite film (thickness of ∼850 nm) after CsI-PDT. This result reveals that Cs gradually incorporates into the treated perovskite film from surface to bulk.',
        '[0043]The morphology of perovskite film with and without CsI-PDT was studied by scanning electron microscope (SEM). As shown in the Fig. 4 , the treated perovskite film shows larger grain size with some nanoneedles on the surface and few grain boundaries in the vertical direction.',
        'Example 2: Device performance of PSCs.',
        "[0044]The device performance of PSCs with and with CsI-PDT were investigated. A doped spiro-OMeTAD solution in chlorobenzene was spin-casted on the surface of the control and the treated perovskite films. Spiro-OMeTAD is doped by 23 µl LiTFSI (520 mg/mL in CH 3 CN) and 39.5 µl 4- tert -butyl pyridine, and 10 µl FK209 (375 mg/mL in ACN). The whole procedure is carried out in dry air (temperature<28°; relative humidity <15%). The device fabrication is completed with deposition of gold electrode (∼70 nm) by thermal evaporation. The PSCs present thus the following configuration: FTO/compact TiO 2 (∼60 nm)/ mesoporous-TiO 2 :perovskite composite layer (∼150 nm)/perovskite upper layer (∼650 nm)/ spiro-MeOTAD (∼150 nm)/Au (∼70 nm), and spiro- MeOTAD is 2,2',7,7'-Tetrakis[ N , N -di(4-methoxyphenyl)amino]-9,9'-spirobifluorene. As shown in Fig. 5a , the CsI-post-deposition treatment significantly improves the performance of PSCs compared to that of control. Especially the open-current voltage ( V OC ) improved from 1.08±0.01V to 1.17±0.01V and fill factor (FF) improved from 75.7±0.9% to 79.7±0.9%, which resulting in a significantly improvement of PCE (average) from 20.56±0.21% to 23.62±0.43%. Fig. 5b shows the current density-voltage (J-V) curves of the inventive target and control devices. The target PSC exhibited an open-current voltage ( V OC ) of 1.17 V, a short-circuit current ( J SC ) of 25.42 mA·cm -2 , and a fill factor (FF) of 81.7%, for a PCE of 24.29%. The control device showed an overall PCE of 21.08% with a V OC of 1.09 V, a J SC of 25.43 mA·cm -2 , and a FF of 76.0%. These values are further ascertained by recording scan speed-independent maximum power point tracking (MPP) measurement ( Fig. 5b insert) corresponding to PCEs of 20.5% and 23.9% for the control and target PSCs, respectively.",
        '[0045]Meanwhile, the CsI-Post Deposition Treatment can also be employed to fabricate highly efficient Br/MA- free FAPbI 3 PSCs. As shown in Fig. 5c , the V OC and FF of FAPbI 3 PSCs were improved from 0.99V to 1.03V and 0.768 to 0.782, respectively. As a result, the PCE was improved from 19.46% to 20.64% (stabilized efficiency of 20.9%). The J SC value obtained from the J-V characteristics is well matched (within 5%) with the IPCE ( Fig. 5d ).',
        'Example 3: Ambient stability of post-deposition treated/not treated perovskite films.',
        '[0046]The stability of perovskite films and relevant device without and with CsI- post-deposition treatment is compared. Firstly, the air stability of perovskite film by exposing to ambient environment is studied. The humidity and temperature are 60 ± 10% and 25 ± 1 °C, respectively. As shown in Fig. 7a , CsI post-deposition treatment significantly enhances the air stability of perovskite film. The treated perovskite film was stable in air more than 135 days, while the control film was completely degraded within 5 days ( Fig. 7b ). The enhanced air stability of perovskite film could arise from two aspects: (i) reduction of vacancy by CsI and (ii) moisture diffusion barrier formed by CsI crown ether complex. In addition, the long-term operational stability of the PSCs under one-sun illumination by maximum power point tracking was tested ( Fig. 7b ). The target device exhibits very high photostability, maintaining >95% of its initial PCE over 500 hours of irradiation. While the control device degraded to 60% of initial PCE in the first 100 hours. This operational stability enhancement can be attributed to both the reduction of defects in the interface of hole transport material/perovskite and the stabilization of the α-phase on FAPbI 3 by CsI-post-deposition treatment.',
        'Example 4. Other metal halides.',
        '[0047]Cesium salts with different halides (F, Cl, and Br) can also be employed by this method. Figure 6 shows the typical J-V curves for the PSCs without and with different CsX-PDT (x=F, Cl, Br). It is clear that cesium salt with other halides also can improve the PSCs performance. . Table 1. The photovoltaic parameters obtained from the J-V curves in Figure 6. V oc (V) J sc (mA/cm 2 ) FF PCE (%) Control 1.081 24.7 0.764 20.39 CsF-PDT 1.134 24.75 0.787 22.07 CsCl-PDT 1.121 24.99 0.775 21.69 CsBr-PDT 1.124 24.8 0.779 21.69',
        '[0048]Other alkali metal halides (AX, A=Li, Na, K, Rb) can be also transferred onto perovskite film with the assistance of a crown ether. Considering the different size of alkali metal cations, one may choose 15-crown-5 for LiX and NaX salts, dibenzo-18-crown-6 or benzo-18-crown-6 or 18-crown-6 and for KX salts, dibenzo-21-crown-7 for RbX salts. The synthesis and treatment are the same as for CsI. Figure 8 shows that different AI- post-deposition treatment (A=Li, Na, K, Rb) can also significantly improve the performance of PSCs, especially the V OC . Table 2. The photovoltaic parameters obtained from the J-V curves in Figure 8. V OC (V) J SC (mA/cm 2 ) FF PCE (%) Control 1.105 24.87 0.778 21.38 LiI-PDT 1.132 25.28 0.779 22.66 NaI-PDT 1.126 24.77 0.786 21.90 KI-PDT 1.171 24.79 0.796 23.10 RbI-PDT 1.185 24.85 0.802 23.61',
        'REFERENCES',
        '[0049]1 Correa-Baena, J.-P. et al. Homogenized halides and alkali cation segregation in alloyed organic-inorganic perovskites. Science 363, 627-631, doi:10.1126/science.aah5065 (2019 ). 2 Turren-Cruz, S.-H., Hagfeldt, A. & Saliba, M. Methylammonium-free, high-performance, and stable perovskite solar cells on a planar architecture. Science 362, 449-453 (2018 ). 3 Jeon, N. J. et al. Compositional engineering of perovskite materials for high-performance solar cells. Nature 517, 476-480, doi:10.1038/nature14133 (2015 ). 4 Ogomi, Y. et al. CH3NH3SnxPb(1-x)I3 Perovskite Solar Cells Covering up to 1060 nm. The Journal of Physical Chemistry Letters 5, 1004-1011, doi:10.1021/jz5002117 (2014 ). 5 Lin, R. et al. Monolithic all-perovskite tandem solar cells with 24.8% efficiency exploiting comproportionation to suppress Sn(ii) oxidation in precursor ink. Nature Energy 4, 864-873, doi:10.1038/s41560-019-0466-3 (2019 ). 6 Zhao, Y. & Zhu, K. Organic-inorganic hybrid lead halide perovskites for optoelectronic and electronic applications. Chemical Society Reviews 45, 655-689, doi:10.1039/C4CS00458B (2016 ). 7 Chen, H. et al. A solvent- and vacuum-free route to large-area perovskite films for efficient solar modules. Nature 550, 92-95, doi:10.1038/nature23877 (2017 ). 8 Saliba, M. et al. Cesium-containing triple cation perovskite solar cells: improved stability, reproducibility and high efficiency. Energy & Environmental Science 9, 1989-1997, doi:10.1039/C5EE03874J (2016 ). 9 Landini, D., Maia, A., Montanari, F. & Pirisi, F. M. Crown ethers as phase-transfer catalysts. A comparison of anionic activation in aqueous-organic two-phase systems and in low polarity anhydrous solutions by perhydrodibenzo-18-crown-6, lipophilic quaternary salts, and cryptands. J. Chem. Soc., Perkin Trans. 2, 46-51 (1980 ). 10 Steed, J. W. First-and second-sphere coordination chemistry of alkali metal crown ether complexes. Coord. Chem. Rev. 215, 171-221 (2001 ).']},
    'id': '62b18d9be1382377b20508c2',
    'inventor': [{'name': 'Zhang Hong', 'person_id': '562f947345cedb33997160c2', 'sequence': 1},
                 {'name': 'Zakeeruddin Shaik Mohammed', 'person_id': '53f45043dabfaeecd69d3ade', 'sequence': 2},
                 {'name': 'Graetzel Michael', 'person_id': '5440905edabfae7d84b8285f', 'sequence': 3}],
    'ipc': [{'l1': 'H', 'l2': 'H01', 'l3': 'H01L', 'l4': 'H01L051/00'},
            {'l1': 'H', 'l2': 'H01', 'l3': 'H01L', 'l4': 'H01L051/42'}],
    'ipcr': [{'l1': 'H', 'l2': 'H01', 'l3': 'H01L', 'l4': 'H01L51/42'},
             {'l1': 'H', 'l2': 'H01', 'l3': 'H01L', 'l4': 'H01L51/00'}], 'merge_id': '62b18d9be1382377b20508c2',
    'priority': [{'country': 'ep', 'date': {'seconds': 1594656000}, 'num': '185783'}],
    'pub_date': {'seconds': 1642550400}, 'pub_kind': 'A1', 'pub_num': '3940806',

    'reference': {
        'paper_references': [{
            'raw_text': 'CORREA-BAENA, J.-P. et al. Homogenized halides and alkali cation segregation in alloyed organic-inorganic perovskites Science 20190000 363 627 631 [0049]',
            'sequence': 1},
            {
                'raw_text': 'TURREN-CRUZ, S.-H. HAGFELDT, A. SALIBA, M. Methylammonium-free, high-performance, and stable perovskite solar cells on a planar architecture Science 20180000 362 449 453 [0049]',
                'sequence': 2},
            {
                'raw_text': 'JEON, N. J. et al. Compositional engineering of perovskite materials for high-performance solar cells Nature 20150000 517 476 480 [0049]',
                'sequence': 3},
            {
                'raw_text': 'OGOMI, Y. et al. CH3NH3SnxPb(1-x)I3 Perovskite Solar Cells Covering up to 1060 nm The Journal of Physical Chemistry Letters 20140000 5 1004 1011 [0049]',
                'sequence': 4},
            {
                'raw_text': 'LIN, R. et al. Monolithic all-perovskite tandem solar cells with 24.8% efficiency exploiting comproportionation to suppress Sn(ii) oxidation in precursor ink Nature Energy 20190000 4 864 873 [0049]',
                'sequence': 5},
            {
                'raw_text': 'ZHAO, Y. ZHU, K. Organic-inorganic hybrid lead halide perovskites for optoelectronic and electronic applications Chemical Society Reviews 20160000 45 655 689 [0049]',
                'sequence': 6},
            {
                'raw_text': 'CHEN, H. et al. A solvent- and vacuum-free route to large-area perovskite films for efficient solar modules Nature 20170000 550 92 95 [0049]',
                'sequence': 7},
            {
                'raw_text': 'SALIBA, M. et al. Cesium-containing triple cation perovskite solar cells: improved stability, reproducibility and high efficiency Energy & Environmental Science 20160000 9 1989 1997 [0049]',
                'sequence': 8},
            {
                'raw_text': 'LANDINI, D. MAIA, A. MONTANARI, F. PIRISI, F. M. Crown ethers as phase-transfer catalysts. A comparison of anionic activation in aqueous-organic two-phase systems and in low polarity anhydrous solutions by perhydrodibenzo-18-crown-6, lipophilic quaternary salts, and cryptands J. Chem. Soc., Perkin Trans. 19800000 2 46 51 [0049]',
                'sequence': 9},
            {
                'raw_text': 'STEED, J. W. First-and second-sphere coordination chemistry of alkali metal crown ether complexes Coord. Chem. Rev. 20010000 215 171 221 [0049]',
                'sequence': 10}]},
    'source': '{"cpc": {"_id": "63db573725ebf36900dad5a1", "src": "cnipa", "_col": "cnipa_patent_update", "meta_id": "63e3a1b3a6e19bfd32dad41f"}, "ipc": {"_id": "643fdc166a55949b1c1079e7", "src": "derwent", "_col": "patent_derwent", "meta_id": "63e42f3759aa5d9780146634"}, "ipcr": {"_id": "63db573725ebf36900dad5a1", "src": "cnipa", "_col": "cnipa_patent_update", "meta_id": "63e3a1b3a6e19bfd32dad41f"}, "agent": {"_id": "63db573725ebf36900dad5a1", "src": "cnipa", "_col": "cnipa_patent_update", "meta_id": "63e3a1b3a6e19bfd32dad41f"}, "title": {"de": {"_id": "63db573725ebf36900dad5a1", "src": "cnipa", "_col": "cnipa_patent_update", "meta_id": "63e3a1b3a6e19bfd32dad41f"}, "en": {"_id": "63db573725ebf36900dad5a1", "src": "cnipa", "_col": "cnipa_patent_update", "meta_id": "63e3a1b3a6e19bfd32dad41f"}, "fr": {"_id": "63db573725ebf36900dad5a1", "src": "cnipa", "_col": "cnipa_patent_update", "meta_id": "63e3a1b3a6e19bfd32dad41f"}}, "claims": {"en": {"_id": "63db573725ebf36900dad5a1", "src": "cnipa", "_col": "cnipa_patent_update", "meta_id": "63e3a1b3a6e19bfd32dad41f"}}, "abstract": {"en": {"_id": "63db573725ebf36900dad5a1", "src": "cnipa", "_col": "cnipa_patent_update", "meta_id": "63e3a1b3a6e19bfd32dad41f"}}, "app_date": {"_id": "63db573725ebf36900dad5a1", "src": "cnipa", "_col": "cnipa_patent_update", "meta_id": "63e3a1b3a6e19bfd32dad41f"}, "assignee": {"_id": "643fdc166a55949b1c1079e7", "src": "derwent", "_col": "patent_derwent", "meta_id": "63e42f3759aa5d9780146634"}, "auth_num": null, "inventor": {"_id": "63db573725ebf36900dad5a1", "src": "cnipa", "_col": "cnipa_patent_update", "meta_id": "63e3a1b3a6e19bfd32dad41f"}, "pct_info": null, "priority": {"_id": "643fdc166a55949b1c1079e7", "src": "derwent", "_col": "patent_derwent", "meta_id": "63e42f3759aa5d9780146634"}, "pub_date": {"_id": "63db573725ebf36900dad5a1", "src": "cnipa", "_col": "cnipa_patent_update", "meta_id": "63e3a1b3a6e19bfd32dad41f"}, "applicant": {"_id": "63db573725ebf36900dad5a1", "src": "cnipa", "_col": "cnipa_patent_update", "meta_id": "63e3a1b3a6e19bfd32dad41f"}, "auth_date": null, "reference": {"_id": "63db573725ebf36900dad5a1", "src": "cnipa", "_col": "cnipa_patent_update", "meta_id": "63e3a1b3a6e19bfd32dad41f"}, "description": {"en": {"_id": "63db573725ebf36900dad5a1", "src": "cnipa", "_col": "cnipa_patent_update", "meta_id": "63e3a1b3a6e19bfd32dad41f"}}, "ep_family_id": null}',
    'title': {'de': ['VERFAHREN ZUR MODIFIZIERUNG DER STRUKTUR VON PEROWSKITFILMEN'],
              'en': ['METHOD OF MODIFYING THE STRUCTURE OF PEROVSKITE FILMS'],
              'fr': ['PROCÉDÉ DE MODIFICATION DE LA STRUCTURE DE FILMS DE PÉROVSKITE']}}}}
ddd = {'success': True, 'msg': '',
       'data': [{'abstract': {'en': [
           'NOVELTY - The joint has a rotation output structure (2) composed of a first rectangular straight waveguide (5), a first arc guide wall (6) and a second circular arc guide wall (7). One narrow side of the first rectangular straight waveguide is connected with the first circular arc waveguide wall. Another side narrow side of the second arc guide wall is connected with a planar structure symmetrical of the first arc guide wall. An input structure (1) is composed of a second rectangular straight waveguide (3) and a circular rectangular waveguide (4). The second circular arc guide wall is embedded in the circular rectangular waveguide. An outer wall of the first circular waveguide wall, the second circular arc guide wall and a outer narrow side inner wall of the circular rectangular waveguide are firmly connected.',
           'USE - Rectangular waveguide H-plane rotary joint.',
           'ADVANTAGE - The joint has simple structure, high power capacity and transmission efficiency, and is connected through a rectangular waveguide array antenna array design and multi-channel.',
           "DESCRIPTION OF DRAWING(S) - The drawing shows a perspective view of a rectangular waveguide h-plane rotary joint. '(Drawing includes non-English language text)'",
           'Input structure (1)', 'Rotation output structure (2)', 'Rectangular straight waveguide (3,5)',
           'Circular rectangular waveguide (4)', 'Circular arc guide wall (6,7)']},
                 'all_kind_versions': [{'id': '63eac1d0675b80cf8c6cf347', 'pub_kind': 'B'},
                                       {'id': '63eb27c204c6eefad4897781', 'pub_kind': 'C'},
                                       {'id': '63386c76667297566c6c24f8', 'pub_kind': 'A'}],
                 'app_date': {'seconds': 1090195200}, 'app_num': '10069356',
                 'assignee': [{'name': 'UNIV NAT DEFENSE TECHNOLOGY (UNDT-C)', 'sequence': 1}],
                 'auth_date': {'seconds': 1626393600}, 'auth_num': '109687057', 'country': 'cn',
                 'id': '63eac1d0675b80cf8c6cf347',
                 'inventor': [{'name': 'ZHANG Q', 'sequence': 1}, {'name': 'ZHAO X', 'sequence': 2},
                              {'name': 'YUAN C', 'sequence': 3}, {'name': 'YU L', 'sequence': 4},
                              {'name': 'SUN Y', 'sequence': 5}],
                 'ipc': [{'l1': 'H', 'l2': 'H01', 'l3': 'H01P', 'l4': 'H01P001/06'}],
                 'merge_id': '63eac1d0675b80cf8c6cf347',
                 'priority': [{'country': 'cn', 'date': {'seconds': 1548288000}, 'num': '10069356'}],
                 'pub_date': {'seconds': 1109721600}, 'pub_kind': 'B', 'pub_num': '1587955', 'reference': {
               'patent_references': [{'patent_office': 'cn', 'raw_kind': 'A', 'raw_number': '1682407', 'sequence': 1},
                                     {'patent_office': 'us', 'raw_kind': 'A', 'raw_number': '2945193', 'sequence': 2}]},
                 'source': '{"cpc": null, "ipc": {"_id": "63dfc0f7413da8b2e16796f2", "src": "old_dupl", "_col": "patent_cnipa_old_dupl", "meta_id": "63e6814f652d1dd088658568"}, "ipcr": null, "agent": null, "title": [{"info": {"_id": "63dfc0f7413da8b2e16796f2", "src": "old_dupl", "_col": "patent_cnipa_old_dupl", "meta_id": "63e6814f652d1dd088658568"}, "language": "en"}], "claims": null, "abstract": [{"info": {"_id": "63dfc0f7413da8b2e16796f2", "src": "old_dupl", "_col": "patent_cnipa_old_dupl", "meta_id": "63e6814f652d1dd088658568"}, "language": "en"}], "app_date": {"_id": "63dfc0f7413da8b2e16796f2", "src": "old_dupl", "_col": "patent_cnipa_old_dupl", "meta_id": "63e6814f652d1dd088658568"}, "assignee": {"_id": "63dfc0f7413da8b2e16796f2", "src": "old_dupl", "_col": "patent_cnipa_old_dupl", "meta_id": "63e6814f652d1dd088658568"}, "auth_num": {"_id": "63dfc0f7413da8b2e16796f2", "src": "old_dupl", "_col": "patent_cnipa_old_dupl", "meta_id": "63e6814f652d1dd088658568"}, "inventor": {"_id": "63dfc0f7413da8b2e16796f2", "src": "old_dupl", "_col": "patent_cnipa_old_dupl", "meta_id": "63e6814f652d1dd088658568"}, "pct_info": null, "priority": {"_id": "63dfc0f7413da8b2e16796f2", "src": "old_dupl", "_col": "patent_cnipa_old_dupl", "meta_id": "63e6814f652d1dd088658568"}, "pub_date": {"_id": "63dfc0f7413da8b2e16796f2", "src": "old_dupl", "_col": "patent_cnipa_old_dupl", "meta_id": "63e6814f652d1dd088658568"}, "applicant": null, "auth_date": {"_id": "63dfc0f7413da8b2e16796f2", "src": "old_dupl", "_col": "patent_cnipa_old_dupl", "meta_id": "63e6814f652d1dd088658568"}, "reference": {"_id": "63dfc0f7413da8b2e16796f2", "src": "old_dupl", "_col": "patent_cnipa_old_dupl", "meta_id": "63e6814f652d1dd088658568"}, "description": null, "ep_family_id": null}',
                 'title': {'en': [
                     'Rectangular waveguide H-plane rotary joint, has first circular waveguide wall whose outer wall, second circular arc guide wall and outer narrow side inner wall of circular rectangular waveguide are firmly connected.']}}],
       'log_id': '2q1FexTdVaOLEAYeCJPxVCEkRz9'}

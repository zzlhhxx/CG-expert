
from until.time_tool import time_format

from until.sql_tools import mongo_client, mysql_db_conn
import re
import json

conn = mysql_db_conn(dbname='cg')
cur = conn.cursor()
mongo_db = mongo_client('cg')
c = mongo_db['zjwl_xm']
sql = 'select id,f_id,xm_id,xm_detail_path from aminer_xm where is_download_path=1 and is_to_mongo=0 and people=0 and source_id is null order by id asc '
# sql = 'select id,f_id,xm_id,xm_detail_path from aminer_xm where xm_id="6509144f3fda6d7f06e0335d" order by id asc'
cur.execute(sql)
data = cur.fetchall()
print(len(data))
for item in data:
    ids, f_id, xm_id, xm_detail_path = item
    print(f_id)
    address = 'Z:/' + xm_detail_path

    print(address)
    selec_sql = 'select aminer_id from paln_list_people where id=%s'
    cur.execute(selec_sql, (f_id,))
    aminer_id = cur.fetchone()[0]

    data = open(address, 'r', encoding='utf-8').read()

    json_data = json.loads(data)

    if not json_data.get("data") :
        print(json_data)
    else:
        dd = json_data['data'][0]
        country = dd.get("country")
        if dd.get("description"):
            summary_list = []
            description = dd['description']
            for desc in description:
                summary = desc['contents']
                language = desc['language']
                summary_list.append(summary[0].strip())
                if language != 'EN':
                    # pass
                    print(description)
            summary_str = "\n".join(summary_list).strip().replace("<br>", '\n')
        else:
            summary_str = ''

        title = dd['title']
        title_c = ''
        for tttt in title:
            # print(tttt)
            if tttt.get('language') == 'EN':
                title_c = '\n'.join(tttt['contents'])
            elif tttt.get('language') == 'ZH':
                title_c = '\n'.join(tttt['contents'])
        if not title_c:
            title_c = '\n'.join(title[0]['contents'])
        if not dd.get("start_date") or not dd.get("end_date"):
            pub_date = ''
            establish_year = ''
        else:
            pub_date = time_format(time_format=dd['start_date'])
            end_date = dd['end_date']
            establish_year = dd['start_date'][:4] + '-' + end_date[:4]
        authors = []
        if dd.get("person"):
            person = dd['person']
            for p in person:
                author = {
                    "name": p['name'],
                    "organs": "",
                    "type": p['role'].lower() if p.get("role") else '',
                }
                if p.get("person_id"):
                    author['_person_id'] = p['person_id']
                authors.append(author)
        if dd.get("keywords"):
            keywords = dd['keywords'][0]['contents']

        else:
            keywords = []
        au_project = {
            "_id": xm_id,
            "name": title_c,
            "summary": summary_str,
            "keywords": keywords,
            "authors": authors,
            "establish_year": establish_year,
            "pub_date": pub_date,
            "net_address": [f"https://www.aminer.cn/profile/{aminer_id}"],
        }

        if not c.find_one({"_id": xm_id}):
            c.insert_one(au_project)

        update_ = 'update aminer_xm set is_to_mongo=1 where id=%s'
        cur.execute(update_, (ids,))
        conn.commit()

accc = {'country': 'US', 'description':
    [{'contents': [
        '9971412<br/>De Heer<br/><br/>Electronic and mechanical properties of multi-walled carbon nanotubes have been widely investigated but are still only poorly understood. In this research these problems are attacked by means of a series of in situ electron microscopy experiments in which the properties of individual, well characterized nanotubes are measured.  These properties include the electronic transport, field emission, electrostatic potentials of the electrically charged nanotubes, and elastic constants.  The feasibility of such measurements have been demonstrated by a series of preliminary experiments which include (i) the making and breaking of electrical contacts involving nanotubes; (ii) in situ field emission; (iii) phase contrast effects of the charged nanotubes; and (iv) observations of electrically induced mechanical resonances.  The latter effect suggests a new approach towards nanomechanics.  This research offers many opportunities for the training of graduate students and postdoctoral research associates in a field which stands at the forefront of contemporary condensed matter physics and materials sciences.<br/>%%%<br/>Carbon nanotubes are nearly perfect graphitic tubes with remarkable properties among which are their exceptional mechanical strength, high current carrying capabilities, possible hydrogen storage capabilities, and others.  In order to characterize these properties and to discover new ones it is essential that carbon tubes be studied individually. The principal investigator has developed the required methods for such studies.  This research offers opportunities for the training of graduate students and postdoctoral research associates in an advanced technological field that offers many employment opportunities during the 21st Century.<br/>***<br/><br/><br/><br/>'],
        'language': 'EN'}],
        'end_date': '2004-05-31T00:00:00Z',
        'fund_amount': 293547,
        'fund_currency': 'USD',
        'id': '64d213e53fda6d7f065f1860',
        'organization': [{'address': {'city': 'ATLANTA',
                                      'country': 'United States',
                                      'detail_address': '926 DALNEY ST NW',
                                      'province': 'Georgia'},
                          'id': '65485741a48a1ca739d67c0f',
                          'name': 'Georgia Tech Research Corporation',
                          'organization_id': '5f71b3671c455f439fe429df',
                          'phone': '4048944819',
                          'project_id': '64d213e53fda6d7f065f1860',
                          'sequence': 0},
                         {
                             'address': {'city': 'ATLANTA',
                                         'country': 'United States',
                                         'detail_address': '926 DALNEY ST NW',
                                         'province': 'Georgia',
                                         'raw_address_info': '926 DALNEY ST NW'},
                             'id': '65485741a48a1ca739d67c10',
                             'name': 'Georgia Tech Research Corporation',
                             'organization_id': '5f71b3671c455f439fe429df',
                             'project_id': '64d213e53fda6d7f065f1860',
                             'role': 'performance',
                             'sequence': 1}],
        'organization_fund': [{'id': '65485741e8ec64db43d67c68', 'name': 'Direct For Mathematical & Physical Scien',
                               'project_id': '64d213e53fda6d7f065f1860', 'sequence': 0}],
        'person': [
            {'email': 'zhong.wang@mse.gatech.edu', 'id': '6552faf501098ba91a3b1f8d', 'name': 'Zhong L Wang',
             'person_id': '542ec5bbdabfae498ae3ae6b', 'project_id': '64d213e53fda6d7f065f1860',
             'role': 'Co-Principal Investigator', 'sequence': 1}],
        'project_kind': 'Grant',
        'project_number': '9971412',
        'project_source': 'NSF',
        'project_status': 'unknown',
        'start_date': '1999-06-15T00:00:00Z',
        'title': [{
            'contents': [
                'In Situ Electron Microscopy Investigation of Physical Properties of Multiwalled Carbon Nanotubes'],
            'language': 'EN'}]}

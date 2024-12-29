import requests
from lxml import etree

url='https://www.aminer.cn/profile/zhong-lin-wang/542ec5bbdabfae498ae3ae6b'
headers={
    'cookie':'_Collect_UD=yPhNgdwqnitfOZR7Bm1pk; _Collect_UD_Create_Time=Tue%20Nov%2026%202024%2010%3A32%3A48%20GMT+0800%20%28%u4E2D%u56FD%u6807%u51C6%u65F6%u95F4%29; _Collect_ISNEW=1732588368929; _YS_userAccect=fzeacHpNASq3F7GHLylPp; gr_user_id=e07522e6-01ed-4a75-9dd7-56a8f8d3ed39; gr_session_id_ae8dfb99e5e4cda1=064dfb85-c43a-4f3d-8310-7d07b8d9ca38; gr_session_id_ae8dfb99e5e4cda1_064dfb85-c43a-4f3d-8310-7d07b8d9ca38=true; searchType=person; aminer_access_token=%22eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhaWQiOiI2NzQ1MzVlZDVmYzViZTkzYjE5ZmNkNzgiLCJhdWQiOlsiYTIyNzI5OWMtMGZhNC00Y2JlLTk1YTgtYThhZjdjZTQ4MzdjIl0sImNpZCI6ImEyMjcyOTljLTBmYTQtNGNiZS05NWE4LWE4YWY3Y2U0ODM3YyIsImV4cCI6MTczMjU5MjYzNywiZ2VuZGVyIjowLCJpYXQiOjE3MzI1ODkwMzcsImlkIjoiNjc0NTM1ZWQ1ZmM1YmU5M2IxOWZjZDc4IiwiaXNzIjoib2F1dGguYW1pbmVyLmNuIiwianRpIjoiODFmMTRjY2MtZWVmMC00YTE4LTk4MTUtNzIyN2RkYzZhNmYxIiwibmJmIjoxNzMyNTg5MDM3LCJuaWNrbmFtZSI6IiIsInN1YiI6IjY3NDUzNWVkNWZjNWJlOTNiMTlmY2Q3OCIsInQiOiJQYXNzd29yZCJ9.loH5PheAhrQkc6rp45jPohaY8XwAxMIUtoP2A9y-KTi2xRdhEkUt6vtrqAOrjWnV-Kk2ow3F74FR_uhmFWWXEZmOb6g3cgo87nf3gjkiCMMgr9xeCfa35iMSVSZnlFxVsdrZ2itK_dRkvyXAYvtstNI2q8foD7mgqqo80tlMvrw4eQ-O1Nk4IrAkYFTTiZicqOrQoUbMPTpjD91_IDG-WSIGknpcCvz0SWwkuqnypwHTVyHmiCqNHPk64kjU2Bdo1qK2nx2dt95EcQZgofWEyYnQ8R0oJ8b7hA-mWdx6O7VUTX8nnDh65CCBSsXPkkQ9hIm13viEY3-5ts6Iu14gXA%22; aminer_refresh_token=%2250509834-d537-4925-8c9d-0acedb15c433%22; _Collect_SN=36',
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
           }

response=requests.post(url,headers=headers)
print(response.text)
# html = etree.HTML(response.text)

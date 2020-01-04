from urllib.request import urlopen
import requests
from urllib.parse import urlencode, quote_plus,quote
import pandas as pd

df = pd.read_csv("./encoding_list.txt", header=None, sep="\s")
df = df.set_index(2)
df.drop(1, axis=1, inplace=True)
code_dict = df.to_dict()[0]

service_key = """au%2FcDjT%2FkDMYFYnQUcVGxTXWAacWaeSa9szNYul7x3vhSEnt7XXJxbaqDJoxrhM%2BqHd75raiS7qInE%2FtE21GRw%3D%3D"""
for key in code_dict.keys():
    if key:
        service_key = service_key.replace(key, code_dict[key])
# print(service_key)

url = 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcNrgTrade?'

for i in range(1, 13):
    payload = {quote_plus('serviceKey'):service_key, 
            quote_plus('LAWD_CD'):'11110',quote_plus('DEAL_YMD'): '2015'+"{:02}".format(i) }
    result = urlencode(payload, quote_via=quote_plus, doseq=True)
    print(result)

    response_body = requests.get(url, params=payload) 
    result = response_body.text
    f = open("result_{0}.xml".format(i), "w")
    f.write(result)
# print(response_body.encoding)

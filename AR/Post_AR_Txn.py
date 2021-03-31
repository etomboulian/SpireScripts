import requests
import json
import urllib
from requests.auth import HTTPBasicAuth

spire_host = "localhost"
spire_port = "10880"
company_name = "Inspire"
user = "APIUser"
password = "SpireAPI123!"
spire_api_ar_endpoint = f"https://{spire_host}:{spire_port}/api/v2/companies/{company_name}/ar/transactions/" 

new_ar_json_string = '''
{
            "customer":{
                "code":"ABOX"
            },
            "date":"2021-03-31",
            "debitAmt":"999.99",
            "termsCode":"AA",
            "customerPO":"43576"
}
'''

new_ar_json = json.loads(new_ar_json_string)
result = requests.post(spire_api_ar_endpoint, json=new_ar_json, auth=HTTPBasicAuth(user, password), verify=False)


print(result.status_code, result.text)
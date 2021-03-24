import requests
import json
import urllib
from requests.auth import HTTPBasicAuth

po_id = 1

# Define some control variables
spire_host = "calm-scene-7886.spirelan.com"
spire_port = "10880"
company_name = "Inspire"
user = "APIUser"
password = "SpireAPI123!"
spire_api_issue_purchase_order_endpoint = f"https://{spire_host}:{spire_port}/api/v2/companies/{company_name}/purchasing/orders/{po_id}/issue" 

po_issue_result = requests.post(spire_api_issue_purchase_order_endpoint, auth=HTTPBasicAuth(user, password))

if(po_issue_result.status_code == 200):
    print("PO Issued Successfully")
    print(po_issue_result.content)
else:
    print("Issuing PO Failed")
    print("Status Code: " + str(po_issue_result.status_code))
    print("Response Msg: " + po_issue_result.text)
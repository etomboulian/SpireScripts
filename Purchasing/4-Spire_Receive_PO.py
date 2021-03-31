import requests
import json
import urllib
from requests.auth import HTTPBasicAuth

# Define some control variables
spire_host = "better-snow-2961.spirelan.com"
spire_port = "10880"
company_name = "inspire"
user = "APIUser"
password = "SpireAPI123!"

# Set the PO ID and Endpoint to update
po_id = 1
spire_api_issue_purchase_order_endpoint = f"https://{spire_host}:{spire_port}/api/v2/companies/{company_name}/purchasing/orders/{po_id}/receive"

po_issue_result = requests.post(spire_api_issue_purchase_order_endpoint, auth=HTTPBasicAuth(user, password))

# If we didn't get a successful result message print out what we received
if(po_issue_result.status_code != 200):
    print("Issuing PO Failed")
    print("Status Code: " + str(po_issue_result.status_code))
    print("Response Msg: " + po_issue_result.text)
    exit(-1)

# Otherwise the PO was received successfully
print("PO Received Successfully")
print(po_issue_result.content)

    
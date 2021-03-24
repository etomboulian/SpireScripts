import requests
import json
from requests.auth import HTTPBasicAuth

po_id = 1

# Define some control variables
spire_host = "calm-scene-7886.spirelan.com"
spire_port = "10880"
company_name = "Inspire"
user = "APIUser"
password = "SpireAPI123!"
spire_api_purchase_order_endpoint = f"https://{spire_host}:{spire_port}/api/v2/companies/{company_name}/purchasing/orders/{po_id}" 

sample_po_items = """
{
    "id": 1,
    "number": "0000080000",
    "vendor": {
        "id": 1
    },
    "status": "R",
    "items": [
        {
            "id": 1,
            "whse": "00",
            "partNo": "WIDGET",
            "inventory": {
                "id": 1
            },
            "receiveQty": "2"
        },
        {
            "id": 2,
            "whse": "00",
            "partNo": "GADGET",
            "inventory": {
                "id": 2
            },
            "receiveQty": "3"
        }
    ]
}
"""

# Convert json string into actual json
sample_po_items_json = json.loads(sample_po_items)

# Post the PO at the purchase order API enpoint
po_update_items_response = requests.put(spire_api_purchase_order_endpoint, json=sample_po_items_json, auth=HTTPBasicAuth(user, password))

if(po_update_items_response.status_code == 200):
    print("PO item quantities updated successfully")
    print(po_update_items_response.content)
else:
    print("Issuing PO Failed")
    print("Status Code: " + str(po_update_items_response.status_code))
    print("Response Msg: " + po_update_items_response.text)
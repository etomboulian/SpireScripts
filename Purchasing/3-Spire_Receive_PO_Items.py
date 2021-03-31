import requests
import json
from requests.auth import HTTPBasicAuth

# Define some control variables
spire_host = "better-snow-2961.spirelan.com"
spire_port = "10880"
company_name = "inspire"
user = "APIUser"
password = "SpireAPI123!"

# Set the PO ID and Endpoint to update
po_id = 1
spire_api_purchase_order_endpoint = f"https://{spire_host}:{spire_port}/api/v2/companies/{company_name}/purchasing/orders/{po_id}" 

# Sample Purchase Order JSON
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

# If we didn't get a successful result message print out what we received
if(po_update_items_response.status_code != 200):
    print("Issuing PO Failed")
    print("Status Code: " + str(po_update_items_response.status_code))
    print("Response Msg: " + po_update_items_response.text)
    exit(-1)

# Otherwise the PO was updated successfully
print("PO item quantities updated successfully")
print(po_update_items_response.content)

    
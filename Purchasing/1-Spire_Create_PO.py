import requests
import json
import urllib
from requests.auth import HTTPBasicAuth

# Define some control variables
spire_host = "calm-scene-7886.spirelan.com"
spire_port = "10880"
company_name = "Inspire"
user = "APIUser"
password = "SpireAPI123!"
spire_api_purchase_order_endpoint = f"https://{spire_host}:{spire_port}/api/v2/companies/{company_name}/purchasing/orders/" 

sample_po = """
{
  "trackingNo": "My tracking number",
  "vendor": {
    "vendorNo": "ACME"
  },
  "status": "O",
  "location": "My location",
  "items": [
    {
      "inventory": {
        "whse": "00",
        "partNo": "GADGET"
      },
      "orderQty": "10",
      "unitPrice": "10"
    },
    {
      "inventory": {
        "whse": "00",
        "partNo": "WIDGET"
      },
      "orderQty": "100",
      "unitPrice": "20"
    }
  ],
  "referenceNo": "Ref1"
}
"""
# Convert json string into actual json
sample_po_json = json.loads(sample_po)

# Post the PO at the purchase order API enpoint
po_create_response = requests.post(spire_api_purchase_order_endpoint, json=sample_po_json, auth=HTTPBasicAuth(user, password))

if (po_create_response.status_code == 201):
    print("PO created successfully!")
    print(po_create_response.text)
else:
    print("Not sure what happened here ...")
    print("Status Code: " + str(po_create_response.status_code))
    print("Response Msg: " + po_create_response.text)

import requests
import json
from requests.auth import HTTPBasicAuth

# Set the API Endpoint for this job
spire_api_add_order_endpoint = "https://calm-scene-7886.spirelan.com:10880/api/v2/companies/Inspire/sales/orders/"

# Set the json data representing the new order to be added to spire
new_order_string_data = """
{
  "customer": {
    "customerNo": "WEB02"
  },
  "orderNo": "W500001867",
  "type": "O",
  "orderDate": "2021-03-09",
  "requiredDate": "2021-03-09",
  "termsCode": "03",
  "customerPO": "123456789",
  "subtotal": "94.13",
  "total": "106.37",
  "hold": true,
  "address": {
    "type": "B",
    "name": "Good Boy Collective",
    "streetAddress": "3633 Main",
    "line1": "3633 Main",
    "line2": "",
    "line3": "",
    "line4": "",
    "city": "Toronto",
    "postalCode": "L6S4Y3 ",
    "provState": "ON",
    "country": "CAN",
    "phone": {
      "number": "6043296529",
      "format": 1
    },
    "fax": {
      "number": null,
      "format": 1
    },
    "email": "shopgoodboy@gmail.com",
    "website": ""
  },
  "shippingAddress": {
    "type": "S",
    "name": "Good Boy Collective",
    "streetAddress": "3633 Main",
    "line1": "3633 Main",
    "line2": "",
    "line3": "",
    "line4": "",
    "city": "Toronto",
    "postalCode": "L6S4Y3",
    "provState": "ON",
    "country": "CAN",
    "phone": {
      "number": "6043296529",
      "format": 1
    },
    "fax": {
      "number": null,
      "format": 1
    },
    "email": "shopgoodboy@gmail.com",
    "website": "",
    "shipCode": "19",
    "salesTaxes": [
      {
        "code": "3"
      }
    ]
  },
  "items": [
    {
      "inventory": {
        "whse": "VA",
        "partNo": "16401",
        "description": "Piazza Aspen LRG"
      },
      "orderQty": "1.00",
      "retailPrice": "94.13",
      "unitPrice": "94.13"
    }
  ]
}
"""
# Convert string json to actual json representation
new_order_json = json.loads(new_order_string_data)

# POST the new order into Spire
result = requests.post(spire_api_add_order_endpoint , json=new_order_json, auth=HTTPBasicAuth('APIUser', 'SpireAPI123!'))

# If the status code returns 201 then the order was added successfully
if (result.status_code == 201):
    print("Success!")
# Otherwise we got an error and will dump the status code and content to help to figure it out.
else:
    print(f"Failed to insert record: \nstatus_code = {result.status_code} \ncontent = {result.content.decode()}")











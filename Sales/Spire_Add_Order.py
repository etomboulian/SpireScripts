import requests
import json
from requests.auth import HTTPBasicAuth

# Control Variables
user = "APIUser"
password = "SpireAPI123!"
spire_host = "better-snow-2961.spirelan.com"
spire_port = "10880"
company_name = "inspire"

# Initial API Endpoint
spire_api_add_order_endpoint = f"https://{spire_host}:{spire_port}/api/v2/companies/{company_name}/sales/orders/"

# New order JSON data in string format
new_order_string_data = """
{
  "customer": {
    "customerNo": "ABOX"
  },
  "orderDate": "2021-03-31",
  "requiredDate": "2021-04-05",
  "termsCode": "03",
  "customerPO": "123456789",  
  "items": [
    {
      "inventory": {
        "whse": "VA",
        "partNo": "INSDB10"
      },
      "orderQty": "5"
    },
    {
      "inventory": {
        "whse": "VA",
        "partNo": "INSDB15"
      },
      "orderQty": "2"
    }
  ]
}
"""
# Convert string json to actual json representation
new_order_json = json.loads(new_order_string_data)

print("Adding new order to Spire")
# POST the new order into Spire
result = requests.post(spire_api_add_order_endpoint , json=new_order_json, auth=HTTPBasicAuth(user, password))

# If we received an error status then dump the status code and content and exit with Error status.  
if (result.status_code != 201):
    print(f"Failed to insert record: \nstatus_code = {result.status_code} \ncontent = {result.content.decode()}")
    exit(-1)

# If the status code returned 201 then the order was added successfully
print("Success adding order")

# Now attempt to invoice the new created order
new_order_endpoint = result.headers['Location']
new_order_endpoint += '/invoice'
print("Invoicing ...")

# Try to create invoice for the new order
invoice_result = requests.post(new_order_endpoint, auth=HTTPBasicAuth(user, password))

# If invoicing is not successful, then print the header data, and exit with an error code
if(invoice_result.status_code != 200):
  print("failed to invoice order")
  print(result.headers)
  exit(-1)
  
# If invoicing is successful (status 200), notify the invoiceNo and finish successfully
print(f"Success invoicing order")
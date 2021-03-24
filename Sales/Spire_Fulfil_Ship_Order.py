import requests
import json
import urllib
from requests.auth import HTTPBasicAuth

# Pick the order no. to ship here
order_to_ship = "0000800085"

# Define some control variables
spire_host = "calm-scene-7886.spirelan.com"
spire_port = "10880"
company_name = "Inspire"
user = "APIUser"
password = "SpireAPI123!"
spire_api_order_endpoint = f"https://{spire_host}:{spire_port}/api/v2/companies/{company_name}/sales/orders/" 

# Create the filter and url-encode it
order_filter = {"orderNo": order_to_ship}
order_filter_str = json.dumps(order_filter)
order_filter_encoded = urllib.parse.quote(order_filter_str)

# Get the data for the selected order
result = requests.get((spire_api_order_endpoint + "?filter=" + order_filter_encoded), auth=HTTPBasicAuth(user, password))

# Return the data for the selected order
order_data = result.content.decode()
order_data_json = json.loads(order_data)

# If the search on Order number returns more than one record or no records should fail and exit (because who knows what we are updating then)
if(order_data_json['count'] != 1):
    print("[-] No unique result for that OrderNo, unable to process any further")
    exit()

# Get the id for this order
order_id = order_data_json['records'][0]['id']

# Get the full order record from the order record endpoint
result_record = requests.get(spire_api_order_endpoint + str(order_id), auth=HTTPBasicAuth(user, password))
result_record_json = json.loads(result_record.content.decode())

print(f"[+] Success receiving data for OrderNo: {order_to_ship}")

# Loop through the items of the order and set the shipQty equal to the orderQty
count = 0
for item in result_record_json['items']:
    if(item['orderQty'] != (item['committedQty'])):
        item['committedQty'] = str(int(item['committedQty']) + int(item['backorderQty']))
        item['backorderQty'] = "0"
        count = count + 1

# If we changed anything then send the record back to the DB
if(count > 0):
    print("[+] Updated some of the line items for this order to be fully shipped")

    # Send updated record back into Spire
    put_result = requests.put(spire_api_order_endpoint + str(order_id), json=result_record_json, auth=HTTPBasicAuth(user, password))

    # If the result of sending the record back is status code 200 then we are successful
    if(put_result.status_code == 200):
        print("[+] Record put back into Spire successfully")
        # now we might want to invoice the order that we just fulfilled
        print("\nAttempting to invoice the order\n")

        # invoice the order
        spire_api_invoice_order_endpoint = spire_api_order_endpoint + str(order_id) + "/invoice"
        invoice_result = requests.post(spire_api_invoice_order_endpoint, auth=HTTPBasicAuth(user, password))

        # Check the result of requesting to invoice the order
        if (invoice_result.status_code == 200):
            invoice_data = json.loads(invoice_result.text)
            invoice_no = invoice_data["invoiceNo"]
            print("[+] Invoicing was successful")
            print(f"[+] Created Invoice: {invoice_no}")
            print("[+] Finished Successfully\n")
        else:
            print("[-] Invoicing failed. See below for details")
            print("[-] Status Code: " + str(invoice_result.status_code))
            print("[-] Response Msg: " + invoice_result.text)

    # If the result of sending the record back is status code 423 then the record is locked in the DB
    elif(put_result.status_code == 423):
        print("[-] Record is locked, please close the record in Spire GUI")
    else:
        print(f"[-] Some other error occured while sending back the updated record and I wasn't able to figure it out.\nStatus Code: {put_result.status_code}")
        print(put_result.text)

# Otherwise nothing was updated, no action to take, just notify and exit
else:
    print("[-] No Action taken -- Nothing to update for this order")

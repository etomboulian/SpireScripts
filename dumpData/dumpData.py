import requests
from requests.auth import HTTPBasicAuth
import json

servername = "better-snow-2961.spirelan.com"    # use the valid SSL hostname here
port = 10880                                    # On premesis Spire: 10880; Cloud: 443
companyName = 'inspire2021'                     # Company Name to call data from
username = 'ApiUser'                            # Login Username
password = 'Spire123!'                          # Login Password

pageSize = 1000                                 # page size to call records in batches of

class SpireData:
    def __init__(self, type, filters = '') -> None:
        # set the valid credentials
        self.credentials = HTTPBasicAuth(username, password)

        # set the type of data that we want to get 
        if (type == 'orders'):
            self.endpoint = 'sales/orders'
        elif (type == 'invoices'):
            self.endpoint = 'sales/invoices'
        elif (type == 'inventory'):
            self.endpoint = 'inventory/items'
        elif (type == 'inventoryMovement'):
            self.endpoint = 'inventory/movement'
        
        # Create the API endpoint url from the provided data
        self.baseUrl = f'https://{servername}:{port}/api/v2/companies/{companyName}/{self.endpoint}'

        if (filters != ''):
            self.baseUrl += f'?{filters}'

    # Function to get all of the records for the endpoint type we chose    
    def fetchAll(self):
        recordCount = self.getRecordCount()
        print(f"Total Record Count: {recordCount}")
        pageCount = int(recordCount / pageSize) + 1 
        self.pageCount = pageCount
        for i in range(0, pageCount):
            start = i * pageSize
            url = self.baseUrl + f"?start={start}&limit={pageSize}"
            print("Getting Data: " + url)
            records = requests.get(url, auth=self.credentials).json()['records']
            yield records

    # Function to get the total number of records for the whole request
    def getRecordCount(self):
        try:
            response = requests.get(self.baseUrl, auth=self.credentials).json()
        except:
            print(self.baseUrl)
            print(requests.get(self.baseUrl, auth=self.credentials))
            raise Exception("unable to get data from Spire API")
        
        return response['count']

    # Function to get all records and write them out to a JSON file
    # This is the main intended action for this class
    def writeAllRecordsToJsonArrayFile(self, outFile):
        # Open the file and begin a JSON array manually
        file = open(outFile, 'w+')
        file.write('[')
        # Set some control variables
        pageCount = 0
        firstPass = True
        # Iterate through all of the pages in the endpoint that the instance of this class points to and write out to file
        for page in self.fetchAll():           
            for item in (page):
                if firstPass:
                    text = json.dumps(item)
                    file.write(text + '\n')
                    firstPass = False
                else:
                    text = json.dumps(item)
                    file.write(',')
                    file.write(text + '\n')
            print(f"Writing page {pageCount}")
            pageCount = pageCount + 1 
        # Manually close the JSON Array and the file
        file.write(']')
        file.close()
        
def main():
    ## Set the type of output that you want here
    '''
    Options:
        -orders
        -invoices
        -inventory
        -inventoryMovement
    '''
    spireData = SpireData('inventoryMovement')

    ## Set the location of the output file that you wish to write to here
    spireData.writeAllRecordsToJsonArrayFile('movement.json')
    print('Done')
    exit(0)

if __name__ == '__main__':
    main()
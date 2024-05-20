import requests
import json
import csv


digitokens = open('digikey_token.json')
data = json.load(digitokens)
digitokens.close()


def get_authorization():

    url = 'https://api.digikey.com/v1/oauth2/token'
    url_data = {
        'client_id': data['client_info'][0]['client_id'],
        'client_secret': data['client_info'][0]['client_secret'],
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, data=url_data)
    Jresponce = response.json()
    data['token_info'][0]['Authorization'] = Jresponce['access_token']
    data['token_info'][0]['token_type'] = Jresponce['token_type']

    with open('digikey_token.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    return(data)

def get_data():
    offsetCounter = 0
    size = 50
    BulkData = []
    while offsetCounter < size:
        url = 'https://api.digikey.com/products/v4/search/keyword'
        url_header = {
            'X-DIGIKEY-Client-Id': data['client_info'][0]['client_id'],
            'Authorization': data['token_info'][0]['token_type'] + ' ' + data['token_info'][0]['Authorization'],
            'content-Type':'application/json'
            }
        url_body = {
            'Keywords': 'ferrite cores',
            'Limit': 50,
            'Offset': offsetCounter,
            'FilterOptionsRequest': {
                'CategoryFilter': [
                    {
                        'Id': '936'
                    }
                ],
                "MarketPlaceFilter": "ExcludeMarketPlace"
                }
            }
    
        coreInfo = requests.post(url, headers = url_header, data=json.dumps(url_body))
        Ecode = coreInfo.status_code
        Jcode = coreInfo.json()
        if Ecode == 200:
            #print("Proper Response")
            size = Jcode["ProductsCount"]
            if size-offsetCounter < 50:
                datapoints = (size-offsetCounter)
            else:
                datapoints = 50
            BulkData = parse_data(BulkData, Jcode, datapoints)
            offsetCounter = offsetCounter + 50
            completionPercent = round((offsetCounter/size)*100,2)
            print("Downloading is " + str(completionPercent) + "% Done")
            
        elif Ecode == 400:
            print("Bad Request\n")
            print("Something is malformed\n")
            print(Jcode)
            break
        elif Ecode == 401:
            print("Unauthorized")
            get_authorization()
            continue
        elif Ecode == 403:
            print("Forbidden")
            print(Jcode)
            break
        elif Ecode == 404:
            print("Not Found")
            print(Jcode)
            break
        elif Ecode == 429:
            print("Too Many Requests")
            print(Jcode) 
            break          
        elif Ecode == 500:
            print("Unhandled error")
            print(Jcode)
            break
        elif Ecode == 503:
            print("Service Unavailable")
            print(Jcode)
            break
        else:
            print("Something is very wrong")
            print(Jcode)
            break

    with open('digikey_coreDump.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in BulkData:
            writer.writerow(row)

def parse_data(orgData, Data, values):
    #print("parsing")
    tempData = [[0 for _ in range(22)] for _ in range(values)]

    for key in range(values):
        tempData[key][0] = Data['Products'][key]['ManufacturerProductNumber']
        tempData[key][1] = Data['Products'][key]['DatasheetUrl']
        tempData[key][2] = Data['Products'][key]['PhotoUrl']
        tempData[key][3] = Data['Products'][key]['ProductUrl']
        tempData[key][4] = Data['Products'][key]['QuantityAvailable']
        tempData[key][5] = Data['Products'][key]['ProductStatus']['Status']
        tempData[key][6] = Data['Products'][key]['ProductVariations'][0]['Supplier']['Name']
        ParameterLen = len(Data['Products'][key]['Parameters'])
        for p in range(ParameterLen):
            compare = Data['Products'][key]['Parameters'][p]['ParameterId']
            if compare == 1012: #Core Type
                tempData[key][7] = Data['Products'][key]['Parameters'][p]['ValueText']
            elif compare == 70: #Material
                tempData[key][8] = Data['Products'][key]['Parameters'][p]['ValueText']
            elif compare == 76: #Diameter
                tempData[key][9] = Data['Products'][key]['Parameters'][p]['ValueText']
            elif compare == 1819: #Inductance Factor (Al)
                tempData[key][10] = Data['Products'][key]['Parameters'][p]['ValueText']
            elif compare == 1820: #Initial Permeability (\u00b5i)
                tempData[key][11] = Data['Products'][key]['Parameters'][p]['ValueText']
            elif compare == 2203: #Effective Length (le) mm
                tempData[key][12] = Data['Products'][key]['Parameters'][p]['ValueText']
            elif compare == 2204: #Effective Area (Ae) mm\u00b2
                tempData[key][13] = Data['Products'][key]['Parameters'][p]['ValueText']
            elif compare == 2206: #Effective Magnetic Volume (Ve) mm\u00b3
                tempData[key][14] = Data['Products'][key]['Parameters'][p]['ValueText']
            elif compare == 329: #Height
                tempData[key][15] = Data['Products'][key]['Parameters'][p]['ValueText']
            elif compare == 77: #Length
                tempData[key][16] = Data['Products'][key]['Parameters'][p]['ValueText']
            elif compare == 3: #Tolerance
                tempData[key][17] = Data['Products'][key]['Parameters'][p]['ValueText']
            elif compare == 1874: #Gap
                tempData[key][18] = Data['Products'][key]['Parameters'][p]['ValueText']
            elif compare == 2201: #Effective Permeability (\u00b5e)
                tempData[key][19] = Data['Products'][key]['Parameters'][p]['ValueText']
            elif compare == 1826: #Finish
                tempData[key][20] = Data['Products'][key]['Parameters'][p]['ValueText']
            elif compare == 2202: #Core Factor (\u03a3I/A) mm\u207b\u00b9
                tempData[key][21] = Data['Products'][key]['Parameters'][p]['ValueText']

    orgData = orgData + tempData
    return(orgData)

def MaterialUpdate():
    print("Updating material Database")


def CoreCalc(Turns):
    with open('digikey_coreDump.csv', newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=',', quotechar='|')
        for lines in data:
            print(lines)



            

if __name__ == "__main__":
    #get_data()
    CoreCalc(1)


## Things to do

# Math on everything




import requests
import json

digitokens = open('digikey_token.json')
data = json.load(digitokens)
digitokens.close()


def get_authorization():

    url = 'https://sandbox-api.digikey.com/v1/oauth2/token'
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

def get_part():
    
    url = 'https://sandbox-api.digikey.com/products/v4/search/categories/936'
    headers = {
        'Authorization': data['token_info'][0]['token_type'] + ' ' + data['token_info'][0]['Authorization'],
        'X-DIGIKEY-Client-Id': data['client_info'][0]['client_id']

        }
    coreInfo = requests.get(url, headers = headers)
    JcoreInfo = coreInfo.json()
    print(coreInfo.status_code)
    with open('digikey_coreDump.json', 'w') as json_file:
        json.dump(JcoreInfo, json_file, indent=4)

#get_authorization()
get_part()
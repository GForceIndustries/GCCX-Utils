import tkinter.simpledialog, base64, requests

client_id = tkinter.simpledialog.askstring("Client ID", "Enter the Client ID")
client_secret = tkinter.simpledialog.askstring("Client Secret", "Enter the Client Secret")
region = tkinter.simpledialog.askstring("Region", "Enter the region")

if region.upper() in ('US-EAST-1','USE1'):
    api_region = 'mypurecloud.com'
elif region.upper() in ('US-EAST-2','USE2','FEDRAMP'):
    api_region = 'use2.us-gov-pure.cloud'
elif region.upper() in ('US-WEST-2','USW2'):
    api_region = 'usw2.pure.cloud'
elif region.upper() in ('EU-WEST-1','EUW1'):
    api_region = 'mypurecloud.ie'
elif region.upper() in ('EU-WEST-2','EUW2'):
    api_region = 'euw2.pure.cloud'
elif region.upper() in ('EU-CENTRAL-1','EUC1'):
    api_region = 'mypurecloud.de'
elif region.upper() in ('EU-CENTRAL-2','EUC2'):
    api_region = 'euc2.pure.cloud'
elif region.upper() in ('CA-CENTRAL-1','CAC1'):
    api_region = 'cac1.pure.cloud'
elif region.upper() in ('AP-NORTHEAST-1','APNE1'):
    api_region = 'mypurecloud.jp'
elif region.upper() in ('AP-NORTHEAST-2','APNE2'):
    api_region = 'apne2.pure.cloud'
elif region.upper() in ('AP-NORTHEAST-3','APNE3'):
    api_region = 'apne3.pure.cloud'
elif region.upper() in ('AP-SOUTHEAST-2','APSE2'):
    api_region = 'mypurecloud.com.au'	
elif region.upper() in ('AP-SOUTH-1','APS1'):
    api_region = 'aps1.pure.cloud'
elif region.upper() in ('SA-EAST-1','SAE1'):
    api_region = 'sae1.pure.cloud'
elif region.upper() in ('ME-CENTRAL-1','MEC1'):
    api_region = 'mec1.pure.cloud'
elif region.upper() in ('DCA'):
    api_region = 'inindca.com'
elif region.upper() in ('TCA'):
    api_region = 'inintca.com'
else:
    print ('Please check that your region selection is valid')
    quit()

authorization = base64.b64encode(bytes(client_id + ":" + client_secret, "ISO-8859-1")).decode("ascii")

auth_url = 'https://login.' + api_region + '/oauth/token'

header = {
    "Authorization": f"Basic {authorization}",
    "Content-Type": "application/x-www-form-urlencoded"
}

payload = {
    "grant_type": "client_credentials"
}

auth_response = requests.post(auth_url, headers = header, data = payload)
print(auth_response)
auth_response_json = auth_response.json()
print(auth_response_json)

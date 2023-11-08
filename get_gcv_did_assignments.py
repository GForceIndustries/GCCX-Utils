from math import e
import tkinter.simpledialog, base64, requests, time

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

# ////////// Authenticate \\\\\\\\\\
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
auth_response_json = auth_response.json()

#Build header for subsequent API requests
header = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + auth_response_json['access_token']
}

# ////////// Get GCV DIDs \\\\\\\\\\
gcv_dids_list = []
get_gcv_dids_page_size = 25
get_gcv_dids_url_host = "https://apps." + api_region + "/platform"
get_gcv_dids_url_path = "/api/v2/carrierservices/numberpurchase/20210520/orders?excludedStatuses=DISCONNECTED,CANCELLED&direction=NEXT&pageSize=" + str(get_gcv_dids_page_size)

get_gcv_dids_fetch_complete = False
gcv_dids_page = 1
while get_gcv_dids_fetch_complete == False:
    get_gcv_dids_url = get_gcv_dids_url_host + get_gcv_dids_url_path
    get_gcv_dids_response = requests.get(get_gcv_dids_url, headers = header)
    gcv_dids_json = get_gcv_dids_response.json()
    print("Processing GCV DIDs page " + str(gcv_dids_page))
    
    try:
        for gcv_did in gcv_dids_json['entities']:
            gcv_dids_list.append("+" + gcv_did['countryCode'] + gcv_did['did'])
        try:
            get_gcv_dids_url_path = gcv_dids_json['next'].replace("%2C",",").replace("20210520","20210520/orders")
        except KeyError:
            get_gcv_dids_fetch_complete = True
    except KeyError:
        pass
    gcv_dids_page += 1

# ////////// Get DIDs \\\\\\\\\\
assigned_gcv_dids_list = []
unassigned_gcv_dids_list = []
get_dids_page_size = 100
get_dids_url_host = "https://apps." + api_region + "/platform"
get_dids_url_path = "/api/v2/telephony/providers/edges/didpools/dids?pageNumber=1&type=ASSIGNED_AND_UNASSIGNED&pageSize=" + str(get_dids_page_size)

get_dids_fetch_complete = False
while get_dids_fetch_complete == False:
    get_dids_url = get_dids_url_host + get_dids_url_path
    get_dids_response = requests.get(get_dids_url, headers = header)
    dids_json = get_dids_response.json()
    print("Processing DIDs page " + str(dids_json['pageNumber']) + " of " + str(dids_json['pageCount']))
    
    try:
        for did in dids_json['entities']:
            if did['number'] in gcv_dids_list: # if the DID is in gcv_dids_list
                if str(did['assigned']).lower() == "true": # and the DID is assigned
                    did_number = did['number']
                    did_owner_name = did['owner']['name']
                    did_owner_self_uri = did['owner']['selfUri']
                    if "/api/v2/architect/ivrs" in did_owner_self_uri:
                        did_owner_type = "IVR call route"
                    elif "/api/v2/telephony/providers/edges/phones" in did_owner_self_uri:
                        did_owner_type = "Station"
                    elif "/api/v2/users" in did_owner_self_uri:
                        did_owner_type = "User"
                    else:
                        did_owner_type = "Object type unknown"
                    assigned_gcv_dids_list.append(did_number + " assigned to " + did_owner_name + " (" + did_owner_type + ")")
                else: # if it's not assigned
                    unassigned_gcv_dids_list.append(did['number'])
        try:
            get_dids_url_path = dids_json['nextUri']
        except KeyError:
            get_dids_fetch_complete = True
    except KeyError:
        pass

    time.sleep(0.1)

print("Current total GCV DIDs: " + str(len(gcv_dids_list)))

print("Current unassigned GCV DIDs: " + str(len(unassigned_gcv_dids_list)))
for did in unassigned_gcv_dids_list:
    print(did)

print("Current assigned GCV DIDs: " + str(len(assigned_gcv_dids_list)))
for did in assigned_gcv_dids_list:
    print(did)

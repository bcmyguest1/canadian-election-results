import requests
import time
# Set of functionalized api calls for easier access if needed
def getApiStatus(election):
    return handleJsonGetRequest(buildURI(election, 'status'),{} , 'apiStatus')

def getPartyInfo(election):
    return handleJsonGetRequest(buildURI(election, 'Parties'),{}, 'PartyInfo')

def getRidingInfo(election):
    return handleJsonGetRequest(buildURI(election, 'Ridings'),{}, 'RidingInfo')

def getCandidateRidingInfo(election, riding):
    params = {'ridingnumber': riding}
    return handleJsonGetRequest(buildURI(election, 'Candidates_For_Riding'),params, 'CandidateRidingInfo')

def handleJsonGetRequest(reqURI, params, reqType, retryAmount=3):
    try:
        resp = requests.get(reqURI, params=params)
        if resp.status_code == 200:
            return resp.json()
        else:
            print('Error getting: {} for: {} - status: {}'.format(resp.url,reqType, resp.status_code))
            if (retryAmount > 0):
                time.sleep(2000)
                print('Retrying getting: {} for: {}'.format(resp.url,reqType))
                return handleJsonGetRequest(reqURI, params, reqType, retryAmount-1)
            print('Not retring getting: {} for: {}'.format(resp.url,reqType))
            return None
    except:
        print('Error getting: {} for: {}'.format(resp.url,reqType))
        return None

def buildURI(election, endpoint):
    uri = 'https://electionsapi.cp.org/api/{}/{}'.format(election, endpoint) 
    return uri
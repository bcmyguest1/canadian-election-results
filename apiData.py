# Used to get election data from electionsapi.cp.org
import requests 
import psycopg2 
import time

election = 'federal2019'

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

def fillCandidateAndVoterInfo(candidate,partiesDict,tmpVoterShare,tmpRidingCandidate):
    if candidate['PartyShortName_En'] in partiesDict:
        # fill in the candidate and roster in the same loop
        # table design kind of forces hard coding here
        candName = tmpRidingCandidate.makeCandidateName(candidate['First'],candidate['Last'])
        voteShare = tmpVoterShare.determineVoteShare(candidate['Votes'],candidate['TotalVoters'])
        print('Adding candidate: {} with VS: {} for party: {}'.format(candName,voteShare,candidate['PartyShortName_En']))
        if candidate['PartyShortName_En'] == 'LIB':
            tmpRidingCandidate.libCand = candName 
            tmpVoterShare.libVS = voteShare
        elif candidate['PartyShortName_En'] == 'CON':
            tmpRidingCandidate.conCand = candName
            tmpVoterShare.conVS = voteShare
        elif candidate['PartyShortName_En'] == 'NDP':
            tmpRidingCandidate.NDPCand = candName
            tmpVoterShare.NDPVS = voteShare
        elif candidate['PartyShortName_En'] == 'BQ':
            tmpRidingCandidate.BQCand = candName
            tmpVoterShare.BQVS = voteShare
        elif candidate['PartyShortName_En'] == 'PPC':
            tmpRidingCandidate.PPCCand = candName
            tmpVoterShare.PPCVS = voteShare
        elif candidate['PartyShortName_En'] == 'GR':
            tmpRidingCandidate.GreCand = candName
            tmpVoterShare.GreVS = voteShare
    return tmpVoterShare, tmpRidingCandidate

def getAndFormatAPIInfo(election):
    status = getApiStatus(election)
    if status is not None and status['status'] == 'ok':
        partiesAPI = getPartyInfo(election)
# build a dict with party short to long name conversion (to be used later)
        partiesDict = {}
        for party in partiesAPI:
            partiesDict[party['ShortName_En']] = party

        ridingsAPI = getRidingInfo(election) 
        ridingsVotesDict = {}
        candidateVotesDict = {}
        for tmpRiding in ridingsAPI:
            ridingsVotesDict[tmpRiding['RidingNumber']] = ridingVotes(tmpRiding['RidingNumber'], tmpRiding['TotalVotes'], tmpRiding['TotalVoters'])
        # for each of these ridings, we will need to make an api request which can be used to both get candidate and more vote info
        # simpler to have this in a separate for loop, time complexity is the same
        if ridingsVotesDict is not None:
            for ridingNumber in ridingsVotesDict:
                print('attempting to get candidate and vote info for riding: {}'.format(ridingNumber))
                candidateVotes = getCandidateRidingInfo(election, ridingNumber)
                try:
                    tmp = ridingsVotesDict[ridingNumber]
                    ridingCandidate = ridingCandidates(ridingNumber)
                    for candidate in candidateVotes:
                        tmp, ridingCandidate = fillCandidateAndVoterInfo(candidate,partiesDict,tmp, ridingCandidate)
                    ridingsVotesDict[ridingNumber] = tmp
                    candidateVotesDict[ridingNumber] = ridingCandidate    
                    candidateVotes = None
                    print('Got candidate and vote info for riding: {}'.format(ridingNumber))
                except (Exception) as e:
                    print('Could not get candidates or voter info for riding: {} - error: {}\n'.format(ridingNumber, e))
        else:
            print('ridingsVotesDict is null, cannot proceed\n')
        return ridingsVotesDict, candidateVotesDict
    else:
        print('Could not connect to API')
        return None, None

# Classes only made for utility, not needed to solve the problem
class ridingCandidates:
    # needs info from the parties, ridings api, candidates riding api
    def __init__(self, number, libCand='', conCand='', NDPCand='', GreCand='',
                BQCand='', PPCCand=''):
        self.ridingNumber = number
        self.libCand = libCand
        self.conCand = conCand
        self.NDPCand = NDPCand
        self.GreCand = GreCand
        self.BQCand = BQCand
        self.PPCCand = PPCCand
    def makeCandidateName(self, fname, lname):
        return '{} {}'.format(fname,lname)

class ridingVotes:
    # needs info from the parties, ridings api, candidates riding api
    def __init__(self, number, votes, voters, nameEn='', nameFr='', 
                conVS=0.0, libVS=0.0, NDPVS=0.0, GreVS=0.0,BQVS=0.0,PPCVS=0.0):
        self.ridingNumber = number
        self.ridingNameEn = nameEn
        self.ridingNameFr = nameFr
        self.totalVoters = votes
        self.totalVoters = voters
        self.conVS = conVS
        self.libVS = libVS
        self.BQVS = BQVS
        self.NDPVS = NDPVS
        self.GreVS = GreVS
        self.PPCVS = PPCVS
    def determineVoteShare(self, votes, voters):
        return votes/voters


try :


    print('Getting riding votes and candidates')
    ridingsVotesDict, candidateVotesDict = getAndFormatAPIInfo(election)
    if (ridingsVotesDict is not None 
        and len(ridingsVotesDict) > 0 
        and candidateVotesDict is not None 
        and len(candidateVotesDict) > 0):
        print('Adding to sql')
    else:
        print('There are no items in one of the dicts! Not adding to sql')
except (Exception, psycopg2.DatabaseError) as e:
    print(e)

class ridingVotes:
    # needs info from the parties, ridings api, candidates riding api
    def __init__(self, number, votes, voters, nameEn='', nameFr='', 
                conVS=0.0, libVS=0.0, NDPVS=0.0, GreVS=0.0,BQVS=0.0,PPCVS=0.0):
        self.ridingNumber = number
        self.ridingNameEn = nameEn
        self.ridingNameFr = nameFr
        self.totalVotes = votes
        self.totalVoters = voters
        self.conVS = conVS
        self.libVS = libVS
        self.BQVS = BQVS
        self.NDPVS = NDPVS
        self.GreVS = GreVS
        self.PPCVS = PPCVS
    def determineVoteShare(self, votes=-1, voters=-1):
        if (votes < 0 or voters < 0):
            return self.totalVotes/self.totalVoters
        return votes/voters
    def createDbInsertString(self):
        cols = (self.ridingNumber,self.ridingNameEn,self.ridingNameFr,
                self.totalVotes, self.determineVoteShare(),self.libVS,
                self.conVS, self.NDPVS, self.BQVS, self.GreVS, self.PPCVS)
        return ('\t'.join(map(str,cols)) + '\n')
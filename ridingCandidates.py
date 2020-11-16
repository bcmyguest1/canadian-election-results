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
    def createDbInsertString(self):
        cols = (self.ridingNumber,self.libCand,self.conCand,self.NDPCand,
                self.GreCand, self.BQCand, self.PPCCand)
        return ('\t'.join(map(str,cols)) + '\n')

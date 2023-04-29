def read_file_to_dict(filename):
    result = {}
    with open(filename, "r") as f:
        for line in f:
            if not line.startswith('#'):
                parts = line.split()
                if len(parts) == 2:
                    key, value = parts
                    result[key] = value
    return result

def getStatsFileName(bm,branchpredictorID,lsize,gsize,csize):
    return bm +"_"+str(branchpredictorID)+"_"+str(lsize)+"_"+str(gsize)+"_"+str(csize)

def isExecuted(statsdir):
    statsDict = read_file_to_dict(statsdir)
    return statsDict["sim_insts"] == '500000000'

def checkConfig(benchmarksList,bpredid,ls,gs,cs):
    currentdir = "/home/010/j/jx/jxp220032/CS6304P2"
    for bm in benchmarksList:
        statsdir = currentdir + "/simstats/"+getStatsFileName(bm,bpredid,ls,gs,cs)
        if not isExecuted(statsdir):
            print(getStatsFileName(bm,ls,gs,cs) + '\n')

def checkAllStats():
    benchmarksList  = ['456.hmmer','458.sjeng','470.lbm']
    #local predictor
    for ls in [1024,2048,4096]:
        checkConfig(benchmarksList,1,ls,1024,1024)
    #biModal
    for gs in [1024,2048,4096]:
        for cs in [1024,2048,4096]:
            checkConfig(benchmarksList,2,1024,gs,cs)
    #tournament
    for gs in [1024,2048,4096]:
        for cs in [1024,2048,4096]:
            for ls in [1024,2048,4096]:
                checkConfig(benchmarksList,3,ls,gs,cs)
    
checkAllStats()
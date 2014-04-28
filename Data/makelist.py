import os

periods= ["A" , "B" , "C" , "D"]

Stream = ["DoubleElectron", "DoubleMuon", "ElectronMuon", "SingleMuon", "SingleElectron"]

dir   = ["DiEl","DiMu","MuEG","Mu","El"]

i_s=-1
for stream in Stream:
    i_s = i_s + 1
    for period in periods:
        os.system("grep 'file =  rootTupleMaker_CRAB_DATA_2012_53X'   " + stream + "/" + dir[i_s]+ period +"/res/CMSSW_* > log" + stream +period)
    
    frp = open('log'+ stream +period ,'r')
    
    fout = open(stream +'period'+ period +'.txt' ,'w')
    for line in frp:
        if "rootTupleMaker_CRAB" in line:
            splitline  = line.split()
            for sline in splitline:
                if "rootTupleMaker_CRAB" in sline:
                    fout.write(sline + "\n")
                

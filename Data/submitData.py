import os,sys
from functions import *

type="Data"
##### First entry is directory name

EMuons = ["ElectronMuon" ,"MuEGA" ,"MuEGB","MuEGC","MuEGD"]
Muons = ["SingleMuon" ,"MuA", "MuB", "MuC", "MuD"]
DoubleMuon = ["DoubleMuon" ,"DiMuA" ,"DiMuB","DiMuC","DiMuD"]
DoubleElectron = ["DoubleElectron" ,"DiElA","DiElB","DiElC","DiElD"]

list_to_submit = DoubleMuon

#### IF YOU WISH TO PRODUCE A SECOND SAMPLE
### put any sample name in Extension and it will be resubmitted with new output name  
Extension= "False"
ext="V1"


###### INITIALISE
dir=""
nsamples=0
not_complete = []
n_running = 0
for i in list_to_submit:
    nsamples+=1
    if nsamples ==1:
        dir= i
        continue

    if not (os.path.exists(dir)):
        os.system("mkdir " +  dir)

    dataset=""
    filename = 'datasetlist.txt'
    for line in open(filename, 'r'):
        if not line.startswith("#"):
            entries = line.split()
            if len(entries)==2:
                if i == entries[0]:
                    dataset=entries[1]

    print "dataset=" + dataset

    if Extension == "True":
        i = i+ ext
        print "Adding extension to job name: " + ext

    cfgfile=  dir+"/ntupleCrab_DATA_" + i + ".cfg"
    jobfile = dir + "/" + i + "/"
    crablog = dir + "/" + i  + "/log/crab.log"
    search="Creator: total # of jobs = "
    search_sub = "Submitted job # " 
    njobs=0

    #### DOES THE DIR EXIST?
    if not (os.path.exists(cfgfile)):
        print "crab dir does not exist for this job. Making now"
        configfile=open(cfgfile,'w')
        configfile.write(makeConfigFile(dataset, i, dir))
        configfile.close()
        os.system("crab -create -cfg " + cfgfile )
    ##### DOES THE JOB EXIST?
    elif not (os.path.exists(crablog)):    
        print "Crab dir exists but no job directory. Creating the jobs with crab -create"
        os.system("crab -create -cfg " + cfgfile )
    #### HAS THE JOB BEEN SUBMITTED    
    else:
        print "Job already created"



    ######## CHECK IF ALL JOBS ARE SUBMITTED 
    all_submitted=False
       
    logfile = open(crablog,'r')
    found = False
    for line in logfile:
        if search in line:
            strippedline = line[60:]
            for s in strippedline.split():
                njobs = s
                print "Job has " + str(njobs) + " sub jobs"
                break

    logfile.close()
    
    search_sub+=str(njobs)
    logfile = open(crablog,'r')
    for line in logfile:
        if search_sub in line:
            all_submitted=True
            print "All sub jobs are previously submitted to crab"
    logfile.close()

    if all_submitted == False:
        ijobs= int(njobs)        
        while ijobs > 0:
            os.system("crab -submit 500 -c " + dir + "/" +  i )    
            ijobs -= 500
                
    else:
        print "Crab job exists for this file: Add extension and resubmit?"
        os.system("crab -status -c " + dir+ "/" +  i)
        os.system("crab -get -c " + dir+ "/" +  i)
        os.system("crab -status -c " + dir+ "/" +  i)
        os.system("crab -status -c " +dir+ "/"  + i + " > log") 


        
        ##### check jobs that fail in output
        
        status_search = "Y   Retrieved         Cleared"
        logfile = open("log",'r')

        ##### LIST FOR RESUBMITTING FAILED JOBS
        resubmit_list = []
        njob=0
        for line in logfile:
            if status_search in line:
                strippedline = line[42:]
                nstrips=0
                for s in line.split():
                    nstrips+=1
                    if nstrips == 1:
                        njob= int(s)
                nsstrips=0        
                for s in strippedline.split():
                    nsstrips+=1
                    if nsstrips < 3:
                        if not int(s) == 0:
                            print "Job " + str(njob) + " failed"           
                            resubmit_list.append(njob)
                            break
                        
        logfile.close()                    

        ###### CHECK FOR ABORTED JOBS
        status_search = "Y   Aborted           Aborted"
        logfile = open("log",'r')
        njob=0
        for line in logfile:
            if status_search in line:
                nstrips=0
                for s in line.split():
                    nstrips+=1
                    if nstrips == 1:
                        njob= int(s)
                        print "Job " + s + " Aborted"
                        resubmit_list.append(njob)
                        break
        logfile.close()


        ##### RESUBMIT JOBS (FAILED+ ABORTED)
        
        fulllist = []
        relist=""
        nresubmit=0
        for it in resubmit_list:
            nresubmit+=1
            if not nresubmit== 1:
                relist+= ","
            relist+= str(it)
            if not nresubmit%400:
                fulllist.append(relist)
                relist=""
                nresubmit=0
        if not nresubmit == 0:
            fulllist.append(relist)
        
        for k in fulllist:
            resubmit_command = "crab -resubmit " + k + " -c " + dir+ "/" +  i
            print resubmit_command
            not_complete.append(i)
            os.system(resubmit_command)



        ########## COUNT NUMBER OF RUNNING JOBS
        status_search = "N   Running"
        n_running=0
        logfile = open("log",'r')
        for line in logfile:
            if status_search in line:
                n_running+=1
        logfile.close()


        ######### ARE JOBS Cancelled
        status_search = "N   Cancelled"
        logfile = open("log",'r')
        stuck_list = []
        njob=0
        for line in logfile:
            if status_search in line:
                nstrips=0
                for s in line.split():
                    nstrips+=1
                    if nstrips == 1:
                        njob= int(s)
                        stuck_list.append(njob)
                        break
        logfile.close()
                    

        
                
        ############  RESUBMIT STUCK JOBS?
        stuck_fulllist = []
        relist=""
        nresubmit=0
        for it in stuck_list:
            nresubmit+=1
            if not nresubmit== 1:
                relist+= ","
            relist+= str(it)
            if not nresubmit%400:
                stuck_fulllist.append(relist)
                relist=""
                nresubmit=0
        if not nresubmit == 0:
            stuck_fulllist.append(relist)

        for k in stuck_fulllist:
            kill_command = "crab -kill " + k + " -c " + dir+ "/" +  i
            resubmit_command = "crab -resubmit " + k + " -c " + dir+ "/" +  i
            print kill_command
            print resubmit_command
            not_complete.append(i)
            os.system(kill_command)
            os.system(resubmit_command)
            
        os.system("rm log")   

n_failed=0        
for jobs in not_complete:
    n_failed+=1

if n_failed == 0:
    if n_running ==0:
        print "All jobs completed"
    else:
        print "Jobs still running. None failed"    
else:
    print "List of jobs yet that were resubmitted are:"
    
for jobs in not_complete:
    print jobs
    


def makeConfigFile(dataset,   uidir, dir):

    config='[CRAB]\n'
    config+='\n'
    config+='jobtype = cmssw\n'
    config+='scheduler = remoteGlidein\n'
    config+='#scheduler = glite\n'
    config+='### NOTE: just setting the name of the server (pi, lnl etc etc )\n'
    config+='###       crab will submit the jobs to the server...\n'
    config+='use_server = 0\n'
    config+='\n'
    config+='[CMSSW]\n'
    config+='\n'
    #config+='allow_nonproductioncmssw = 1\n'
    config+='###### Majorana signal samples ######\n'
    config+='datasetpath=' + dataset + '\n'
    config+='\n'
    config+='### The ParameterSet you want to use\n'
    config+='pset = rootTupleMaker_CRAB_DATA_2012ABCD_ReReco_22Jan2013_53X_chs_cfg.py\n'
    config+='\n'
    config+='### not needed for MC\n'
    config+='lumi_mask = Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt\n'
    config+='### Splitting parameters\n'
    config+='total_number_of_lumis=-1\n'
    config+='lumis_per_job = 15\n'
    config+='\n'
    config+='### The output files (comma separated list)\n'
    config+='output_file = rootTupleMaker_CRAB_DATA_2012_53X.root\n'
    config+='\n'
    config+='\n'
    config+='[USER]\n'
    config+='thresholdLevel          = 100\n'
    config+='use_central_bossDB      = 0\n'
    config+='use_boss_rt             = 0\n'
    config+='email =jalmond@cern.ch\n'
    config+='\n'
    config+='\n'
    config+='### OUTPUT files Management\n'
    config+='##  output back into UI\n'
    config+='ui_working_dir =  ' + dir + "/" + uidir +'\n'
    config+='return_data = 0\n'
    config+='\n'
    config+='\n'
    config+='## OUTPUT files INTO A SE\n'
    config+='copy_data = 1\n'
    config+='\n'
    config+='### if you want to copy data in a "official CMS site"\n'
    config+='### you have to specify the name as written in \n'
    config+='\n'
    config+='storage_element = T3_KR_KISTI\n'
    config+='user_remote_dir = Collision12_tag18/LQ_2016_AprilData_loosept_'+uidir+'\n'
    config+='\n'
    config+='### To publish produced output in a local istance of DBS set publish_data = 1\n'
    config+='publish_data = 1\n'
    config+='publish_data_name = LQNtupleSNU_Data_PF2PAT2016_'+uidir+'\n' 
    config+='\n'
    config+='#### Specify the dataset name. The full path will be <primarydataset>/<publish_data_name>/USER\n'
    config+='\n'
    config+='eMail = jalmond@cern.ch\n'
    config+='[GRID]\n'
    config+='\n'
    config+='se_black_list = cream01.iihe.ac.be,T2_US_Wisconsin,T2_US_MIT,T2_US_Nebraska,T2_US_UCSD\n'
    config+='#se_white_list = charm.ucr.edu\n'
    config+='\n'

    
    return config

import sys,os
import argparse
import re
import optparse
sys.path.append('..')
import DAS_filesearch as search
import json


parser = argparse.ArgumentParser(description='condor for postproc')
parser.add_argument('-f', dest='file', default='', help='json file input')
args = parser.parse_args()

with open(args.file, "r") as f:
    jsons = json.load(f)
    f.close()

for dataset in jsons:
    
    print "dataset name:", dataset['name']
    print "year: ", dataset['year'], '\n'

    datasetname = dataset['name'].split('/')[1]+"_"+dataset['name'].split('/')[2]
    os.system("mkdir -p "+datasetname+"/log")
    os.chdir(datasetname)
    search.getLFN(dataset['name'], datasetname)


    with open ("filepath_"+datasetname+".txt","r") as f0:
        lines = f0.readlines()
        f0.close()


    i = 0
    for line in lines:
        line = line.rstrip('\n')
        filepath = search.getValidSite(line)+line 
        filename = line.split('.root')[0].split('/')
        filename = filename[len(filename)-1] 
        i += 1


        # prepare submit code
        Proxy_path = "/afs/cern.ch/user/s/sdeng/.krb5/x509up_u109738"
        with open ("submit_"+datasetname+"_file"+str(i)+"_"+filename+".jdl","w+") as f:
            f.write("universe \t = vanilla\n")
            f.write("executable \t = wrapper_"+datasetname+"_file"+str(i)+"_"+filename+".sh\n")
            f.write("requirements \t = (OpSysAndVer =?= \"CentOS7\")\n")
            f.write("+JobFlavour \t = testmatch\n\n")
            f.write("request_cpus \t = 4\n")
            f.write("request_memory \t = 4096\n")
            f.write("request_disk \t = 4096000\n\n")
            f.write("error \t = log/"+datasetname+"_file"+str(i)+"_"+filename+".err\n")
            f.write("output \t = log/"+datasetname+"_file"+str(i)+"_"+filename+".output\n")
            f.write("log \t = log/"+datasetname+"_file"+str(i)+"_"+filename+".log\n\n")
            f.write("should_transfer_files \t = YES\n")
            # f.write("transfer_input_files \t = filepath_"+datasetname+".txt\n")
            # f.write("transfer_output_remaps \t = \"test.root = "+datasetname+"_file"+filename+".root\"\n")
            f.write("when_to_transfer_output \t = ON_EXIT\n")
            f.write("+MaxRuntime = 49600\n")
            f.write("queue 1")
        f.close()
        print "file",str(i),filename," submit code prepared"


        # prepare shell
        with open ("wrapper_"+datasetname+"_file"+str(i)+"_"+filename+".sh","w+") as f:
            f.write("#!/bin/bash\n\n")
            # f.write("voms-proxy-info -all\n")
            f.write("voms-proxy-info -all -file "+Proxy_path+"\n")
            f.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n\n")
            f.write("initial_path=${PWD}\n")
            f.write("scramv1 project CMSSW CMSSW_10_6_0\n")
            f.write("cd CMSSW_10_6_0/src\n")
            f.write("eval `scramv1 runtime -sh`\n\n")
            f.write("git clone https://github.com/Senphy/nanoAOD-WVG.git PhysicsTools/NanoAODTools\n")
            f.write("scram b -j4\n\n")
            f.write("cd PhysicsTools/NanoAODTools/WZG_selector/data\n")
            # f.write("cp ${initial_path}/filepath_"+datasetname+".txt .\n" )
            f.write("python WZG_postproc_data.py -f "+filepath+" -j "+dataset['json']+"\n\n")
            f.write("cp *.root ${initial_path}")
            # f.write("python ${CMSSW_BASE}/src/PhysicsTools/NanoAODTools/scripts/haddnano.py test.root *.root\n")
            # f.write("cp test.root ${initial_path}\n")
            f.close()
        print "file",str(i),filename," shell prepared"


        os.system("condor_submit submit_"+datasetname+"_file"+str(i)+"_"+filename+".jdl")
        print "file",str(i),filename," submitted\n"


    print "total "+str(i)+" file(s) submitted\n"


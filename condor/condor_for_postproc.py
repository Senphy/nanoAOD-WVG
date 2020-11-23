import sys,os
import argparse
import re
import optparse
sys.path.append('..')
import WZG_selector.DAS_filesearch as search


parser = argparse.ArgumentParser(description='condor for postproc')
parser.add_argument('-y', dest='year', default='2016', help='year of dataset')
parser.add_argument('-n', dest='name', default='test', help='dataset name in short, currently support' 
    '\n tZq_ll'
    '\n WZ'
    '\n TTWJetsToLNu'
    '\n ttZJets')
args = parser.parse_args()

print "year: ", args.year
print "dataset name:", args.name




os.system("mkdir -p Submit_WZG_Postproc/log")

if args.name == 'tZq_ll':
    if args.year == '2016': dataset = "/tZq_ll_4f_13TeV-amcatnlo-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM"
elif args.name == 'WZ':
    if args.year == '2016': dataset = "/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM"
elif args.name == 'TTWJetsToLNu':
    if args.year == '2016': dataset = "/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM"
elif args.name == 'ttZJets':
    if args.year == '2016': dataset = "/ttZJets_13TeV_madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM"
else:
    print "unknown dataset name"
    sys.exit(0)




# prepare submit code
Proxy_path = "/afs/cern.ch/user/s/sdeng/.krb5/x509up_u109738"
with open ("Submit_WZG_Postproc/submit_"+args.name+"_"+args.year+".jdl","w+") as f:
    f.write("universe = vanilla\n")
    f.write("arguments = $(Proxy_path)\n")
    f.write("executable = wrapper_"+args.name+"_"+args.year+".sh\n")
    f.write("requirements = (OpSysAndVer =?= \"CentOS7\")\n")
    f.write("transfer_input_files = filepath_"+args.name+"_"+args.year+".txt\n")
    f.write("+JobFlavour = testmatch\n")
    f.write("should_transfer_files = YES\n")
    f.write("RequestCpus = 4\n")
    f.write("error = error/"+args.name+"_"+args.year+".err\n")
    f.write("output = output/"+args.name+"_"+args.year+".output\n")
    f.write("log = log/"+args.name+"_"+args.year+".log\n")
    f.write("queue 1")
f.close()

# prepare shell
with open ("Submit_WZG_Postproc/wrapper_"+args.name+"_"+args.year+".sh","w+") as f:
    f.write("#!usr/bin/env bash\n\n")
    f.write("voms-proxy-info -all\n")
    f.write("voms-proxy-info -all -file "+Proxy_path+"\n")
    f.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n\n")
    f.write("initial_path=${PWD}\n")
    f.write("scramv1 project CMSSW CMSSW_10_6_0\n")
    f.write("cd CMSSW_10_6_0/src\n")
    f.write("eval `scramv1 runtime -sh`\n\n")
    f.write("git clone https://github.com/Senphy/nanoAOD-WVG.git PhysicsTools/NanoAODTools\n")
    f.write("scram b -j4\n\n")
    f.write("cd PhysicsTools/NanoAODTools/WZG_selector\n")
    f.write("cp ${initial_path}/filepath_"+args.name+"_"+args.year+".txt .\n" )
    f.write("python WZG_postproc.py -m condor -n "+args.name+" -y "+args.year+"\n\n")
    f.write("python ${CMSSW_BASE}/src/PhysicsTools/NanoAODTools/scripts/haddnano.py test.root *.root\n")
    f.write("cp test.root ${initial_path}\n")



os.chdir("Submit_WZG_Postproc")
search.getFilePath(dataset, args.name+"_"+args.year)
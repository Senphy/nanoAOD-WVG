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
print "dataset name:", args.name, '\n'




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




os.system("mkdir -p Submit_WZG_Postproc_"+args.name+"_"+args.year+"/log")
os.chdir("Submit_WZG_Postproc_"+args.name+"_"+args.year)
search.getLFN(dataset, args.name+"_"+args.year)


with open ("filepath_"+args.name+"_"+args.year+".txt","r") as f0:
    lines = f0.readlines()
    i = 0


    for line in lines:
        line = line.rstrip('\n')
        filename = line.split('.root')[0].split('/')
        filename = filename[len(filename)-1] 
        i += 1


        # prepare submit code
        Proxy_path = "/afs/cern.ch/user/s/sdeng/.krb5/x509up_u109738"
        with open ("submit_"+args.name+"_"+args.year+"_file"+str(i)+"_"+filename+".jdl","w+") as f:
            f.write("universe \t = vanilla\n")
            f.write("executable \t = wrapper_"+args.name+"_"+args.year+"_file"+str(i)+"_"+filename+".sh\n")
            f.write("requirements \t = (OpSysAndVer =?= \"CentOS7\")\n")
            f.write("+JobFlavour \t = testmatch\n\n")
            f.write("request_cpus \t = 4\n")
            f.write("request_memory \t = 4096\n")
            f.write("request_disk \t = 4096000\n\n")
            f.write("error \t = log/"+args.name+"_"+args.year+"_file"+str(i)+"_"+filename+".err\n")
            f.write("output \t = log/"+args.name+"_"+args.year+"_file"+str(i)+"_"+filename+".output\n")
            f.write("log \t = log/"+args.name+"_"+args.year+"_file"+str(i)+"_"+filename+".log\n\n")
            f.write("should_transfer_files \t = YES\n")
            # f.write("transfer_input_files \t = filepath_"+args.name+"_"+args.year+".txt\n")
            # f.write("transfer_output_remaps \t = \"test.root = "+args.name+"_"+args.year+"_file"+filename+".root\"\n")
            f.write("when_to_transfer_output \t = ON_EXIT\n")
            f.write("queue 1")
        f.close()
        print "file",str(i),filename," submit code prepared"


        # prepare shell
        with open ("wrapper_"+args.name+"_"+args.year+"_file"+str(i)+"_"+filename+".sh","w+") as f:
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
            f.write("cd PhysicsTools/NanoAODTools/WZG_selector\n")
            # f.write("cp ${initial_path}/filepath_"+args.name+"_"+args.year+".txt .\n" )
            f.write("python WZG_postproc.py -m condor -n "+args.name+" -y "+args.year+" -f "+line+"\n\n")
            f.write("cp *.root ${initial_path}")
            # f.write("python ${CMSSW_BASE}/src/PhysicsTools/NanoAODTools/scripts/haddnano.py test.root *.root\n")
            # f.write("cp test.root ${initial_path}\n")
            f.close()
        print "file",str(i),filename," shell prepared"


        os.system("condor_submit submit_"+args.name+"_"+args.year+"_file"+str(i)+"_"+filename+".jdl")
        print "file",str(i),filename," submitted\n"


    print "total "+str(i)+" file(s) submitted\n"
    f0.close()


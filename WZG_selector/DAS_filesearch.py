import sys,os
import argparse
import re
import optparse


def getFilePath(dataset, name):

    print "Searching for LFN"
    os.system("/cvmfs/cms.cern.ch/common/dasgoclient --query=\"file dataset="+dataset+"\" -limit=0 > filepath_"+name+".txt")
    print "LFN prepared\n"


    with open ("filepath_"+name+".txt") as f:
        lines = f.readlines()
        f.close()


    with open ("filepath_"+name+".txt","w+") as f:
        for line in lines:
            line = line.rstrip('\n') 


            print "Searching for valid site"
            os.system("cmsRun ${CMSSW_BASE}/src/PhysicsTools/NanoAODTools/WZG_selector/test_ValidSite_cfg.py inputFiles=\""+line+"\" > test_ValidSite.log 2>&1")


            with open ("test_ValidSite.log","r") as test:
                test_lines = test.read()
                # print test_lines
                if 'Successfully' in test_lines:
                    valid_site = test_lines.split('Successfully opened file ')[1].split('/store/mc')[0]
                    print "valid site for ", line, ": ", valid_site, "\n"
                    f.write(valid_site+line+"\n")


                else:
                    print "no accessable site for "+line
                    os.remove("test_ValidSite.log")
                    sys.exit(0)


                test.close()


            os.remove("test_ValidSite.log")


        # f.write("root://cms-xrd-global.cern.ch//eos/cms"+line)
        f.close()

if __name__ =="__main__":
    getFilePath(dataset,name)


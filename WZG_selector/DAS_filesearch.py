import sys,os
import argparse
import re
import optparse


def getLFN(dataset, name):

    print "Searching for LFN"
    os.system("/cvmfs/cms.cern.ch/common/dasgoclient --query=\"file dataset="+dataset+"\" -limit=0 > filepath_"+name+".txt")
    print "LFN prepared\n"


def getValidSite(filepath):


            print "Searching for valid site"
            os.system("cmsRun ${CMSSW_BASE}/src/PhysicsTools/NanoAODTools/nanoAOD-WVG/WZG_selector/test_ValidSite_cfg.py inputFiles=\""+filepath+"\" > test_ValidSite.log 2>&1")


            with open ("test_ValidSite.log","r") as test:
                test_lines = test.read()
                # print test_lines
                if 'Successfully' in test_lines:
                    if '/store/mc' in test_lines:
                        valid_site = test_lines.split('Successfully opened file ')[1].split('/store/mc')[0]
                    if '/store/data' in test_lines:
                        valid_site = test_lines.split('Successfully opened file ')[1].split('/store/data')[0]
                    print "valid site for ", filepath, ": ", valid_site, "\n"
                    return(valid_site)


                else:
                    print "no accessable site for "+filepath
                    os.remove("test_ValidSite.log")
                    return

                test.close()


            os.remove("test_ValidSite.log")

if __name__ == '__main__':
    getLFN(sys.argv[1], sys.argv[1].split('/')[1])
    with open('filepath_'+sys.argv[1].split('/')[1]+".txt") as f:
        lines = f.readlines()
        for line in lines:
            line = line.rstrip('\n')
            getValidSite(line)
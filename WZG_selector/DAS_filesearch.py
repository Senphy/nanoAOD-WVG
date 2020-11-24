import sys,os
import argparse
import re
import optparse


def getFilePath(dataset, name):

    os.system("/cvmfs/cms.cern.ch/common/dasgoclient --query=\"file dataset="+dataset+"\" -limit=0 > filepath_"+name+".txt")

    with open ("filepath_"+name+".txt") as f:
        lines = f.readlines()
        f.close()
    with open ("filepath_"+name+".txt","w+") as f:
        for line in lines:
            # f.write("root://cms-xrd-global.cern.ch//eos/cms"+line)
            f.write("root://cms-xrd-global.cern.ch/"+line)
        f.close()


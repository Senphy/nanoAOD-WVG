import sys,os
import argparse
import re
import optparse


def getFilePath(dataset):

    os.system("/cvmfs/cms.cern.ch/common/dasgoclient --query=\"file dataset="+dataset+"\" -limit=0 > filepath.txt")

    with open ("filepath.txt") as f:
        lines = f.readlines()
        f.close()
    with open ("filepath.txt","w+") as f:
        for line in lines:
            f.write("root://xrootd-cms.infn.it//eos/cms"+line)
        f.close()


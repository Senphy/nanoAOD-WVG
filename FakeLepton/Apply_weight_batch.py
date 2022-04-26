import os,sys
import argparse
import json
import subprocess
import shutil

if __name__ == '__main__':

    year = "2018"
    store_path = "/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/%s/" %(year)

    for file in os.listdir(store_path):
        if not file.endswith('.root'):
            print ('%s is not an applicable file' %(file))
            continue
        try:
            os.system("python Apply_weight_Template_postproc.py -f %s/%s -y %s" %(store_path, file, str(year)))
        except:
            print ('%s is not an applicable file' %(file))
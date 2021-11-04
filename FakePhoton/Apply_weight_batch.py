import os,sys
import argparse
import json
import subprocess
import shutil

if __name__ == '__main__':

    store_path = "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2018"

    for file in os.listdir(store_path):
        try:
            os.system("python Apply_weight_FakePho_Template_postproc.py -f " + store_path + '/' +file)
        except:
            print (f'{file} is not an applicable file')
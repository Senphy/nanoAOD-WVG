import os,sys
import argparse
import json
import subprocess
import shutil

parser = argparse.ArgumentParser(description='Apply weight batchly')
parser.add_argument('-f', dest='file', default='', help='json file input')
args = parser.parse_args()

def get_abbre(name,sample_type,year):
    if sample_type == 'MC':
        return name.split('/')[1] + '_' + year
    elif sample_type == 'data':
        return name.split('/')[1] + '_' + name.split('/')[2].split('-')[0]

if __name__ == '__main__':

    store_path = "/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/"

    with open(args.file, "r") as f:
        jsons = json.load(f)
        f.close()

    for dataset in jsons:
        abbre_name = get_abbre(dataset['name'], dataset['type'], str(dataset['year']))
        os.system("python Apply_weight_Template_postproc.py -f "+store_path+abbre_name+".root")
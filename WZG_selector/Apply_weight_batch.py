import os,sys
import argparse
import json
import subprocess
import shutil

parser = argparse.ArgumentParser(description='create attachment NanoAOD-like fake photon result')
parser.add_argument('-p', dest='path', default='/eos/user/s/sdeng/WZG_analysis/final_skim/', help='File path input')
parser.add_argument('-y', dest='year', default='2018', help='year')
args = parser.parse_args()

if __name__ == '__main__':

    store_path = '{path}/{year}'.format(path=args.path, year=args.year)

    for file in os.listdir(store_path):
        if file.endswith('.root'):
            try:
                os.system('python Apply_weight_Template_postproc.py -f {store_path}/{file} -y {year}'.format(store_path=store_path, file=file, year=args.year))
                new_file = file.rsplit('.root')[0] + '_Skim.root'
                os.system('mv {new_file} {file}'.format(file=file, new_file=new_file))
            except:
                print ('{file} is not an applicable file'.format(file=file))
        else:
            print ('{file} is not an applicable file'.format(file=file))
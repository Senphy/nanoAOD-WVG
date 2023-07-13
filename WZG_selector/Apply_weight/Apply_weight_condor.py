import argparse
from logging import raiseExceptions
import os,sys
import argparse

parser = argparse.ArgumentParser(description='create attachment NanoAOD-like fake photon result')
parser.add_argument('-p', dest='path', default='/eos/user/s/sdeng/WZG_analysis/final_skim/', help='File path input')
parser.add_argument('-y', dest='year', default='2016Pre', help='year')
parser.add_argument('-t', dest='tar', default=False, action='store_true', help='tar CMS env')
args = parser.parse_args()

def prepare_condor(path=None, file=None, year=None, isdata=None, **kwargs):
    _name = file.split('.root')[0]
    skim_name = f'{_name}_Skim.root'
    with open(f'submit_{_name}.jdl', 'w+') as f:
        submit_string = \
        f'''universe = vanilla
executable = Apply_weight.sh
requirements = (OpSysAndVer =?= "CentOS7")

arguments = {path} {file} {year} {skim_name} {isdata} $(Cluster) $(Process)
use_x509userproxy  = true
+JobFlavour = "testmatch"

should_transfer_files = IF_NEEDED
transfer_input_files = ../Apply_weight_Template_postproc.py,../Apply_weight_keep_and_drop.txt,../Apply_weight_output_branch_selection.txt,cmssw_setup.sh,sandbox-CMSSW_10_6_29-WZG.tar.bz2

RequestCpus = 4
RequestDisk = 10240000
RequestMemory = 10240
error = log/{_name}_{year}.err
output = log/{_name}_{year}.out
log = log/{_name}_{year}.log
when_to_transfer_output = NO
queue 1'''
        f.write(submit_string)
        pass
    os.system(f'condor_submit submit_{_name}.jdl')

if __name__ == '__main__':
    if args.tar:
        os.system('python cmssw_sandbox.py -v create $CMSSW_BASE -U')
    for file in os.listdir(f'{args.path}/{args.year}'):
        if file.endswith('.root'):
            if f'Run{args.year}' in file or 'Run2016' in file:
                prepare_condor(path=args.path, file=file, year=args.year, isdata='-d')
            else:
                continue
                # try:
                prepare_condor(path=args.path, file=file, year=args.year)
                # except:
                    # print(f'{file} not applicable')
        else:
            print(f'{file} not applicable')
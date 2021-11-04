import os,sys
import argparse
import json
import subprocess
import shutil

parser = argparse.ArgumentParser(description='prepare crab code')
parser.add_argument('-f', dest='file', default='', help='json file input')
parser.add_argument('-m', dest='mode', default='', help='work mode')
args = parser.parse_args()

def get_abbre(name,sample_type,year):
    if sample_type == 'MC':
        return name.split('/')[1] + '_' + year
    elif sample_type == 'data':
        return name.split('/')[1] + '_' + name.split('/')[2].split('-')[0]

def prepare_crab(name,sample_type,year,period):

    abbre_name = get_abbre(name,sample_type,year) 
    if not os.path.exists('crabcode_' + year):
        os.mkdir("crabcode_" + year)

    print ("------> preparing submit code for",abbre_name)
    with open('crabcode_' + year + '/' + abbre_name + '_cfg.py', 'w+') as f:
        f.write('from WMCore.Configuration import Configuration \n\n')

        f.write('config = Configuration()\n')
        f.write('config.section_("General")\n')
        f.write('config.General.requestName = "' + abbre_name + '"\n')
        f.write('config.General.transferLogs = False \n')
        f.write('config.General.workArea = "crab' + year + '"\n\n')

        f.write('config.section_("JobType")\n')
        f.write('config.JobType.pluginName = "Analysis"\n')
        f.write('config.JobType.psetName = "PSet.py"\n')
        f.write('config.JobType.scriptExe = "./full_crab_script.sh" \n')
        f.write('config.JobType.inputFiles = ["../../scripts/haddnano.py","./full_Template_postproc.py","./full_keep_and_drop.txt","./full_output_branch_selection.txt"] #hadd nano will not be needed once nano tools are in cmssw \n')
        f.write('config.JobType.scriptArgs = ["isdata=' + sample_type + '","year=' + year + '","period=' + period + '"] \n')
        f.write('config.JobType.sendPythonFolder  = True\n')
        f.write('config.JobType.allowUndistributedCMSSW = True \n\n')
        f.write('config.JobType.maxJobRuntimeMin = 4320 \n\n')

        f.write('config.section_("Data")\n')
        f.write('config.Data.inputDataset = "' + name + '" \n')
        f.write('#config.Data.inputDBS = "phys03"\n')
        f.write('config.Data.inputDBS = "global"\n')
        if sample_type == 'MC' or ('MuonEG_Run2018D' in abbre_name):
            f.write('config.Data.splitting = "FileBased"\n')
            f.write('config.Data.unitsPerJob = 1\n')
        elif sample_type == 'data' and ('MuonEG_Run2018D' not in abbre_name):
            f.write('config.Data.splitting = "LumiBased"\n')
            f.write('config.Data.unitsPerJob = 80\n')

        if sample_type == 'MC':
            pass
        elif year == '2018':
            # f.write('config.Data.lumiMask = "https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt" \n\n')
            # f.write('config.Data.lumiMask = "test.json" \n\n')
            if 'MuonEG_Run2018' not in abbre_name:
                f.write('config.Data.lumiMask = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt" \n\n')
            else:
                f.write('config.Data.lumiMask = "" \n\n')
        elif year == '2017':
            f.write('config.Data.lumiMask = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt" \n\n')

        f.write('config.Data.outLFNDirBase ="/store/user/sdeng/WZG_analysis/fake_photon_template/AR/' + sample_type + '/' + year + '"\n')
        f.write('config.Data.publication = False\n')
        f.write('config.Data.ignoreLocality = True\n')
        f.write('config.Data.allowNonValidInputDataset = True\n')
        f.write('config.Data.outputDatasetTag = "' + abbre_name + '" \n\n')

        f.write('config.section_("Site")\n')
        f.write('config.Site.storageSite = "T3_CH_CERNBOX"\n')
        f.write('config.Site.whitelist = ["T2_US_MIT","T2_US_Wisconsin","T2_US_Purdue","T2_US_UCSD","T2_US_Caltech"] \n')
        f.close()

def submit(name,sample_type,year):

    abbre_name = get_abbre(name,sample_type,year)

    if not os.path.exists(f'crabcode_{year}/{abbre_name}_cfg.py'):
        print ("crabcode for ",abbre_name," not existed, \033[31mskipping\033[0m")
        return True

    r=subprocess.run(args=f"crab submit -c crabcode_{year}/{abbre_name}_cfg.py",shell=True,stdout=subprocess.PIPE,encoding='utf-8')
    if 'Success' in r.stdout:
        print ("--------> submit info:","submit crab jobs for",abbre_name)
    else:
        print ("--------> submit info:","\033[31mfail\033[0m to submit for",abbre_name)

def kill(name,sample_type,year):

    abbre_name = get_abbre(name,sample_type,year)

    if not os.path.exists(f'crab{year}/crab_{abbre_name}'):
        print ("crab log for ",abbre_name," not existed, \033[31mskipping\033[0m \n")
        return True

    r=subprocess.run(args=f"crab kill -d crab{year}/crab_{abbre_name}" ,shell=True,stdout=subprocess.PIPE,encoding='utf-8')
    print (r.stdout,'\n')

    shutil.rmtree(f'crab{year}/crab_{abbre_name}')
    print (f'crab{year}/crab_{abbre_name} has been removed')


def status(name,sample_type,year):

    abbre_name = get_abbre(name,sample_type,year)

    if not os.path.exists(f'crab{year}/crab_{abbre_name}'):
        print ("crab log for ",abbre_name," not existed, \033[31mskipping\033[0m \n")
        return True

    r=subprocess.run(args=f"crab status -d crab{year}/crab_{abbre_name}" ,shell=True,stdout=subprocess.PIPE,encoding='utf-8')
    print (r.stdout,'\n')


def hadd_help(name,sample_type,year):

    abbre_name = get_abbre(name,sample_type,year)
    store_path = '/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/'
    first_name = name.split('/')[1]

    if os.path.exists(f'{abbre_name}.root'):
        print (f'{abbre_name} already existed, \033[31mskipping\033[0m')
        return True

    if not (os.path.exists(f'{store_path}/{sample_type}/{year}/{first_name}/{abbre_name}')):
        print (f'results for {abbre_name} not existed in {store_path}/{sample_type}/{year}/{first_name}/{abbre_name}, \033[31mskipping\033[0m\n')
        return True
    
    if not (len(os.listdir(f'{store_path}/{sample_type}/{year}/{first_name}/{abbre_name}')) == 1 ):
        print (f'more than 1 result for {abbre_name}, Please check {store_path}/{sample_type}/{year}/{first_name}/{abbre_name}\n')
        return True

    run_number = os.listdir(f'{store_path}/{sample_type}/{year}/{first_name}/{abbre_name}')[0]
    path = f'{store_path}/{sample_type}/{year}/{first_name}/{abbre_name}/{run_number}/'
    print (f'hadding root files in {path}')
    for i in os.listdir(path):
        # print (f'{path}/{i}/*.root')
        r=subprocess.run(args=f"andrew_haddnano.py {abbre_name}_{i}.root {path}/{i}/*.root ", shell=True,stdout=subprocess.PIPE,encoding='utf-8')
    
        if os.path.exists(f'{abbre_name}_{i}.root'):
            print (f'hadd \033[32mcomplete\033[0m, please check {abbre_name}_{i}.root\n')
        else:
            print (f'hadd \033[31m fail \033[0m!!')

def report_lumi(name,sample_type,year):

    abbre_name = get_abbre(name,sample_type,year)
    if not os.path.exists(f'crab{year}/crab_{abbre_name}'):
        print ("crab log for ",abbre_name," not existed, \033[31mskipping\033[0m \n")
        return True

    r=subprocess.run(args=f"crab report -d crab{year}/crab_{abbre_name}" ,shell=True,stdout=subprocess.PIPE,encoding='utf-8')
    print (r.stdout,'\n')

    if not os.path.exists(f'lumi_{year}'):
        os.mkdir(f'lumi_{year}')
    
    shutil.copy(f'crab{year}/crab_{abbre_name}/results/notFinishedLumis.json', f'lumi_{year}/{abbre_name}.json')

def resubmit(name,sample_type,year):

    abbre_name = get_abbre(name,sample_type,year)

    if not os.path.exists(f'crab{year}/crab_{abbre_name}'):
        print ("crab log for ",abbre_name," not existed, \033[31mskipping\031[0m \n")
        return True

    print (f"resubmitting {abbre_name}\n")
    r = subprocess.run(args=f"crab resubmit -d crab{year}/crab_{abbre_name}" ,shell=True,stdout=subprocess.PIPE,encoding='utf-8')
    print (r.stdout,"\n")


if __name__=='__main__':
    
    with open(args.file, "r") as f:
        jsons = json.load(f)
        f.close()

    if args.mode == 'prepare':
        for dataset in jsons:
            prepare_crab(dataset['name'], dataset['type'], str(dataset['year']), dataset['period'])
    
    if args.mode == 'submit':
        for dataset in jsons:
            submit(dataset['name'], dataset['type'], str(dataset['year']))

    if args.mode == 'kill':
        for dataset in jsons:
            kill(dataset['name'], dataset['type'], str(dataset['year']))
    
    if args.mode == 'status':
        for dataset in jsons:
            status(dataset['name'], dataset['type'], str(dataset['year']))

    if args.mode == 'hadd':
        for dataset in jsons:
            hadd_help(dataset['name'], dataset['type'], str(dataset['year']))

    if args.mode == 'report':
        for dataset in jsons:
            if dataset['type'] == 'data':
                report_lumi(dataset['name'], dataset['type'], str(dataset['year']))
    
    if args.mode == 'resubmit':
        for dataset in jsons:
            resubmit(dataset['name'], dataset['type'], str(dataset['year']))



import mplhep as hep
import pandas as pd
import os, sys
from array import array
from copy import deepcopy
import time
import argparse
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import boost_histogram as bh
import uproot
import awkward
import json
import numba
import threading
import logging
import ROOT
import warnings
from Prepare_hist_turbo import WZG_plot
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

class WZG_plot_condor(WZG_plot):
    def __init__(self, year='2018', region='WZG', file='', plottype=1, isdata=False, mcname='', **kwargs):
        super(WZG_plot_condor, self).__init__(year=year, region=region, **kwargs)
        self.file = file
        # type: 1: nominal, 2: fakelep, 3: fakepho
        self.plottype = plottype
        self.isdata = isdata
        self.mcname = mcname

    def abbr_name(self, file):
        if not file.endswith('.root'):
            raise Exception(f'{file} Not a valid file')
        dirt_0, suffix = os.path.splitext(file)
        dirt_1, filename = os.path.split(dirt_0)
        return filename

    def hist_store(self, hists, **kwargs):
        store_name = self.abbr_name(self.file)
        plottype_map = {
            1: 'nom',
            2: 'fakelep',
            3: 'fakepho'
        }
        output = uproot.recreate(f'{self.region}_{store_name}_{plottype_map[plottype]}_{self.year}.root')
        year_suffix_map ={
            '2016Pre':'16',
            '2016Post':'16',
            '2016':'16',
            '2017':'17',
            '2018':'18',
        }
        year_suffix = year_suffix_map[self.year]
        for branch_name in self.branch:
            plotbranch = self.branch[branch_name]['name']
            if self.plottype == 1:
                if self.isdata:
                    # store data
                    output[f'{self.channel_map[self.channel]}_{plotbranch}_data_None'] = hists[branch_name]
                else:
                    # merge mc
                    unc_total = deepcopy(self.unc_map)
                    unc_total.update(self.unc_special_map)
                    self.branch[branch_name]['hists'] = {}
                    suffix_list = ['Nom']
                    suffix_list.extend([f'{unc}Up' for unc in unc_total])
                    suffix_list.extend([f'{unc}Down' for unc in unc_total])
                    for group in self.plot_groups:
                        self.branch[branch_name]['hists'][group] = {}
                        if self.branch[branch_name].__contains__('bin_array'):
                            for suffix in suffix_list:
                                self.branch[branch_name]['hists'][group][suffix] = bh.numpy.histogram([], bins=self.branch[branch_name]['bin_array'], density=False, histogram=bh.Histogram, storage=bh.storage.Weight())
                        else:
                            xbins = self.branch[branch_name]['xbins']
                            xleft = self.branch[branch_name]['xleft']
                            xright = self.branch[branch_name]['xright']
                            for suffix in suffix_list:
                                self.branch[branch_name]['hists'][group][suffix] = bh.numpy.histogram([], bins=xbins, range=(xleft, xright), density=False, histogram=bh.Histogram, storage=bh.storage.Weight())
                    for file in hists:
                        for group in self.plot_groups:
                            if hists[file]['name'].lower() in self.plot_groups[group]['names']:
                                self.branch[branch_name]['hists'][group]['Nom'] += hists[file][branch_name]
                                for unc in unc_total:
                                    self.branch[branch_name]['hists'][group][f'{unc}Up'] += hists[file][f'{branch_name}_{unc}Up']
                                    self.branch[branch_name]['hists'][group][f'{unc}Down'] += hists[file][f'{branch_name}_{unc}Down']
                                continue
                    # store mc
                    for group in self.plot_groups:
                        output[f'{self.channel_map[self.channel]}_{plotbranch}_{group}_None'] = self.branch[branch_name]['hists'][group]['Nom']
                        for unc in unc_total:
                            if unc_total[unc]['corr'] == 1:
                                output[f'{self.channel_map[self.channel]}_{plotbranch}_{group}_{unc}Up'] = self.branch[branch_name]['hists'][group][f'{unc}Up']
                                output[f'{self.channel_map[self.channel]}_{plotbranch}_{group}_{unc}Down'] = self.branch[branch_name]['hists'][group][f'{unc}Down']
                            else:
                                output[f'{self.channel_map[self.channel]}_{plotbranch}_{group}_{unc}_{year_suffix}Up'] = self.branch[branch_name]['hists'][group][f'{unc}Up']
                                output[f'{self.channel_map[self.channel]}_{plotbranch}_{group}_{unc}_{year_suffix}Down'] = self.branch[branch_name]['hists'][group][f'{unc}Down']
            elif self.plottype == 2:
                output[f'{self.channel_map[self.channel]}_{plotbranch}_FakeLep_None'] = hists[branch_name]
                output[f'{self.channel_map[self.channel]}_{plotbranch}_FakeLep_fakerate_{year_suffix}Up'] = hists[f'{branch_name}_fakerateUp']
                output[f'{self.channel_map[self.channel]}_{plotbranch}_FakeLep_fakerate_{year_suffix}Down'] = hists[f'{branch_name}_fakerateDown']
            elif self.plottype == 3:
                output[f'{self.channel_map[self.channel]}_{plotbranch}_FakePho_None'] = hists[branch_name]
                for _unc in self._fakepho_unc_list:
                    for _suffix in ['Up','Down']:
                        if _unc == 'stat':
                            output[f'{self.channel_map[self.channel]}_{plotbranch}_FakePho_FakePho_{_unc}_{year_suffix}{_suffix}'] = hists[f'{branch_name}_{_unc}_{_suffix.lower()}']
                        else:
                            output[f'{self.channel_map[self.channel]}_{plotbranch}_FakePho_FakePho_{_unc}{_suffix}'] = hists[f'{branch_name}_{_unc}_{_suffix.lower()}']

    def run(self):
        hists = {}
        if self.isdata:
            if self.plottype == 1:
                hists = self.AddHist(self.file, hists=hists, isData=True)
            elif self.plottype == 2:
                hists = self.AddHist_FakeLep(self.file, hists=hists, isData=True)
            elif self.plottype == 3:
                hists = self.AddHist_FakePho(self.file, hists=hists, isData=True)
        else:
            if self.plottype == 1:
                hists[self.mcname] = {}
                hists[self.mcname]['name'] = self.filelist_MC[self.mcname]['name']
                hists[self.mcname] = self.AddHist(self.file, hists=hists[self.mcname], isData=False, xsec=self.filelist_MC[self.mcname]['xsec'])
            elif self.plottype == 2:    
                hists = self.AddHist_FakeLep(self.file, hists=hists, isData=False, xsec=self.filelist_MC[self.mcname]['xsec'])
            elif self.plottype == 3:    
                hists = self.AddHist_FakePho(self.file, hists=hists, isData=False, xsec=self.filelist_MC[self.mcname]['xsec'])
        # print(hists)
        self.hist_store(hists)
        return hists
    

plottype_map = {
    1: 'nom',
    2: 'fakelep',
    3: 'fakepho'
}

def submit_condor(path=None, file=None, year=None, isdata=' ', plottype=1, region='ttZ', mcname=' ', **kwargs):
    _name = file.split('.root')[0]
    if not os.path.exists('condor/log'):
        os.makedirs('condor/log')
    
    output_filename = f'{region}_{_name}_{plottype_map[plottype]}_{year}.root'
    with open(f'condor/submit_{region}_{_name}_{plottype_map[plottype]}_{year}.jdl', 'w+') as f:
        submit_string = \
        f'''universe = vanilla
executable = Prepare_hist_turbo_condor.sh
requirements = (OpSysAndVer =?= "CentOS7")
getenv = True

arguments = {path} {file} {year} {plottype} {region} {output_filename} mcname={mcname} isdata={isdata} 
use_x509userproxy  = true
+JobFlavour = "testmatch"

should_transfer_files = YES
transfer_input_files = Prepare_hist_turbo_condor.py, ./{year}/{region}/Control_pad.py, Prepare_hist_turbo.py

RequestCpus = 2
RequestDisk = 15360000
RequestMemory = 10240
error = condor/log/{region}_{_name}_{plottype_map[plottype]}_{year}.err
output = condor/log/{region}_{_name}_{plottype_map[plottype]}_{year}.out
log = condor/log/{region}_{_name}_{plottype_map[plottype]}_{year}.log
when_to_transfer_output = ON_EXIT_OR_EVICT
queue 1'''
        f.write(submit_string)

    os.system(f'condor_submit condor/submit_{region}_{_name}_{plottype_map[plottype]}_{year}.jdl')

def get_filename(file):
    dirt_1, _filename = os.path.split(file)
    return dirt_1, _filename

def hadd_hist(data_list=[], mc_dict={}, region='', year='2018', **kwargs):
    store_path = '/eos/user/s/sdeng/WZG_analysis/hists/'
    hadd_list = []
    if region in ['WZG','ZGJ']:
        typelist = [1,2,3]
    else:
        typelist = [1,2]
    for filepath in data_list:
        for _plottype in typelist:
            path, filename = get_filename(filepath)
            filename = filename.split('.root')[0]
            filename = f'{region}_{filename}_{plottype_map[_plottype]}_{year}.root'
            if not os.path.exists(f'{store_path}/{filename}'):
                raise FileNotFoundError(f'{filename} not exists in {store_path}')
            hadd_list.append(f'{store_path}/{filename}')
    for mc in mc_dict:
        filepath = mc_dict[mc]['path']
        for _plottype in typelist:
            path, filename = get_filename(filepath)
            filename = filename.split('.root')[0]
            filename = f'{region}_{filename}_{plottype_map[_plottype]}_{year}.root'
            if not os.path.exists(f'{store_path}/{filename}'):
                raise FileNotFoundError(f'{filename} not exists in {store_path}')
            hadd_list.append(f'{store_path}/{filename}')
    
    hadd_string = ''
    for file in hadd_list:
        hadd_string += f'{file} '
    os.system(f'hadd -f {year}/{region}_{year}.root {hadd_string}')

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='plot input')
    parser.add_argument('-y', dest='year', default='2018', choices=['2016Pre','2016Post','2016','2017','2018','RunII'])
    parser.add_argument('-r', dest='region', choices=['ttZ','ZZ','ZGJ','WZG','ttG','ALP'], default='ttZ')
    parser.add_argument('-f', dest='file', default='test.root')
    parser.add_argument('-t', dest='type', default='1', choices=['1', '2', '3'])
    parser.add_argument('-m', dest='mode', default='prepare', choices=['prepare', 'submit', 'hadd'])
    parser.add_argument('-c', dest='iscondor', default=False, action='store_true')
    parser.add_argument('-d', dest='isdata', action='store_true', default=False, help='isdata')
    parser.add_argument('-n', dest='mcname', default='', help='mc name for dict index')
    args = parser.parse_args()

    if args.mode == 'submit':
        sys.path.append(f'./{args.year}/{args.region}')
        import Control_pad as cp
        filelist_data = cp.filelist_data
        filelist_MC = cp.filelist_MC
        filelist_ALP = cp.filelist_ALP
        for filepath in filelist_data:
            path, filename = get_filename(filepath)
            submit_condor(path=path, file=filename, year=args.year, isdata='-d', plottype=1, region=args.region)
            submit_condor(path=path, file=filename, year=args.year, isdata='-d', plottype=2, region=args.region)
            if args.region in ['WZG','ZGJ']:
                submit_condor(path=path, file=filename, year=args.year, isdata='-d', plottype=3, region=args.region)
        for mc in filelist_MC:
            filepath = filelist_MC[mc]['path']
            path, filename = get_filename(filepath)
            submit_condor(path=path, file=filename, year=args.year, plottype=1, region=args.region, mcname=mc)
            submit_condor(path=path, file=filename, year=args.year, plottype=2, region=args.region, mcname=mc)
            if args.region in ['WZG','ZGJ']:
                submit_condor(path=path, file=filename, year=args.year, plottype=3, region=args.region, mcname=mc)
        if args.region in ['ALP']:
            for mc in filelist_ALP:
                filepath = filelist_ALP[mc]['path']
                path, filename = get_filename(filepath)
                submit_condor(path=path, file=filename, year=args.year, plottype=1, region=args.region, mcname=mc)

    elif args.mode == 'prepare':
        plottype = int(args.type)
        WZG_plot_Module = WZG_plot_condor(year=args.year, region=args.region, file=args.file, plottype=plottype, isdata=args.isdata, mcname=args.mcname)
        WZG_plot_Module.run()

    elif args.mode == 'hadd':
        sys.path.append(f'./{args.year}/{args.region}')
        import Control_pad as cp
        filelist_data = cp.filelist_data
        filelist_MC = cp.filelist_MC
        hadd_hist(data_list=filelist_data, mc_dict=filelist_MC, region=args.region, year=args.year)
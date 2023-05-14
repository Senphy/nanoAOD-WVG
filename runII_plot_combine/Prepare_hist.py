import matplotlib
import uproot, uproot3
import numpy
import awkward
import numba
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import pandas as pd
from tqdm import trange
import ROOT
import os,sys
from array import array
from copy import deepcopy
import time
import argparse

sys.path.append('..')
sys.path.append(os.getcwd())
from lumi import CMS_lumi
from AddHist_help import AddHist
from AddHist_help import AddHist_FakeLepton
from AddHist_help import AddHist_FakePhoton
from AddHist_help import SetHistStyle
from AddHist_help import unc_map 
from ratio import createRatio
        
parser = argparse.ArgumentParser(description='plot input')
parser.add_argument('-y', dest='year', default='2018', choices=['2016Pre','2016Post','2017','2018'])
parser.add_argument('-r', dest='region', choices=['ttZ','ZZ','ZGJ','WZG'], default='ttZ')
parser.add_argument('-m', dest='mode', choices=['local','condor'], default='local')
args = parser.parse_args()

def Prepare_hist(year='2018', region='WZG', **kwargs):

    sys.path.append(f'./{year}/{region}')
    from Control_pad import channel_map
    from Control_pad import channel
    from Control_pad import UpDown_map
    from Control_pad import filelist_data
    from Control_pad import filelist_MC
    from Control_pad import branch
    from Control_pad import lumi

    time_total_init = time.time()

    hist_data = {}
    for branch_name in branch:
        plot_branch = branch[branch_name]["name"]
        if branch[branch_name].__contains__("bin_array"):
            hist_data_temp = ROOT.TH1F("", "", len(branch[branch_name]["bin_array"])-1, array('d', branch[branch_name]["bin_array"]))
        else:
            hist_data_temp = ROOT.TH1F("", "", branch[branch_name]["xbins"], branch[branch_name]["xleft"], branch[branch_name]["xright"])
        hist_data_temp.SetXTitle(f'{branch[branch_name]["axis_name"]}')
        hist_data_temp.SetYTitle(f'events / bin')
        SetHistStyle(hist_data_temp, 1)
        hist_data[plot_branch] = deepcopy(hist_data_temp)
    for file in filelist_data:
        AddHist(file, hist_data, 1, 0, 0, channel, branch, year=year)

    for file in filelist_MC:
        hist_MC = {}
        for branch_name in branch:
            plot_branch = branch[branch_name]["name"]
            if branch[branch_name].__contains__("bin_array"):
                hist_MC_temp = ROOT.TH1F("", "", len(branch[branch_name]["bin_array"])-1, array('d', branch[branch_name]["bin_array"]))
            else:
                hist_MC_temp = ROOT.TH1F("", "", branch[branch_name]["xbins"], branch[branch_name]["xleft"], branch[branch_name]["xright"])
            SetHistStyle(hist_MC_temp, filelist_MC[file]["color"])
            hist_MC_temp.SetXTitle(f'{branch[branch_name]["axis_name"]}')
            for UpDown in range(0,5):
                hist_MC[plot_branch+f"_{UpDown_map[UpDown]}"] = deepcopy(hist_MC_temp)
            for unc in unc_map:
                hist_MC[f'{plot_branch}_{unc}Up'] = deepcopy(hist_MC_temp)
                hist_MC[f'{plot_branch}_{unc}Down'] = deepcopy(hist_MC_temp)
            
        AddHist(filelist_MC[file]["path"], hist_MC, 0, filelist_MC[file]["xsec"], lumi, channel, branch, year=year)
        filelist_MC[file]["hist"] = hist_MC
    
    hist_FakeLep = {}
    for branch_name in branch:
        plot_branch = branch[branch_name]["name"]
        if branch[branch_name].__contains__("bin_array"):
            hist_FakeLep_temp = ROOT.TH1F("", "", len(branch[branch_name]["bin_array"])-1, array('d', branch[branch_name]["bin_array"]))
        else:
            hist_FakeLep_temp = ROOT.TH1F("", "", branch[branch_name]["xbins"], branch[branch_name]["xleft"], branch[branch_name]["xright"])
        hist_FakeLep_temp.SetXTitle(f'{branch[branch_name]["axis_name"]}')
        hist_FakeLep_temp.SetYTitle(f'events / bin')
        SetHistStyle(hist_FakeLep_temp,23)
        hist_FakeLep[plot_branch] = deepcopy(hist_FakeLep_temp)
    for file in filelist_data:
        AddHist_FakeLepton(file, hist_FakeLep, 1, 0, 0, channel, branch, year=year)
    for file in filelist_MC:
        AddHist_FakeLepton(filelist_MC[file]["path"], hist_FakeLep, 0, filelist_MC[file]["xsec"], lumi, channel, branch, year)

    hist_FakePho= {}
    for branch_name in branch:
        plot_branch = branch[branch_name]["name"]
        if branch[branch_name].__contains__("bin_array"):
            hist_FakePho_temp = ROOT.TH1F("", "", len(branch[branch_name]["bin_array"])-1, array('d', branch[branch_name]["bin_array"]))
        else:
            hist_FakePho_temp = ROOT.TH1F("", "", branch[branch_name]["xbins"], branch[branch_name]["xleft"], branch[branch_name]["xright"])
        hist_FakePho_temp.SetXTitle(f'{branch[branch_name]["axis_name"]}')
        hist_FakePho_temp.SetYTitle(f'events / bin')
        SetHistStyle(hist_FakePho_temp,30)
        hist_FakePho[plot_branch] = deepcopy(hist_FakePho_temp)

    if channel in [0,1,2,3,4,20,21,22,23,24,30,31,32]:
        for file in filelist_data:
            AddHist_FakePhoton(file, hist_FakePho, 1, 0, 0, channel, branch, year=year)
        for file in filelist_MC:
            AddHist_FakePhoton(filelist_MC[file]["path"], hist_FakePho, 0, filelist_MC[file]["xsec"], lumi, channel, branch, year=year)
    else:
        pass

    file_hist = ROOT.TFile(f'./{year}/{channel_map[channel]}_{year}.root',"RECREATE")
    file_hist.cd()
    for branch_name in branch:
        plot_branch = branch[branch_name]["name"]

        hist_data[plot_branch].SetName(f"{channel_map[channel]}_{plot_branch}_data_{str(UpDown_map[0])}")
        hist_FakeLep[plot_branch].SetName(f"{channel_map[channel]}_{plot_branch}_FakeLep_{str(UpDown_map[0])}")
        hist_FakePho[plot_branch].SetName(f"{channel_map[channel]}_{plot_branch}_FakePho_{str(UpDown_map[0])}")
        hist_data[plot_branch].Write()
        hist_FakeLep[plot_branch].Write()
        hist_FakePho[plot_branch].Write()

        for file in filelist_MC:
            #Nominal + JES JER updown
            for UpDown in range(0,5):
                filelist_MC[file]["hist"][plot_branch+f"_{UpDown_map[UpDown]}"].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{str(UpDown_map[UpDown])}')
                filelist_MC[file]["hist"][plot_branch+f"_{UpDown_map[UpDown]}"].Write()
            #updown
            for unc in unc_map:
                filelist_MC[file]['hist'][f'{plot_branch}_{unc}Up'].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{unc}Up')
                filelist_MC[file]['hist'][f'{plot_branch}_{unc}Up'].Write()
                filelist_MC[file]['hist'][f'{plot_branch}_{unc}Down'].SetName(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{unc}Down')
                filelist_MC[file]['hist'][f'{plot_branch}_{unc}Down'].Write()
    file_hist.Close()

    print (time.time()-time_total_init)

if __name__ == "__main__":
    sys.exit(Prepare_hist(year=args.year, region=args.region))
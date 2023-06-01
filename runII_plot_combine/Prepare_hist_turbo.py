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

parser = argparse.ArgumentParser(description='plot input')
parser.add_argument('-y', dest='year', default='2018', choices=['2016Pre','2016Post','2016','2017','2018'])
parser.add_argument('-r', dest='region', choices=['ttZ','ZZ','ZGJ','WZG','ALP'], default='ttZ')
parser.add_argument('-m', dest='mode', default='prepare')
args = parser.parse_args()

hep.style.use("CMS")

class WZG_plot():
    def __init__(self, year='2018', region='WZG', **kwargs):
        self.year = year
        self.region = region
        sys.path.append(f'./{self.year}/{self.region}')
        import Control_pad as cp
        self.channel_map = cp.channel_map
        self.channel = cp.channel
        self.UpDown_map = cp.UpDown_map
        self.filelist_data = cp.filelist_data
        self.filelist_MC = cp.filelist_MC
        self.branch = cp.branch
        self.lumi = cp.lumi
        self.unc_special_map = {
            'jesTotal':{
                "Nom":None,
                "Up":"jesTotalUp",
                "Down":"jesTotalDown",
                "overlap":0,
                "corr":None
            },
            'jer':{
                "Nom":None,
                "Up":"jerUp",
                "Down":"jerDown",
                "overlap":0,
                "corr":None
            },
        }
        self.unc_map = {
            "Muon_ID_Weight":{
                "Nom":"Muon_ID_Weight",
                "Up":"Muon_ID_Weight_UP",
                "Down":"Muon_ID_Weight_DOWN",
                "overlap":0,
                "corr":1
            },
            "Electron_ID_Weight":{
                "Nom":"Electron_ID_Weight",
                "Up":"Electron_ID_Weight_UP",
                "Down":"Electron_ID_Weight_DOWN",
                "overlap":0,
                "corr":1
            },
            "Electron_RECO_Weight":{
                "Nom":"Electron_RECO_Weight",
                "Up":"Electron_RECO_Weight_UP",
                "Down":"Electron_RECO_Weight_DOWN",
                "overlap":0,
                "corr":1
            },
            "puWeight":{
                "Nom":"puWeight",
                "Up":"puWeightUp",
                "Down":"puWeightDown",
                "overlap":0,
                "corr":1
            },
            "l1pref":{
                "Nom":"L1PreFiringWeight_Nom",
                "Up":"L1PreFiringWeight_Up",
                "Down":"L1PreFiringWeight_Dn",
                "overlap":0,
                "corr":1
            },
            "btagWeight_bc_corr":{
                "Nom":"btagWeight",
                "Up":"btagWeight_bc_up_corr",
                "Down":"btagWeight_bc_down_corr",
                "overlap":0,
                "corr":1
            },
            "btagWeight_l_corr":{
                "Nom":"btagWeight",
                "Up":"btagWeight_l_up_corr",
                "Down":"btagWeight_l_down_corr",
                "overlap":1,
                "corr":1
            },
            "btagWeight_bc_uncorr":{
                "Nom":"btagWeight",
                "Up":"btagWeight_bc_up_uncorr",
                "Down":"btagWeight_bc_down_uncorr",
                "overlap":1,
                "corr":None
            },
            "btagWeight_l_uncorr":{
                "Nom":"btagWeight",
                "Up":"btagWeight_l_up_uncorr",
                "Down":"btagWeight_l_down_uncorr",
                "overlap":1,
                "corr":None
            }
        }
        self.plot_groups = {
            "VV":{
                "names":["qqzz","ggzz_2e2mu","ggzz_2e2nu","ggzz_2e2tau","ggzz_2mu2nu","ggzz_2mu2tau","ggzz_4e","ggzz_4mu","ggzz_4tau","wz"],
                "color":'tab:blue',
                "label":"VV"
            },
            "VG":{  
                "names":["zgtollg","wgtolnug"],
                "color":'tab:green',
                "label":"VG"
            },
            "VVV":{
                "names":["www","wwz","zzz","wzz"],
                "color":'tab:purple',
                "label":"VVV"
            },
            "Top":{
                "names":["ttgjets", "ttztollnunu", "ttztoll", "ttwjetstolnu", "tttt", "tZq_ll", "st antitop", "st top"],
                "color":'tab:orange',
                "label":"Top"
            },
            "WZG":{
                "names":["wzg"],
                "color":'tab:red',
                "label":"WZG"
            },
        }

    def HLT_cut(self, file, arrays, **kwargs):
        if str(self.year) == '2018':
            HLT_SingleMuon = arrays.loc[:,'HLT_IsoMu24'] == True
            HLT_DoubleMuon = arrays.loc[:,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8'] == True
            HLT_EGamma = arrays.loc[:,'HLT_Ele32_WPTight_Gsf'] == True
            HLT_DoubleEG = arrays.loc[:,'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'] == True
            HLT_MuonEG1 = arrays.loc[:,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'] == True
            HLT_MuonEG2 = arrays.loc[:,'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL'] == True
        elif str(self.year) == '2017':
            HLT_SingleMuon = arrays.loc[:,'HLT_IsoMu27'] == True
            HLT_DoubleMuon = arrays.loc[:,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8']
            HLT_SingleElectron = arrays.loc[:,'HLT_Ele32_WPTight_Gsf_L1DoubleEG'] == True
            HLT_DoubleEG = arrays.loc[:,'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'] == True
            HLT_MuonEG1 = arrays.loc[:,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'] == True
            HLT_MuonEG2 = arrays.loc[:,'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'] == True
        elif str(self.year) == '2016Pre':
            HLT_SingleMuon = arrays.loc[:,'HLT_IsoTkMu24'] == True
            HLT_DoubleMuon = arrays.loc[:,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL']
            HLT_SingleElectron = arrays.loc[:,'HLT_Ele27_WPTight_Gsf'] == True
            HLT_DoubleEG = arrays.loc[:,'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'] == True
            HLT_MuonEG1 = arrays.loc[:,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL'] == True
            HLT_MuonEG2 = arrays.loc[:,'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL'] == True
        elif str(self.year) == '2016Post':
            HLT_SingleMuon = arrays.loc[:,'HLT_IsoTkMu24'] == True
            HLT_DoubleMuon = arrays.loc[:,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL']
            HLT_SingleElectron = arrays.loc[:,'HLT_Ele27_WPTight_Gsf'] == True
            HLT_DoubleEG = arrays.loc[:,'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'] == True
            HLT_MuonEG1 = arrays.loc[:,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL'] == True
            HLT_MuonEG2 = arrays.loc[:,'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL'] == True

        if str(self.year) == '2018':
            if 'SingleMuon' in file:
                arrays = arrays.loc[HLT_SingleMuon, :].copy()
            elif 'DoubleMuon' in file:
                arrays = arrays.loc[~HLT_SingleMuon & HLT_DoubleMuon, :].copy()
        #         2018 is special
            elif 'EGamma' in file:
                arrays = arrays.loc[~HLT_SingleMuon & ~HLT_DoubleMuon &   (HLT_EGamma | HLT_DoubleEG) ,:].copy()
            elif 'MuonEG' in file:
                arrays = arrays.loc[~HLT_SingleMuon & ~HLT_DoubleMuon &  ~(HLT_EGamma | HLT_DoubleEG) & (HLT_MuonEG1 | HLT_MuonEG2),:].copy()
            else:
                arrays = arrays.loc[HLT_SingleMuon | HLT_DoubleMuon |  HLT_EGamma | HLT_DoubleEG | HLT_MuonEG1 | HLT_MuonEG2,:].copy() 
        else:
            if 'SingleMuon' in file:
                arrays = arrays.loc[HLT_SingleMuon, :].copy()
            elif 'DoubleMuon' in file:
                arrays = arrays.loc[~HLT_SingleMuon & HLT_DoubleMuon, :].copy()
            elif 'SingleElectron' in file:
                arrays = arrays.loc[~HLT_SingleMuon & ~HLT_DoubleMuon & HLT_SingleElectron, :].copy()
            elif 'DoubleEG' in file:
                arrays = arrays.loc[~HLT_SingleMuon & ~HLT_DoubleMuon & ~HLT_SingleElectron & HLT_DoubleEG, :].copy()
            elif 'MuonEG' in file:
                arrays = arrays.loc[~HLT_SingleMuon & ~HLT_DoubleMuon & ~HLT_SingleElectron & ~HLT_DoubleEG & (HLT_MuonEG1 | HLT_MuonEG2),:].copy()
            else:
                arrays = arrays.loc[HLT_SingleMuon | HLT_DoubleMuon |  HLT_SingleElectron | HLT_DoubleEG | HLT_MuonEG1 | HLT_MuonEG2,:].copy()

        return arrays

    def channel_cut(self, arrays):
        mark = {
            0: (arrays.loc[:,'channel_mark'] >= 1) & (arrays.loc[:,'channel_mark'] <= 4),
            10: (arrays.loc[:,'channel_mark'] >= 11) & (arrays.loc[:,'channel_mark'] <= 14),
            9: (arrays.loc[:,'channel_mark'] >= 5) & (arrays.loc[:,'channel_mark'] <= 8),
            20: (arrays.loc[:,'channel_mark'] >= 21) & (arrays.loc[:,'channel_mark'] <= 24),
            30: (arrays.loc[:,'channel_mark'] >= 31) & (arrays.loc[:,'channel_mark'] <= 32)
        }
        if self.channel in mark.keys():
            arrays = arrays.loc[mark[self.channel], :]
        else:
            cut = arrays.loc[:,'channel_mark'] == self.channel
            arrays = arrays.loc[cut, :]
        
        if self.channel in [0,1,2,3,4]:
            sel = '((channel_mark==2|channel_mark==4) | ((channel_mark==1|channel_mark==3)&(mwa<75|mwa>105))) & WZG_trileptonmass>100 & (WZG_dileptonmass>75&WZG_dileptonmass<105) & WZG_photon_pt>20'

        if self.channel in [10,11,12,13,14]:
            sel = 'ttZ_trileptonmass>100 & (ttZ_dileptonmass<75|ttZ_dileptonmass>105)'

        if self.channel in [5,6,7,8,9]:
            sel = 'ZZ_mllz2>75 & ZZ_mllz2<105 & nbJets==0'

        if self.channel in [30,31,32]:
            # sel = 'ZGJ_dileptonmass>75 & ZGJ_dileptonmass<105 & nbJets>0'
            # sel = '(ZGJ_mlla<75 | ZGJ_mlla>105) & (ZGJ_dileptonmass<75 | ZGJ_dileptonmass>105)'
            # sel = '((ZGJ_mlla + ZGJ_dileptonmass) > 182) & ZGJ_dileptonmass>75 & ZGJ_dileptonmass<105'
            # sel = '(ZGJ_dileptonmass<75 | ZGJ_dileptonmass>105) & ZGJ_photon_pt>20 & nbJets>0'
            sel = 'ZGJ_photon_pt>20 & nbJets>0'
        arrays = arrays.query(sel)

        return arrays

    def lep_gen_cut(self, arrays):
        lep_gen_cut_WZG = ((arrays.loc[:,'WZG_lepton1_genPartFlav'] == 1) | (arrays.loc[:,'WZG_lepton1_genPartFlav'] == 15)) &\
                            ((arrays.loc[:,'WZG_lepton2_genPartFlav'] == 1) | (arrays.loc[:,'WZG_lepton2_genPartFlav'] == 15)) &\
                            ((arrays.loc[:,'WZG_lepton3_genPartFlav'] == 1) | (arrays.loc[:,'WZG_lepton3_genPartFlav'] == 15))
        lep_gen_cut_ttG = ((arrays.loc[:,'ttG_lepton1_genPartFlav'] == 1) | (arrays.loc[:,'ttG_lepton1_genPartFlav'] == 15)) &\
                            ((arrays.loc[:,'ttG_lepton2_genPartFlav'] == 1) | (arrays.loc[:,'ttG_lepton2_genPartFlav'] == 15)) &\
                            ((arrays.loc[:,'ttG_lepton3_genPartFlav'] == 1) | (arrays.loc[:,'ttG_lepton3_genPartFlav'] == 15))
        lep_gen_cut_ZGJ = ((arrays.loc[:,'ZGJ_lepton1_genPartFlav'] == 1) | (arrays.loc[:,'ZGJ_lepton1_genPartFlav'] == 15)) &\
                            ((arrays.loc[:,'ZGJ_lepton2_genPartFlav'] == 1) | (arrays.loc[:,'ZGJ_lepton2_genPartFlav'] == 15)) 
        if self.channel in [10,11,12,13,14,5,6,7,8,9]:
            lep_gen_cut_ttZ = ((arrays.loc[:,'ttZ_lepton1_genPartFlav'] == 1) | (arrays.loc[:,'ttZ_lepton1_genPartFlav'] == 15)) &\
                                ((arrays.loc[:,'ttZ_lepton2_genPartFlav'] == 1) | (arrays.loc[:,'ttZ_lepton2_genPartFlav'] == 15)) &\
                                ((arrays.loc[:,'ttZ_lepton3_genPartFlav'] == 1) | (arrays.loc[:,'ttZ_lepton3_genPartFlav'] == 15))
            lep_gen_cut_ZZ = ((arrays.loc[:,'ZZ_lepton1_genPartFlav'] == 1) | (arrays.loc[:,'ZZ_lepton1_genPartFlav'] == 15)) &\
                                ((arrays.loc[:,'ZZ_lepton2_genPartFlav'] == 1) | (arrays.loc[:,'ZZ_lepton2_genPartFlav'] == 15)) &\
                                ((arrays.loc[:,'ZZ_lepton3_genPartFlav'] == 1) | (arrays.loc[:,'ZZ_lepton3_genPartFlav'] == 15)) &\
                                ((arrays.loc[:,'ZZ_lepton4_genPartFlav'] == 1) | (arrays.loc[:,'ZZ_lepton4_genPartFlav'] == 15))
        else:
            lep_gen_cut_ttZ = None
            lep_gen_cut_ZZ = None

        lep_gen_cut_map = {
                        0:lep_gen_cut_WZG, 
                        1:lep_gen_cut_WZG,
                        2:lep_gen_cut_WZG,
                        3:lep_gen_cut_WZG,
                        4:lep_gen_cut_WZG,
                        10:lep_gen_cut_ttZ,
                        11:lep_gen_cut_ttZ,
                        12:lep_gen_cut_ttZ,
                        13:lep_gen_cut_ttZ,
                        14:lep_gen_cut_ttZ,
                        20:lep_gen_cut_ttG,
                        21:lep_gen_cut_ttG,
                        22:lep_gen_cut_ttG,
                        23:lep_gen_cut_ttG,
                        24:lep_gen_cut_ttG,
                        5:lep_gen_cut_ZZ,
                        6:lep_gen_cut_ZZ,
                        7:lep_gen_cut_ZZ,
                        8:lep_gen_cut_ZZ,
                        9:lep_gen_cut_ZZ,
                        30:lep_gen_cut_ZGJ,
                        31:lep_gen_cut_ZGJ,
                        32:lep_gen_cut_ZGJ
        }
        if self.channel in lep_gen_cut_map:
            return arrays.loc[lep_gen_cut_map[self.channel],:]
        else:
            return arrays

    def pho_gen_cut(self, arrays):
        pho_gen_cut_WZG = (arrays.loc[:,'WZG_photon_genPartFlav'] > 0)
        pho_gen_cut_ttG = (arrays.loc[:,'ttG_photon_genPartFlav'] > 0)
        pho_gen_cut_ZGJ = (arrays.loc[:,'ZGJ_photon_genPartFlav'] == 1)
        pho_gen_cut_map = {
                        0:pho_gen_cut_WZG,
                        1:pho_gen_cut_WZG,
                        2:pho_gen_cut_WZG,
                        3:pho_gen_cut_WZG,
                        4:pho_gen_cut_WZG,
                        20:pho_gen_cut_ttG,
                        21:pho_gen_cut_ttG,
                        22:pho_gen_cut_ttG,
                        23:pho_gen_cut_ttG,
                        24:pho_gen_cut_ttG,
                        30:pho_gen_cut_ZGJ,
                        31:pho_gen_cut_ZGJ,
                        32:pho_gen_cut_ZGJ
        }
        if self.channel in pho_gen_cut_map:
            return arrays.loc[pho_gen_cut_map[self.channel],:]
        else:
            return arrays

    def init_branch(self, init_branches):
        if str(self.year) == '2018':
            init_branches.extend(['channel_mark',\
                            'region_mark',\
                            'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL',\
                            'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',\
                            'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ',\
                            'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8',\
                            'HLT_Ele32_WPTight_Gsf',\
                            'HLT_IsoMu24'])
        elif str(self.year) == '2017':
            init_branches.extend(['channel_mark',\
                            'region_mark',\
                            'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL',\
                            'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',\
                            'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ',\
                            'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8',\
                            'HLT_Ele32_WPTight_Gsf_L1DoubleEG',\
                            'HLT_IsoMu27'])
        elif str(self.year) == '2016Pre':
            init_branches.extend(['channel_mark',\
                            'region_mark',\
                            'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',\
                            'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',\
                            'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL',\
                            'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL',\
                            'HLT_Ele27_WPTight_Gsf',\
                            'HLT_IsoTkMu24'])
        elif str(self.year) == '2016Post':
            init_branches.extend(['channel_mark',\
                            'region_mark',\
                            'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',\
                            'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',\
                            'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL',\
                            'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL',\
                            'HLT_Ele27_WPTight_Gsf',\
                            'HLT_IsoTkMu24'])
        return init_branches

    def AddBranches_MC(self, file, branches, **kwargs):
        search_keys = ['MET_T1Smear*', '*_lepton*genPartFlav', '*_photon*genPartFlav','*ID_Weight*', '*RECO_Weight*', 'L1PreFiringWeight*', 'puWeight*', 'btagWeight*']
        for key in search_keys:
            branches.extend(uproot.open(f'{file}:Events').keys(filter_name=key))
        branches.append('Generator_weight')
        return branches
        
    def AddHist(self, file, hists={}, isData=True, xsec=0, **kwargs):
        time_init = time.time()
        init_branches = []
        init_branches = self.init_branch(init_branches)

        if isData:
            print('is Data')
        else:
            print('is MC')
            init_branches = self.AddBranches_MC(file, init_branches)
            true_events = uproot.open(file)['nEventsGenWeighted'].values()[0]

        print(f'Adding hist for {file}')
        for branch_name in self.branch:
            if self.branch[branch_name]['name'] not in init_branches:
                init_branches.append(self.branch[branch_name]['name'])
        df = uproot.open(f'{file}:Events').arrays(init_branches, library='pd')
        df = self.HLT_cut(file, df)
        df = self.channel_cut(df)
        region_cut = df.loc[:,'region_mark'] == 1
        df = df.loc[region_cut,:]

        if isData:
            if self.channel in [0,1,2,3,4, 10,11,12,13,14]:
                MET_cut = (df.loc[:,'MET'] > 30)
            elif self.channel in [5,6,7,8,9,30,31,32]:
                MET_cut = (df.loc[:,'MET'] <= 30)
            else:
                MET_cut = (df.loc[:,'MET'] >= 0)
            df = df.loc[MET_cut,:]
            for branch_name in self.branch:
                if self.branch[branch_name].__contains__('bin_array'):
                    h_temp = bh.numpy.histogram(df[self.branch[branch_name]['name']], bins=self.branch[branch_name]['bin_array'], density=False, histogram=bh.Histogram, storage=bh.storage.Weight())
                else:
                    xbins = self.branch[branch_name]['xbins']
                    xleft = self.branch[branch_name]['xleft']
                    xright = self.branch[branch_name]['xright']
                    h_temp = bh.numpy.histogram(df[self.branch[branch_name]['name']], bins=xbins, range=(xleft, xright), density=False, histogram=bh.Histogram, storage=bh.storage.Weight())
                if f'{branch_name}' in hists.keys():
                    hists[branch_name] += h_temp
                else:
                    hists[branch_name] = deepcopy(h_temp)
                del h_temp
            print (f'Time Cost for {file.split("/")[len(file.split("/"))-1]}: {time.time()-time_init}s')
            return hists
        
        else:
            df = self.lep_gen_cut(df)
            df = self.pho_gen_cut(df)

            # only for tes
            # for unc in ['btagWeight_bc','btagWeight_l']:
            #     for suffix1 in ['up','down']:
            #         for suffix2 in ['corr','uncorr']:
            #             df[f'{unc}_{suffix1}_{suffix2}'] = df[f'{unc}_{suffix1}_{suffix2}'].apply(lambda x: 1 if x==0 else x)
            #             print(df[f'{unc}_{suffix1}_{suffix2}'])
            df['Generator_weight_sgn'] = df['Generator_weight'].apply(lambda x: 1 if x >= 0 else -1)

            # prepare unc
            df['unc_product'] = 1.0
            unc_nom_list = set([self.unc_map[x]['Nom'] for x in self.unc_map])
            for unc in unc_nom_list:
                df['unc_product'] *= df[f'{unc}']
            df['true_weight'] = df['unc_product'] * self.lumi * xsec * 1000 * df['Generator_weight_sgn'] / true_events

            for unc in self.unc_map:
                unc_else = unc_nom_list - set([self.unc_map[unc]['Nom']])
                df['temp_unc_product'] = 1.0
                for unc_temp in unc_else:
                    df['temp_unc_product'] *= df[f'{unc_temp}']
                df[f'{unc}Up'] = df['temp_unc_product'] * df[self.unc_map[unc]['Up']] * df['Generator_weight_sgn'] * self.lumi * xsec * 1000 / true_events
                df[f'{unc}Down'] = df['temp_unc_product'] * df[self.unc_map[unc]['Down']] * df['Generator_weight_sgn'] * self.lumi * xsec * 1000 / true_events
            
            df_special = deepcopy(df)
            if self.channel in [0,1,2,3,4, 10,11,12,13,14]:
                MET_cut = (df.loc[:,f'MET_T1Smear_pt'] > 30)
                df = df.loc[MET_cut,:].copy()
            elif self.channel in [5,6,7,8,9,30,31,32]:
                MET_cut = (df.loc[:,f'MET_T1Smear_pt'] <= 30)
                df = df.loc[MET_cut,:].copy()
            else:
                df = df.copy()

            # special treatment for jes/jer (MET cut related)
            for unc in self.unc_special_map:
                for suffix in ['Up', 'Down']:
                    if self.channel in [0,1,2,3,4, 10,11,12,13,14]:
                        MET_special_cut = (df_special.loc[:,f'MET_T1Smear_pt_{self.unc_special_map[unc][suffix]}'] > 30)
                    elif self.channel in [5,6,7,8,9,30,31,32]:
                        MET_special_cut = (df_special.loc[:,f'MET_T1Smear_pt_{self.unc_special_map[unc][suffix]}'] <= 30)
                    else:
                        MET_special_cut = None
                    df_special = df_special.loc[MET_special_cut,:].copy()
                    for branch_name in self.branch:
                        if self.branch[branch_name].__contains__('bin_array'):
                            h_temp = bh.numpy.histogram(df_special[self.branch[branch_name]['name']], bins=self.branch[branch_name]['bin_array'], density=False, weights=df_special['true_weight'], histogram=bh.Histogram, storage=bh.storage.Weight())
                        else:
                            xbins = self.branch[branch_name]['xbins']
                            xleft = self.branch[branch_name]['xleft']
                            xright = self.branch[branch_name]['xright']
                            h_temp = bh.numpy.histogram(df_special[self.branch[branch_name]['name']], bins=xbins, range=(xleft, xright), density=False, weights=df_special['true_weight'], histogram=bh.Histogram, storage=bh.storage.Weight())
                        hists[f'{branch_name}_{unc}{suffix}'] = deepcopy(h_temp)
                        del h_temp


            # Fill hist
            for branch_name in self.branch:
                if self.branch[branch_name].__contains__('bin_array'):
                    h_temp = bh.numpy.histogram(df[self.branch[branch_name]['name']], bins=self.branch[branch_name]['bin_array'], density=False, weights=df['true_weight'], histogram=bh.Histogram, storage=bh.storage.Weight())
                    # h_temp_err = bh.numpy.sqrt(np.histogram(df[self.branch[branch_name]['name']], bins=self.branch[branch_name]['bin_array'], density=False, weights=df['true_weight']**2)[0])
                else:
                    xbins = self.branch[branch_name]['xbins']
                    xleft = self.branch[branch_name]['xleft']
                    xright = self.branch[branch_name]['xright']
                    h_temp = bh.numpy.histogram(df[self.branch[branch_name]['name']], bins=xbins, range=(xleft, xright), density=False, weights=df['true_weight'], histogram=bh.Histogram, storage=bh.storage.Weight())
                    # h_temp_err = bh.numpy.sqrt(np.histogram(df[self.branch[branch_name]['name']], bins=xbins, range=(xleft, xright), density=False, weights=df['true_weight']**2)[0])
                hists[branch_name] = deepcopy(h_temp)
                # hists[f'{branch_name}_err'] = deepcopy(h_temp_err)
                del h_temp

                for unc in self.unc_map:
                    if self.branch[branch_name].__contains__('bin_array'):
                        h_temp_up = bh.numpy.histogram(df[self.branch[branch_name]['name']], bins=self.branch[branch_name]['bin_array'], density=False, weights=df[f'{unc}Up'], histogram=bh.Histogram, storage=bh.storage.Weight())
                        h_temp_down = bh.numpy.histogram(df[self.branch[branch_name]['name']], bins=self.branch[branch_name]['bin_array'], density=False, weights=df[f'{unc}Down'], histogram=bh.Histogram, storage=bh.storage.Weight())
                    else:
                        xbins = self.branch[branch_name]['xbins']
                        xleft = self.branch[branch_name]['xleft']
                        xright = self.branch[branch_name]['xright']
                        h_temp_up = bh.numpy.histogram(df[self.branch[branch_name]['name']], bins=xbins, range=(xleft, xright), density=False, weights=df[f'{unc}Up'], histogram=bh.Histogram, storage=bh.storage.Weight())
                        h_temp_down = bh.numpy.histogram(df[self.branch[branch_name]['name']], bins=xbins, range=(xleft, xright), density=False, weights=df[f'{unc}Down'], histogram=bh.Histogram, storage=bh.storage.Weight())
                    hists[f'{branch_name}_{unc}Up'] = deepcopy(h_temp_up)
                    hists[f'{branch_name}_{unc}Down'] = deepcopy(h_temp_down)
                    del h_temp_up
                    del h_temp_down

            print (f'Time Cost for {file.split("/")[len(file.split("/"))-1]}: {time.time()-time_init}s')
            return hists
        pass

    def AddHist_FakeLep(self, file, hists={}, isData=True, xsec=0, **kwargs):
        time_init = time.time()
        init_branches = ['fake_lepton_weight','fake_lepton_weight_up','fake_lepton_weight_down']
        init_branches = self.init_branch(init_branches)

        if isData:
            print('FakeLep Data')
        else:
            print('FakeLep MC')
            init_branches = self.AddBranches_MC(file, init_branches)
            true_events = uproot.open(file)['nEventsGenWeighted'].values()[0]

        print(f'Adding hist for {file}')
        for branch_name in self.branch:
            if self.branch[branch_name]['name'] not in init_branches:
                init_branches.append(self.branch[branch_name]['name'])
        df = uproot.open(f'{file}:Events').arrays(init_branches, library='pd')
        df = self.HLT_cut(file, df)
        df = self.channel_cut(df)
        region_cut = df.loc[:,'region_mark'] == 2
        df = df.loc[region_cut,:]

        if isData:
            if self.channel in [0,1,2,3,4, 10,11,12,13,14]:
                MET_cut = (df.loc[:,'MET'] > 30)
            elif self.channel in [5,6,7,8,9,30,31,32]:
                MET_cut = (df.loc[:,'MET'] <= 30)
            else:
                MET_cut = (df.loc[:,'MET'] >= 0)
            df = df.loc[MET_cut,:]
            for branch_name in self.branch:
                if self.branch[branch_name].__contains__('bin_array'):
                    h_temp = bh.numpy.histogram(df[self.branch[branch_name]['name']], bins=self.branch[branch_name]['bin_array'], density=False, weights=df['fake_lepton_weight'],histogram=bh.Histogram, storage=bh.storage.Weight())
                else:
                    xbins = self.branch[branch_name]['xbins']
                    xleft = self.branch[branch_name]['xleft']
                    xright = self.branch[branch_name]['xright']
                    h_temp = bh.numpy.histogram(df[self.branch[branch_name]['name']], bins=xbins, range=(xleft, xright), density=False, weights=df['fake_lepton_weight'],histogram=bh.Histogram, storage=bh.storage.Weight())
                if f'{branch_name}' in hists.keys():
                    hists[branch_name] += h_temp
                else:
                    hists[branch_name] = deepcopy(h_temp)
                del h_temp
            print (f'Time Cost for {file.split("/")[len(file.split("/"))-1]}: {time.time()-time_init}s')
            return hists
        
        else:
            df = self.lep_gen_cut(df)
            df = self.pho_gen_cut(df)

            df['Generator_weight_sgn'] = df['Generator_weight'].apply(lambda x: 1 if x >= 0 else -1)
            df['unc_product'] = 1.0
            unc_nom_list = set([self.unc_map[x]['Nom'] for x in self.unc_map])
            for unc in unc_nom_list:
                df['unc_product'] *= df[f'{unc}']
            df['true_weight'] = df['unc_product'] * self.lumi * xsec * 1000 * df['Generator_weight_sgn'] * df['fake_lepton_weight']/ true_events

            for branch_name in self.branch:
                if self.branch[branch_name].__contains__('bin_array'):
                    h_temp = bh.numpy.histogram(df[self.branch[branch_name]['name']], bins=self.branch[branch_name]['bin_array'], density=False, weights=-1*df['true_weight'], histogram=bh.Histogram, storage=bh.storage.Weight())
                else:
                    xbins = self.branch[branch_name]['xbins']
                    xleft = self.branch[branch_name]['xleft']
                    xright = self.branch[branch_name]['xright']
                    h_temp = bh.numpy.histogram(df[self.branch[branch_name]['name']], bins=xbins, range=(xleft, xright), density=False, weights=-1*df['true_weight'], histogram=bh.Histogram, storage=bh.storage.Weight())
                if f'{branch_name}' in hists.keys():
                    hists[branch_name] += h_temp
                else:
                    hists[branch_name] = deepcopy(h_temp)
                del h_temp
            print (f'Time Cost for {file.split("/")[len(file.split("/"))-1]}: {time.time()-time_init}s')
            return hists

    def AddHist_FakePho(self, file, hists={}, isData=True, xsec=0, **kwargs):
        time_init = time.time()
        init_branches = ['fake_photon_weight',
                        'WZG_photon_genPartFlav','WZG_photon_pt','WZG_photon_eta','WZG_photon_pfRelIso03_chg','WZG_photon_sieie',\
                        'ttG_photon_genPartFlav','ttG_photon_pt','ttG_photon_eta','ttG_photon_pfRelIso03_chg','ttG_photon_sieie',\
                        'ZGJ_photon_genPartFlav','ZGJ_photon_pt','ZGJ_photon_eta','ZGJ_photon_pfRelIso03_chg','ZGJ_photon_sieie',\
                        ]
        init_branches = self.init_branch(init_branches)

        if isData:
            print('FakePho Data')
        else:
            print('FakePho MC')
            init_branches = self.AddBranches_MC(file, init_branches)
            true_events = uproot.open(file)['nEventsGenWeighted'].values()[0]

        print(f'Adding hist for {file}')
        for branch_name in self.branch:
            if self.branch[branch_name]['name'] not in init_branches:
                init_branches.append(self.branch[branch_name]['name'])
        df = uproot.open(f'{file}:Events').arrays(init_branches, library='pd')
        df = self.HLT_cut(file, df)
        df = self.channel_cut(df)
        region_cut = df.loc[:,'region_mark'] == 3
        df = df.loc[region_cut,:]

        if ((self.channel >= 0) and (self.channel <=4)):
            chg_cut = ((df.loc[:,"WZG_photon_pfRelIso03_chg"]*df.loc[:,"WZG_photon_pt"]) > 4) & ((df.loc[:,"WZG_photon_pfRelIso03_chg"]*df.loc[:,"WZG_photon_pt"]) < 10)
            sieie_sel = '(WZG_photon_sieie>0.01015 & WZG_photon_sieie<0.05030 & WZG_photon_eta<1.4442) | (WZG_photon_sieie>0.0272 & WZG_photon_sieie<0.1360 & WZG_photon_eta>1.566)'
        elif ((self.channel >= 20) and (self.channel <=24)):
            chg_cut = ((df.loc[:,"ttG_photon_pfRelIso03_chg"]*df.loc[:,"ttG_photon_pt"]) > 4) & ((df.loc[:,"ttG_photon_pfRelIso03_chg"]*df.loc[:,"ttG_photon_pt"]) < 10)
            sieie_sel = '(ttG_photon_sieie>0.01015 & ttG_photon_sieie<0.05030 & ttG_photon_eta<1.4442) | (ttG_photon_sieie>0.0272 & ttG_photon_sieie<0.1360 & ttG_photon_eta>1.566)'
        elif ((self.channel >= 30) and (self.channel <=32)):
            chg_cut = ((df.loc[:,"ZGJ_photon_pfRelIso03_chg"]*df.loc[:,"ZGJ_photon_pt"]) > 4) & ((df.loc[:,"ZGJ_photon_pfRelIso03_chg"]*df.loc[:,"ZGJ_photon_pt"]) < 10)
            sieie_sel = '(ZGJ_photon_sieie>0.01015 & ZGJ_photon_sieie<0.05030 & ZGJ_photon_eta<1.4442) | (ZGJ_photon_sieie>0.0272 & ZGJ_photon_sieie<0.1360 & ZGJ_photon_eta>1.566)'
        df = df.query(sieie_sel)
        df = df.loc[chg_cut,:]

        if isData:
            if self.channel in [0,1,2,3,4, 10,11,12,13,14]:
                MET_cut = (df.loc[:,'MET'] > 30)
            elif self.channel in [5,6,7,8,9,30,31,32]:
                MET_cut = (df.loc[:,'MET'] <= 30)
            else:
                MET_cut = (df.loc[:,'MET'] >= 0)
            df = df.loc[MET_cut,:]
            for branch_name in self.branch:
                if self.branch[branch_name].__contains__('bin_array'):
                    h_temp = bh.numpy.histogram(df[self.branch[branch_name]['name']], bins=self.branch[branch_name]['bin_array'], density=False, weights=df['fake_photon_weight'], histogram=bh.Histogram, storage=bh.storage.Weight())
                else:
                    xbins = self.branch[branch_name]['xbins']
                    xleft = self.branch[branch_name]['xleft']
                    xright = self.branch[branch_name]['xright']
                    h_temp = bh.numpy.histogram(df[self.branch[branch_name]['name']], bins=xbins, range=(xleft, xright), density=False, weights=df['fake_photon_weight'], histogram=bh.Histogram, storage=bh.storage.Weight())
                if f'{branch_name}' in hists.keys():
                    hists[branch_name] += h_temp
                else:
                    hists[branch_name] = deepcopy(h_temp)
                del h_temp
            print (f'Time Cost for {file.split("/")[len(file.split("/"))-1]}: {time.time()-time_init}s')
            return hists
        
        else:
            df = self.lep_gen_cut(df)
            df = self.pho_gen_cut(df)

            df['Generator_weight_sgn'] = df['Generator_weight'].apply(lambda x: 1 if x >= 0 else -1)
            df['unc_product'] = 1.0
            unc_nom_list = set([self.unc_map[x]['Nom'] for x in self.unc_map])
            for unc in unc_nom_list:
                df['unc_product'] *= df[f'{unc}']
            df['true_weight'] = df['unc_product'] * self.lumi * xsec * 1000 * df['Generator_weight_sgn'] * df['fake_photon_weight'] / true_events

            for branch_name in self.branch:
                if self.branch[branch_name].__contains__('bin_array'):
                    h_temp = bh.numpy.histogram(df[self.branch[branch_name]['name']], bins=self.branch[branch_name]['bin_array'], density=False, weights=-1*df['true_weight'], histogram=bh.Histogram, storage=bh.storage.Weight())
                else:
                    xbins = self.branch[branch_name]['xbins']
                    xleft = self.branch[branch_name]['xleft']
                    xright = self.branch[branch_name]['xright']
                    h_temp = bh.numpy.histogram(df[self.branch[branch_name]['name']], bins=xbins, range=(xleft, xright), density=False, weights=-1*df['true_weight'], histogram=bh.Histogram, storage=bh.storage.Weight())
                if f'{branch_name}' in hists.keys():
                    hists[branch_name] += h_temp
                else:
                    hists[branch_name] = deepcopy(h_temp)
                del h_temp
            print (f'Time Cost for {file.split("/")[len(file.split("/"))-1]}: {time.time()-time_init}s')
            return hists

    def file_input(self):
        pass

    def hist_store(self, hists_data={}, hists_mc={}, hists_flep={}, hists_fpho={}, **kwargs):
        output = uproot.recreate(f'{self.year}/{self.region}_{self.year}.root')
        for branch_name in self.branch:
            plotbranch = self.branch[branch_name]['name']
            # store data
            output[f'{self.channel_map[self.channel]}_{plotbranch}_data_None'] = hists_data[branch_name]
        
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
            for file in hists_mc:
                for group in self.plot_groups:
                    if hists_mc[file]['name'].lower() in self.plot_groups[group]['names']:
                        self.branch[branch_name]['hists'][group]['Nom'] += hists_mc[file][branch_name]
                        for unc in unc_total:
                            self.branch[branch_name]['hists'][group][f'{unc}Up'] += hists_mc[file][f'{branch_name}_{unc}Up']
                            self.branch[branch_name]['hists'][group][f'{unc}Down'] += hists_mc[file][f'{branch_name}_{unc}Down']
                        continue

            # store mc
            year_suffix_map ={
                '2016Pre':'16',
                '2016Post':'16',
                '2016':'16',
                '2017':'17',
                '2018':'18',
            }
            year_suffix = year_suffix_map[self.year]
            suffix_list = ['Nom']
            for group in self.plot_groups:
                output[f'{self.channel_map[self.channel]}_{plotbranch}_{group}_None'] = self.branch[branch_name]['hists'][group]['Nom']
                for unc in unc_total:
                    if unc_total[unc]['corr'] == 1:
                        output[f'{self.channel_map[self.channel]}_{plotbranch}_{group}_{unc}Up'] = self.branch[branch_name]['hists'][group][f'{unc}Up']
                        output[f'{self.channel_map[self.channel]}_{plotbranch}_{group}_{unc}Down'] = self.branch[branch_name]['hists'][group][f'{unc}Down']
                    else:
                        output[f'{self.channel_map[self.channel]}_{plotbranch}_{group}_{unc}Up_{year_suffix}'] = self.branch[branch_name]['hists'][group][f'{unc}Up']
                        output[f'{self.channel_map[self.channel]}_{plotbranch}_{group}_{unc}Down_{year_suffix}'] = self.branch[branch_name]['hists'][group][f'{unc}Down']

            # store fakelep
            output[f'{self.channel_map[self.channel]}_{plotbranch}_FakeLep_None'] = hists_flep[branch_name]

            if self.channel in [0,1,2,3,4,20,21,22,23,24,30,31,32]:
                # store fakepho
                output[f'{self.channel_map[self.channel]}_{plotbranch}_FakePho_None'] = hists_fpho[branch_name]


    def _make_error_boxes(self, hist=None, facecolor='none', edgecolor='grey', alpha=0.9, hatch='\\\\', linewidth=0.05, **kwargs):
        _x = hist.axes.edges[0][:-1]
        _x_width = hist.axes.widths[0]
        _y = hist.values() - np.sqrt(hist.variances())
        _y_width = 2 * np.sqrt(hist.variances())
        _err_boxes = [mpl.patches.Rectangle((_x_i, _y_i), _x_width_i, _y_width_i) for _x_i, _y_i, _x_width_i, _y_width_i in zip(_x, _y, _x_width, _y_width)]
        _pc = mpl.collections.PatchCollection(_err_boxes, facecolor=facecolor, alpha=alpha, edgecolor=edgecolor, label='Stat Unc.', hatch=hatch, linewidth=0.05 )

        _err_box_proxy = mpl.patches.Patch(facecolor=facecolor, alpha=alpha, hatch=hatch, linewidth=0.05, label='Stat Unc.')
        return _pc, _err_box_proxy
    
    def _make_ratio(self, h1, h2):
        h1_sq = h1.values() * h1.values()
        h2_sq = h2.values() * h2.values()
        array_ratio = np.divide(h1.values(), h2.values(), out=np.zeros_like(h1.values()), where=h2.values()!=0)
        array_ratio_err = np.divide(h1.variances(), h1_sq, out=np.zeros_like(h1_sq), where=h1.values()!=0) + np.divide(h2.variances(), h2_sq, out=np.zeros_like(h2_sq), where=h2.values()!=0)
        array_bin = h1.axes.edges[0]
        # print(h1.variances() * h1.values() * h1.values() + h2.variances() * h2.values() * h2.values()) / (h2.values() * h2.values())
        h_ratio = bh.numpy.histogram([0], bins=array_bin, density=False, weights=1, histogram=bh.Histogram, storage=bh.storage.Weight())
        h_ratio[...] = np.stack([array_ratio, array_ratio_err], axis=-1)
        return h_ratio

    def plot(self, hists_data={}, hists_mcgroup={}, hists_flep={}, hists_fpho={}, flow='none', **kwargs):

        for branch_name in self.branch:
            # create axs
            fig, axs = plt.subplots(
                2, 1,
                sharex = True,
                gridspec_kw = {'height_ratios' : [4,1]},
                figsize = (10, 10)
            )
            fig.subplots_adjust(hspace=0.06)

            # create stack 
            stack_list = []
            color = []
            label = []
            stack_list.append(hists_flep[branch_name])
            hist_pred = deepcopy(hists_flep[branch_name])
            color.append('tab:olive')
            label.append('Fake $\ell$')
            if self.channel in [0,1,2,3,4,20,21,22,23,24,30,31,32]:
                stack_list.append(hists_fpho[branch_name])
                hist_pred += hists_fpho[branch_name]
                color.append('tab:cyan')
                label.append('Fake $\gamma$')
            for group in self.plot_groups:
                stack_list.append(hists_mcgroup[group][branch_name])
                hist_pred += hists_mcgroup[group][branch_name]
                color.append(self.plot_groups[group]['color'])
                label.append(self.plot_groups[group]['label'])
                pass

            # manually add flow instead of using function from mpl for better setup
            if flow.lower() == 'sum':
                pass

            # plot data
            if self.channel not in [0,1,2,3,4]:
                hep.histplot(
                    hists_data[branch_name], 
                    color = 'black',
                    label = 'Data',
                    histtype='errorbar',
                    # xerr = True,
                    yerr = True,
                    binticks = True,
                    ax = axs[0]
                )
            # plot stack
            hep.histplot(
                stack_list,
                stack=True,
                histtype = 'fill',
                color = color,
                label = label,
                binticks = True,
                ax = axs[0]
            )

            # plot errorbar
            pc_pred, pred_err_box_proxy = self._make_error_boxes(ax=axs[0], hist=hist_pred)
            axs[0].add_collection(pc_pred)

            # check position
            # hep.histplot(
            #     hist_pred,
            #     color = 'grey',
            #     label = 'Stat Unc.',
            #     histtype = 'errorbar',
            #     xerr = True,
            #     yerr = True,
            #     binticks = True,
            #     ax = ax,
            #     marker = None,
            #     fillstyle = 'top'
            # )

            # Set y maximum
            _ylim = 0
            if self.channel not in [0,1,2,3,4]:
                _ylim = max(np.array(hist_pred.values()).max(), np.array(hists_data[branch_name].values()).max())
            else:
                _ylim = np.array(hist_pred.values()).max()
            axs[0].set_ylim(0, 2.0*_ylim)
            axs[1].set_ylim(0.5, 1.5)

            # plot ratio
            if self.channel not in [0,1,2,3,4]:
                hist_ratio = self._make_ratio(hists_data[branch_name], hist_pred)
                hep.histplot(
                    hist_ratio, 
                    color = 'black',
                    label = 'Data',
                    histtype='errorbar',
                    # xerr = True,
                    yerr = True,
                    binticks = True,
                    ax = axs[1]
                )
            hist_pred_ratio = self._make_ratio(hist_pred, hist_pred)
            pc_ratio, ratio_err_box_proxy = self._make_error_boxes(ax=axs[1], hist=hist_pred_ratio, hatch=None, facecolor='grey', alpha=0.3)
            axs[1].add_collection(pc_ratio)

            # Add label and set axes style
            handles, labels = axs[0].get_legend_handles_labels()
            handles.append(pred_err_box_proxy)
            labels.append('Stat Unc.')
            axs[0].legend(handles=handles, loc=9, ncol=3, fontsize=20)
            axs[0].grid(axis='both', which='major', linestyle='--', linewidth=1.0, alpha=0.2)
            axs[1].grid(axis='y', which='major', linestyle='--', linewidth=1.0, alpha=0.9)
            axs[0].set_ylabel(f'Events / bin', fontsize=25)
            axs[1].set_xlabel(f'{self.branch[branch_name]["axis_name"]}', fontsize=25)
            axs[1].set_ylabel(f'Data / Pred.', fontsize=25)
            hep.cms.label('Preliminary', data=True, lumi=self.lumi, year=self.year, ax=axs[0])

            fig.savefig(f'{self.year}/{self.region}/{self.region}_{self.branch[branch_name]["name"]}_None_{self.year}.png', dpi=100)
            pass
            del hist_pred
            del pred_err_box_proxy

    def run(self, mode='prepare'):
        hists_data = {}
        hists_mc = {}
        hists_mcgroup = {}
        hists_flep = {}
        hists_fpho = {}
        if mode.lower() == 'prepare':
            for file in self.filelist_data:
                hists_data = self.AddHist(file, hists=hists_data, isData=True)
            for file in self.filelist_MC:
                hists_mc[file] = {}
                hists_mc[file]['name'] = self.filelist_MC[file]['name']
                hists_mc[file] = self.AddHist(self.filelist_MC[file]['path'], hists=hists_mc[file], isData=False, xsec=self.filelist_MC[file]['xsec'])
            for file in self.filelist_data:
                hists_flep = self.AddHist_FakeLep(file, hists=hists_flep, isData=True)
            for file in self.filelist_MC:
                hists_flep = self.AddHist_FakeLep(self.filelist_MC[file]['path'], hists=hists_flep, isData=False, xsec=self.filelist_MC[file]['xsec'])
            if self.channel in [0,1,2,3,4,20,21,22,23,24,30,31,32]:
                for file in self.filelist_data:
                    hists_fpho = self.AddHist_FakeLep(file, hists=hists_fpho, isData=True)
                for file in self.filelist_MC:
                    hists_fpho = self.AddHist_FakeLep(self.filelist_MC[file]['path'], hists=hists_fpho, isData=False, xsec=self.filelist_MC[file]['xsec'])
            self.hist_store(hists_data=hists_data, hists_mc=hists_mc, hists_flep=hists_flep, hists_fpho=hists_fpho)
        else:
            file = uproot.open(f'{self.year}/{self.region}_{self.year}.root')
            for group in self.plot_groups:
                hists_mcgroup[f'{group}'] = {}
            for branch_name in self.branch:
                plotbranch = self.branch[branch_name]['name']
                hists_data[f'{branch_name}'] = file[f'{self.channel_map[self.channel]}_{plotbranch}_data_None'].to_boost()
                hists_flep[f'{branch_name}'] = file[f'{self.channel_map[self.channel]}_{plotbranch}_FakeLep_None'].to_boost()
                if self.channel in [0,1,2,3,4,20,21,22,23,24,30,31,32]:
                    hists_fpho[f'{branch_name}'] = file[f'{self.channel_map[self.channel]}_{plotbranch}_FakePho_None'].to_boost()
                for group in self.plot_groups:
                    hists_mcgroup[f'{group}'][f'{branch_name}'] = file[f'{self.channel_map[self.channel]}_{plotbranch}_{group}_None'].to_boost()

            self.plot(hists_data=hists_data, hists_mcgroup=hists_mcgroup, hists_flep=hists_flep, hists_fpho=hists_fpho)


if __name__ == '__main__':
    time_total_init = time.time()
    p = WZG_plot(year=args.year, region=args.region)
    p.run(args.mode)
    print (f'Total Time Cost: {time.time()-time_total_init}s')
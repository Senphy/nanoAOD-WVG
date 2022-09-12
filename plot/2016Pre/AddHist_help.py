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
import time

def HLT_cut(file, branches):
    HLT_SingleMuon = branches.loc[:,'HLT_IsoTkMu24'] == True
    HLT_DoubleMuon = branches.loc[:,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL']
    HLT_SingleElectron = branches.loc[:,'HLT_Ele27_WPTight_Gsf'] == True
    HLT_DoubleEG = branches.loc[:,'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'] == True
    HLT_MuonEG1 = branches.loc[:,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL'] == True
    HLT_MuonEG2 = branches.loc[:,'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL'] == True
    if 'SingleMuon' in file:
        arrays = branches.loc[HLT_SingleMuon, :].copy()
    elif 'DoubleMuon' in file:
        arrays = branches.loc[~HLT_SingleMuon & HLT_DoubleMuon, :].copy()
    elif 'SingleElectron' in file:
        arrays = branches.loc[~HLT_SingleMuon & ~HLT_DoubleMuon & HLT_SingleElectron, :].copy()
    elif 'DoubleEG' in file:
        arrays = branches.loc[~HLT_SingleMuon & ~HLT_DoubleMuon & ~HLT_SingleElectron & HLT_DoubleEG, :].copy()
    elif 'MuonEG' in file:
        arrays = branches.loc[~HLT_SingleMuon & ~HLT_DoubleMuon & ~HLT_SingleElectron & ~HLT_DoubleEG & (HLT_MuonEG1 | HLT_MuonEG2),:].copy()
    else:
        arrays = branches.loc[HLT_SingleMuon | HLT_DoubleMuon |  HLT_SingleElectron | HLT_DoubleEG | HLT_MuonEG1 | HLT_MuonEG2,:].copy()
    return arrays

def channel_cut(channel, arrays):
    mark = {
        0: (arrays.loc[:,'channel_mark'] >= 1) & (arrays.loc[:,'channel_mark'] <= 4),
        10: (arrays.loc[:,'channel_mark'] >= 11) & (arrays.loc[:,'channel_mark'] <= 14),
        9: (arrays.loc[:,'channel_mark'] >= 5) & (arrays.loc[:,'channel_mark'] <= 8),
        20: (arrays.loc[:,'channel_mark'] >= 21) & (arrays.loc[:,'channel_mark'] <= 24),
        30: (arrays.loc[:,'channel_mark'] >= 31) & (arrays.loc[:,'channel_mark'] <= 32)
    }
    if channel in mark.keys():
        arrays = arrays.loc[mark[channel], :]
    else:
        cut = arrays.loc[:,'channel_mark'] == channel
        arrays = arrays.loc[cut, :]
    
    if channel in [0,1,2,3,4]:
        sel = '(mwa<75|mwa>105) & WZG_trileptonmass>100 & (WZG_dileptonmass>75&WZG_dileptonmass<105)'
        arrays = arrays.query(sel)

    if channel in [10,11,12,13,14]:
        sel = 'ttZ_trileptonmass>100 & (ttZ_dileptonmass<75|ttZ_dileptonmass>105)'
        arrays = arrays.query(sel)

    if channel in [5,6,7,8,9]:
        sel = 'ZZ_mllz2>75 & ZZ_mllz2<105 & nbJets==0'
        arrays = arrays.query(sel)

    if channel in [30,31,32]:
        # sel = 'ZGJ_dileptonmass>75 & ZGJ_dileptonmass<105 & nbJets>0'
        # sel = '(ZGJ_mlla<75 | ZGJ_mlla>105) & (ZGJ_dileptonmass<75 | ZGJ_dileptonmass>105)'
        sel = '((ZGJ_mlla + ZGJ_dileptonmass) > 182) & ZGJ_dileptonmass>75 & ZGJ_dileptonmass<105'
        arrays = arrays.query(sel)
        pass

    return arrays

def lep_gen_cut(channel, arrays):
    lep_gen_cut_WZG = ((arrays.loc[:,'WZG_lepton1_genPartFlav'] == 1) | (arrays.loc[:,'WZG_lepton1_genPartFlav'] == 15)) &\
                        ((arrays.loc[:,'WZG_lepton2_genPartFlav'] == 1) | (arrays.loc[:,'WZG_lepton2_genPartFlav'] == 15)) &\
                        ((arrays.loc[:,'WZG_lepton3_genPartFlav'] == 1) | (arrays.loc[:,'WZG_lepton3_genPartFlav'] == 15))
    lep_gen_cut_ttG = ((arrays.loc[:,'ttG_lepton1_genPartFlav'] == 1) | (arrays.loc[:,'ttG_lepton1_genPartFlav'] == 15)) &\
                        ((arrays.loc[:,'ttG_lepton2_genPartFlav'] == 1) | (arrays.loc[:,'ttG_lepton2_genPartFlav'] == 15)) &\
                        ((arrays.loc[:,'ttG_lepton3_genPartFlav'] == 1) | (arrays.loc[:,'ttG_lepton3_genPartFlav'] == 15))
    lep_gen_cut_ZGJ = ((arrays.loc[:,'ZGJ_lepton1_genPartFlav'] == 1) | (arrays.loc[:,'ZGJ_lepton1_genPartFlav'] == 15)) &\
                        ((arrays.loc[:,'ZGJ_lepton2_genPartFlav'] == 1) | (arrays.loc[:,'ZGJ_lepton2_genPartFlav'] == 15)) 
    if channel in [10,11,12,13,14,5,6,7,8,9]:
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
    if channel in lep_gen_cut_map:
        return arrays.loc[lep_gen_cut_map[channel],:]
    else:
        return arrays

def pho_gen_cut(channel, arrays):
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
    if channel in pho_gen_cut_map:
        return arrays.loc[pho_gen_cut_map[channel],:]
    else:
        return arrays

def AddHist(file, hist, isData, xsec, lumi, channel, branch):
    
    UpDown_map={
        0:None,
        1:"jesTotalUp",
        2:"jesTotalDown",
        3:"jerUp",
        4:"jerDown"
    }

    init_time = time.time()
    init_branches = ['channel_mark',\
                    'region_mark',\
                    'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',\
                    'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',\
                    'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL',\
                    'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL',\
                    'HLT_Ele27_WPTight_Gsf',\
                    'HLT_IsoTkMu24']
    
    if isData:
        print('is Data')
        for branch_name in branch:
            if branch[branch_name]["name"] not in init_branches:
                init_branches.append(branch[branch_name]["name"])
    else:
        print('is MC')
        add_branches = ['Generator_weight']
        met_branches = uproot.open(file+':Events').keys(filter_name='MET_T1Smear*')
        gen_lepton_branches = uproot.open(file+':Events').keys(filter_name='*_lepton*genPartFlav')
        gen_photon_branches= uproot.open(file+':Events').keys(filter_name='*_photon*genPartFlav')
        lepID_weight_branches= uproot.open(file+':Events').keys(filter_name='*ID_Weight*')
        lepRECO_weight_branches= uproot.open(file+':Events').keys(filter_name='*RECO_Weight*')
        # btag_weight_branches= uproot.open(file+':Events').keys(filter_name='*btagWeight*')
        l1_weight_branches = uproot.open(file+':Events').keys(filter_name='L1PreFiringWeight*')
        pu_branches = uproot.open(file+':Events').keys(filter_name='puWeight*')
        true_events = uproot.open(file)['nEventsGenWeighted'].values()[0]
        # btag_weight_ratio = uproot.open(file)['h_nEventsGenWeighted'].values()[0] / uproot.open(file)['h_nEventsGenWeighted_btag'].values()[0]
        init_branches.extend(add_branches)
        init_branches.extend(gen_lepton_branches)
        init_branches.extend(gen_photon_branches)
        init_branches.extend(met_branches)
        init_branches.extend(lepID_weight_branches)
        init_branches.extend(lepRECO_weight_branches)
        # init_branches.extend(btag_weight_branches)
        init_branches.extend(l1_weight_branches)
        init_branches.extend(pu_branches)
        for branch_name in branch:
            if branch[branch_name]["name"] not in init_branches:
                init_branches.append(branch[branch_name]["name"])
        
    branches = uproot.open(file+':Events').arrays(init_branches, library='pd')
    arrays = HLT_cut(file, branches)
    arrays = channel_cut(channel, arrays)
    region_cut = arrays.loc[:,'region_mark'] == 1
    arrays = arrays.loc[region_cut,:]
    
    if isData:
        if channel in [0,1,2,3,4, 10,11,12,13,14]:
            MET_cut = (arrays.loc[:,'MET'] > 30)
        elif channel in [5,6,7,8,9,30,31,32]:
            MET_cut = (arrays.loc[:,'MET'] <= 30)
        else:
            MET_cut = (arrays.loc[:,'MET'] >= 0)
        arrays = arrays.loc[MET_cut,:]
        for branch_name in branch:
            for i in trange(0, len(arrays[branch[branch_name]["name"]]), desc=f'fill {branch[branch_name]["name"]} for {file}'):
                hist[branch_name].Fill(float(arrays[branch[branch_name]["name"]].values[i]))
            print (f"SumOfWeights for {branch_name}: ", hist[branch_name].GetSumOfWeights())

    else:
        arrays = lep_gen_cut(channel, arrays)
        arrays = pho_gen_cut(channel, arrays)

        arrays['Generator_weight_sgn'] = arrays['Generator_weight'].apply(lambda x: 1 if x >= 0 else -1)

        # Temp bugs *FIXME*
        # arrays['Muon_ID_Weight'] = arrays['Muon_ID_Weight'].apply(lambda x: 1 if x==0 else x)
        # arrays['Muon_ID_Weight_UP'] = arrays['Muon_ID_Weight_UP'].apply(lambda x: 1 if x==0 else x)
        # arrays['Muon_ID_Weight_DOWN'] = arrays['Muon_ID_Weight_DOWN'].apply(lambda x: 1 if x==0 else x)
        # arrays['Electron_ID_Weight'] = arrays['Electron_ID_Weight'].apply(lambda x: 1 if x==0 else x)
        # arrays['Electron_ID_Weight_UP'] = arrays['Electron_ID_Weight_UP'].apply(lambda x: 1 if x==0 else x)
        # arrays['Electron_ID_Weight_DOWN'] = arrays['Electron_ID_Weight_DOWN'].apply(lambda x: 1 if x==0 else x)
        # arrays['Electron_RECO_Weight'] = arrays['Electron_RECO_Weight'].apply(lambda x: 1 if x==0 else x)
        # arrays['Electron_RECO_Weight_UP'] = arrays['Electron_RECO_Weight_UP'].apply(lambda x: 1 if x==0 else x)
        # arrays['Electron_RECO_Weight_DOWN'] = arrays['Electron_RECO_Weight_DOWN'].apply(lambda x: 1 if x==0 else x)
        # arrays['btagWeight'] = arrays['btagWeight'].apply(lambda x: 1 if x==0 else x)

        # arrays['true_weight'] = arrays['puWeight'] * arrays['L1PreFiringWeight_Nom'] * btag_weight_ratio * arrays['btagWeight'] * arrays['Muon_ID_Weight'] * arrays['Electron_ID_Weight'] * arrays['Electron_RECO_Weight'] * lumi * xsec * 1000 * arrays['Generator_weight_sgn'] / true_events
        arrays['true_weight'] = arrays['puWeight'] * arrays['L1PreFiringWeight_Nom'] * arrays['Muon_ID_Weight'] * arrays['Electron_ID_Weight'] * arrays['Electron_RECO_Weight'] * lumi * xsec * 1000 * arrays['Generator_weight_sgn'] / true_events
        if channel in [0,1,2,3,4, 10,11,12,13,14]:
            MET_cut = (arrays.loc[:,f'MET_T1Smear_pt'] > 30)
            arrays_copy_nominal = arrays.loc[MET_cut,:].copy()
        elif channel in [5,6,7,8,9,30,31,32]:
            MET_cut = (arrays.loc[:,f'MET_T1Smear_pt'] <= 30)
            arrays_copy_nominal = arrays.loc[MET_cut,:].copy()
        else:
            arrays_copy_nominal = arrays.copy()

        #Fill nominal
        print("Filling nominal:")
        for branch_name in branch:
            for i in trange(0, len(arrays_copy_nominal[branch[branch_name]["name"]]), desc=f'fill {branch[branch_name]["name"]} for {file} in {UpDown_map[0]}'):
                hist[branch_name+f"_{UpDown_map[0]}"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]].values[i]), float(arrays_copy_nominal['true_weight'].values[i]))
        print("\n")
        
        #Fill lep ID RECO up down
        print("Filling up down:")
        arrays_copy_nominal['true_weight_MuonIDup'] = arrays_copy_nominal['puWeight'] * arrays_copy_nominal['L1PreFiringWeight_Nom'] * arrays_copy_nominal['Muon_ID_Weight_UP'] * arrays_copy_nominal['Electron_ID_Weight'] * arrays_copy_nominal['Electron_RECO_Weight'] * lumi * xsec * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
        arrays_copy_nominal['true_weight_MuonIDdown'] = arrays_copy_nominal['puWeight'] * arrays_copy_nominal['L1PreFiringWeight_Nom'] * arrays_copy_nominal['Muon_ID_Weight_DOWN'] * arrays_copy_nominal['Electron_ID_Weight'] * arrays_copy_nominal['Electron_RECO_Weight'] * lumi * xsec * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
        arrays_copy_nominal['true_weight_ElectronIDup'] = arrays_copy_nominal['puWeight'] * arrays_copy_nominal['L1PreFiringWeight_Nom'] * arrays_copy_nominal['Muon_ID_Weight'] * arrays_copy_nominal['Electron_ID_Weight_UP'] * arrays_copy_nominal['Electron_RECO_Weight'] * lumi * xsec * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
        arrays_copy_nominal['true_weight_ElectronIDdown'] = arrays_copy_nominal['puWeight'] * arrays_copy_nominal['L1PreFiringWeight_Nom'] * arrays_copy_nominal['Muon_ID_Weight'] * arrays_copy_nominal['Electron_ID_Weight_DOWN'] * arrays_copy_nominal['Electron_RECO_Weight'] * lumi * xsec * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
        arrays_copy_nominal['true_weight_ElectronRECOup'] = arrays_copy_nominal['puWeight'] * arrays_copy_nominal['L1PreFiringWeight_Nom'] * arrays_copy_nominal['Muon_ID_Weight'] * arrays_copy_nominal['Electron_ID_Weight'] * arrays_copy_nominal['Electron_RECO_Weight_UP'] * lumi * xsec * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
        arrays_copy_nominal['true_weight_ElectronRECOdown'] = arrays_copy_nominal['puWeight'] * arrays_copy_nominal['L1PreFiringWeight_Nom'] * arrays_copy_nominal['Muon_ID_Weight'] * arrays_copy_nominal['Electron_ID_Weight'] * arrays_copy_nominal['Electron_RECO_Weight_DOWN'] * lumi * xsec * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
        arrays_copy_nominal['true_weight_l1up'] = arrays_copy_nominal['puWeight'] * arrays_copy_nominal['L1PreFiringWeight_Up'] * arrays_copy_nominal['Muon_ID_Weight'] * arrays_copy_nominal['Electron_ID_Weight'] * arrays_copy_nominal['Electron_RECO_Weight'] * lumi * xsec * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
        arrays_copy_nominal['true_weight_l1down'] = arrays_copy_nominal['puWeight'] * arrays_copy_nominal['L1PreFiringWeight_Dn'] * arrays_copy_nominal['Muon_ID_Weight'] * arrays_copy_nominal['Electron_ID_Weight'] * arrays_copy_nominal['Electron_RECO_Weight'] * lumi * xsec * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
        arrays_copy_nominal['true_weight_puup'] = arrays_copy_nominal['puWeightUp'] * arrays_copy_nominal['L1PreFiringWeight_Nom'] * arrays_copy_nominal['Muon_ID_Weight'] * arrays_copy_nominal['Electron_ID_Weight'] * arrays_copy_nominal['Electron_RECO_Weight'] * lumi * xsec * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
        arrays_copy_nominal['true_weight_pudown'] = arrays_copy_nominal['puWeightDown'] * arrays_copy_nominal['L1PreFiringWeight_Nom'] * arrays_copy_nominal['Muon_ID_Weight'] * arrays_copy_nominal['Electron_ID_Weight'] * arrays_copy_nominal['Electron_RECO_Weight'] * lumi * xsec * 1000 * arrays_copy_nominal['Generator_weight_sgn'] / true_events
        for branch_name in branch:
            for i in trange(0, len(arrays_copy_nominal[branch[branch_name]["name"]]), desc=f'fill {branch[branch_name]["name"]} for {file} in {UpDown_map[0]}'):
                hist[branch_name+f"_MuonIDup"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]].values[i]), float(arrays_copy_nominal['true_weight_MuonIDup'].values[i]))
                hist[branch_name+f"_MuonIDdown"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]].values[i]), float(arrays_copy_nominal['true_weight_MuonIDdown'].values[i]))
                hist[branch_name+f"_ElectronIDup"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]].values[i]), float(arrays_copy_nominal['true_weight_ElectronIDup'].values[i]))
                hist[branch_name+f"_ElectronIDdown"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]].values[i]), float(arrays_copy_nominal['true_weight_ElectronIDdown'].values[i]))
                hist[branch_name+f"_ElectronRECOup"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]].values[i]), float(arrays_copy_nominal['true_weight_ElectronRECOup'].values[i]))
                hist[branch_name+f"_ElectronRECOdown"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]].values[i]), float(arrays_copy_nominal['true_weight_ElectronRECOdown'].values[i]))
                hist[branch_name+f"_l1up"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]].values[i]), float(arrays_copy_nominal['true_weight_l1up'].values[i]))
                hist[branch_name+f"_l1down"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]].values[i]), float(arrays_copy_nominal['true_weight_l1down'].values[i]))
                hist[branch_name+f"_puup"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]].values[i]), float(arrays_copy_nominal['true_weight_puup'].values[i]))
                hist[branch_name+f"_pudown"].Fill(float(arrays_copy_nominal[branch[branch_name]["name"]].values[i]), float(arrays_copy_nominal['true_weight_pudown'].values[i]))
        print("\n")

        #Fill JES JER up down
        for UpDown in range(1,5):
            print(f"Filling JES {str(UpDown_map[UpDown])}:")
            if channel in [0,1,2,3,4, 10,11,12,13,14]:
                MET_cut = (arrays.loc[:,f'MET_T1Smear_pt_{UpDown_map[UpDown]}'] > 30)
                arrays_copy = arrays.loc[MET_cut,:].copy()
            elif channel in [5,6,7,8,9,30,31,32]:
                MET_cut = (arrays.loc[:,f'MET_T1Smear_pt_{UpDown_map[UpDown]}'] <= 30)
                arrays_copy = arrays.loc[MET_cut,:].copy()
            else:
                arrays_copy = arrays.copy()
        
            for branch_name in branch:
                for i in trange(0, len(arrays_copy[branch[branch_name]["name"]]), desc=f'fill {branch[branch_name]["name"]} for {file} in {UpDown_map[UpDown]}'):
                    hist[branch_name+f"_{UpDown_map[UpDown]}"].Fill(float(arrays_copy[branch[branch_name]["name"]].values[i]), float(arrays_copy['true_weight'].values[i]))
                # print (f"SumOfWeights for {branch_name}: ", hist[branch_name+f"_{UpDown_map[UpDown]}"].GetSumOfWeights())
            print("\n")

    end_time = time.time()
    print ('Time cost: %.2f\n' %(end_time-init_time))
    return True


def AddHist_FakeLepton(file, hist, isData, xsec, lumi, channel, branch):
    
    init_time = time.time()
    init_branches = ['fake_lepton_weight',\
                    'channel_mark',\
                    'region_mark',\
                    'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',\
                    'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',\
                    'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL',\
                    'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL',\
                    'HLT_Ele27_WPTight_Gsf',\
                    'HLT_IsoTkMu24']
    
    if isData:
        print('is Data')
        for branch_name in branch:
            if branch[branch_name]["name"] not in init_branches:
                init_branches.append(branch[branch_name]["name"])
    else:
        print('is MC')
        add_branches = ['Generator_weight']
        gen_branches = uproot.open(file+':Events').keys(filter_name='*_lepton*genPartFlav')
        true_events = uproot.open(file)['nEventsGenWeighted'].values()[0]
        init_branches.extend(add_branches)
        init_branches.extend(gen_branches)
        for branch_name in branch:
            if branch[branch_name]["name"] not in init_branches:
                init_branches.append(branch[branch_name]["name"])
        
    branches = uproot.open(file+':Events').arrays(init_branches, library='pd')
    arrays = HLT_cut(file, branches)
    arrays = channel_cut(channel, arrays)
    region_cut = arrays.loc[:,'region_mark'] == 2
    arrays = arrays.loc[region_cut,:]
    
    if isData:
        if channel in [0,1,2,3,4, 10,11,12,13,14]:
            MET_cut = (arrays.loc[:,'MET'] > 30)
        elif channel in [5,6,7,8,9,30,31,32]:
            MET_cut = (arrays.loc[:,'MET'] <= 30)
        else:
            MET_cut = (arrays.loc[:,'MET'] >= 0)
        arrays = arrays.loc[MET_cut,:]
        for branch_name in branch:
            for i in trange(0, len(arrays[branch[branch_name]["name"]]), desc=f'fill {branch[branch_name]["name"]} for {file}'):
                hist[branch_name].Fill(float(arrays[branch[branch_name]["name"]].values[i]), float(arrays['fake_lepton_weight'].values[i]))
            print (f"SumOfWeights for {branch_name}: ", hist[branch_name].GetSumOfWeights())
    else:
        arrays = lep_gen_cut(channel, arrays)
        if channel in [0,1,2,3,4, 10,11,12,13,14]:
            MET_cut = (arrays.loc[:,'MET'] > 30)
        elif channel in [5,6,7,8,9,30,31,32]:
            MET_cut = (arrays.loc[:,'MET'] <= 30)
        else:
            MET_cut = (arrays.loc[:,'MET'] >= 0)
        arrays = arrays.loc[MET_cut,:]
    
        arrays['Generator_weight_sgn'] = arrays['Generator_weight'].apply(lambda x: 1 if x >= 0 else -1)
        arrays['true_weight'] = lumi * xsec * 1000 * arrays['Generator_weight_sgn'] / true_events
        for branch_name in branch:
            for i in trange(0, len(arrays[branch[branch_name]["name"]]), desc=f'fill {branch[branch_name]["name"]} for {file}'):
                hist[branch_name].Fill(float(arrays[branch[branch_name]["name"]].values[i]), -1 * float(arrays['fake_lepton_weight'].values[i]) * float(arrays['true_weight'].values[i]))
            print (f"SumOfWeights for {branch_name}: ", hist[branch_name].GetSumOfWeights())
    
    end_time = time.time()
    print ('Time cost: %.2f\n' %(end_time-init_time))

def AddHist_FakePhoton(file, hist, isData, xsec, lumi, channel, branch):
    
    init_time = time.time()
    init_branches = ['fake_photon_weight','channel_mark',\
                    'region_mark',\
                    'WZG_photon_genPartFlav','WZG_photon_pt','WZG_photon_eta','WZG_photon_pfRelIso03_chg','WZG_photon_sieie',\
                    'ttG_photon_genPartFlav','ttG_photon_pt','ttG_photon_eta','ttG_photon_pfRelIso03_chg','ttG_photon_sieie',\
                    'ZGJ_photon_genPartFlav','ZGJ_photon_pt','ZGJ_photon_eta','ZGJ_photon_pfRelIso03_chg','ZGJ_photon_sieie',\
                    'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',\
                    'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',\
                    'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL',\
                    'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL',\
                    'HLT_Ele27_WPTight_Gsf',\
                    'HLT_IsoTkMu24']
    
    if isData:
        print('is Data')
        for branch_name in branch:
            if branch[branch_name]["name"] not in init_branches:
                init_branches.append(branch[branch_name]["name"])
    else:
        print('is MC')
        add_branches = ['Generator_weight']
        gen_branches = uproot.open(file+':Events').keys(filter_name='*_lepton*genPartFlav')
        true_events = uproot.open(file)['nEventsGenWeighted'].values()[0]
        init_branches.extend(add_branches)
        init_branches.extend(gen_branches)
        for branch_name in branch:
            if branch[branch_name]["name"] not in init_branches:
                init_branches.append(branch[branch_name]["name"])
        
    branches = uproot.open(file+':Events').arrays(init_branches, library='pd')
    arrays = HLT_cut(file, branches)
    arrays = channel_cut(channel, arrays)
    region_cut = arrays.loc[:,'region_mark'] == 3
    arrays = arrays.loc[region_cut,:]
    
    
    if ((channel >= 0) and (channel <=4)):
        chg_cut = ((arrays.loc[:,"WZG_photon_pfRelIso03_chg"]*arrays.loc[:,"WZG_photon_pt"]) > 4) & ((arrays.loc[:,"WZG_photon_pfRelIso03_chg"]*arrays.loc[:,"WZG_photon_pt"]) < 10)
        sieie_sel = '(WZG_photon_sieie>0.01015 & WZG_photon_sieie<0.05030 & WZG_photon_eta<1.4442) | (WZG_photon_sieie>0.0272 & WZG_photon_sieie<0.1360 & WZG_photon_eta>1.566)'
    elif ((channel >= 20) and (channel <=24)):
        chg_cut = ((arrays.loc[:,"ttG_photon_pfRelIso03_chg"]*arrays.loc[:,"ttG_photon_pt"]) > 4) & ((arrays.loc[:,"ttG_photon_pfRelIso03_chg"]*arrays.loc[:,"ttG_photon_pt"]) < 10)
        sieie_sel = '(ttG_photon_sieie>0.01015 & ttG_photon_sieie<0.05030 & ttG_photon_eta<1.4442) | (ttG_photon_sieie>0.0272 & ttG_photon_sieie<0.1360 & ttG_photon_eta>1.566)'
    elif ((channel >= 30) and (channel <=32)):
        chg_cut = ((arrays.loc[:,"ZGJ_photon_pfRelIso03_chg"]*arrays.loc[:,"ZGJ_photon_pt"]) > 4) & ((arrays.loc[:,"ZGJ_photon_pfRelIso03_chg"]*arrays.loc[:,"ZGJ_photon_pt"]) < 10)
        sieie_sel = '(ZGJ_photon_sieie>0.01015 & ZGJ_photon_sieie<0.05030 & ZGJ_photon_eta<1.4442) | (ZGJ_photon_sieie>0.0272 & ZGJ_photon_sieie<0.1360 & ZGJ_photon_eta>1.566)'
    arrays = arrays.query(sieie_sel)

    if isData:
        arrays = arrays.loc[chg_cut,:]
        if channel in [0,1,2,3,4, 10,11,12,13,14]:
            MET_cut = (arrays.loc[:,'MET'] > 30)
        elif channel in [5,6,7,8,9,30,31,32]:
            MET_cut = (arrays.loc[:,'MET'] <= 30)
        else:
            MET_cut = (arrays.loc[:,'MET'] >= 0)
        arrays = arrays.loc[chg_cut & MET_cut,:]

        for branch_name in branch:
            for i in trange(0, len(arrays[branch[branch_name]["name"]]), desc=f'fill {branch[branch_name]["name"]} for {file}'):
                hist[branch_name].Fill(float(arrays[branch[branch_name]["name"]].values[i]), float(arrays['fake_photon_weight'].values[i]))
            print (f"SumOfWeights for {branch_name}: ", hist[branch_name].GetSumOfWeights())

    else:
        arrays = lep_gen_cut(channel, arrays)
        arrays = pho_gen_cut(channel, arrays)
        if channel in [0,1,2,3,4, 10,11,12,13,14]:
            MET_cut = (arrays.loc[:,'MET'] > 30)
        elif channel in [5,6,7,8,9,30,31,32]:
            MET_cut = (arrays.loc[:,'MET'] <= 30)
        else:
            MET_cut = (arrays.loc[:,'MET'] >= 0)
        arrays = arrays.loc[chg_cut & MET_cut,:]
    
        arrays['Generator_weight_sgn'] = arrays['Generator_weight'].apply(lambda x: 1 if x >= 0 else -1)
        arrays['true_weight'] = lumi * xsec * 1000 * arrays['Generator_weight_sgn'] / true_events
        for branch_name in branch:
            for i in trange(0, len(arrays[branch[branch_name]["name"]]), desc=f'fill {branch[branch_name]["name"]} for {file}'):
                hist[branch_name].Fill(float(arrays[branch[branch_name]["name"]].values[i]), -1 * float(arrays['fake_photon_weight'].values[i]) * float(arrays['true_weight'].values[i]))
            print (f"SumOfWeights for {branch_name}: ", hist[branch_name].GetSumOfWeights())
    
    end_time = time.time()
    print ('Time cost: %.2f\n' %(end_time-init_time))

def SetHistStyle(hist, color):
    if color != 1:
        hist.SetFillColor(color)
        hist.SetLineColor(0)
        hist.SetLineWidth(0)
    else:
        hist.SetLineWidth(2)
        hist.SetLineColor(1)
    hist.SetMarkerStyle(20)
    hist.SetMarkerColor(1)
    hist.SetYTitle('events/bin')
    hist.SetStats(0)
    # hist.Sumw2()

    # Adjust y-axis settings
    # hist.GetYaxis().SetNdivisions(105)
    hist.GetYaxis().SetTitleSize(45)
    hist.GetYaxis().SetTitleFont(43)
    hist.GetYaxis().SetTitleOffset(1.65)
    hist.GetYaxis().SetLabelFont(43)
    hist.GetYaxis().SetLabelSize(38)
    hist.GetYaxis().SetLabelOffset(0.015)

    # Adjust x-axis settings
    hist.GetXaxis().SetTitleSize(45)
    hist.GetXaxis().SetTitleFont(43)
    hist.GetXaxis().SetTitleOffset(3.3)
    hist.GetXaxis().SetLabelFont(43)
    hist.GetXaxis().SetLabelSize(38)
    hist.GetXaxis().SetLabelOffset(0.015)

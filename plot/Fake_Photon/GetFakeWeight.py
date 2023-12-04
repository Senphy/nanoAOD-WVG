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
import argparse

parser = argparse.ArgumentParser(description='photon fake weight')
parser.add_argument('-y', dest='year', default='2018', choices=['2016','2017','2018'])
parser.add_argument('-b', dest='isbarrel', default=False, action='store_true')
args = parser.parse_args()

# CMS_lumi
#   Initiated by: Gautier Hamel de Monchenault (Saclay)
#   Translated in Python by: Joshua Hardenbrook (Princeton)
#   Updated by:   Dinko Ferencek (Rutgers)
#

cmsText     = "CMS"
cmsTextFont   = 62  

writeExtraText = True
extraText   = "Preliminary"
extraTextFont = 52 

lumiTextSize     = 0.45
lumiTextOffset   = 0.2

cmsTextSize      = 0.55
cmsTextOffset    = 0.1

relPosX    = 0.045
relPosY    = 0.035
relExtraDY = 1.2

extraOverCmsTextSize  = 0.76

lumi_13TeV = "20.1 fb^{-1}"
lumi_8TeV  = "19.7 fb^{-1}" 
lumi_7TeV  = "5.1 fb^{-1}"
lumi_sqrtS = "59.7 fb^{-1} (13 TeV)"

drawLogo      = False

def CMS_lumi(pad,  iPeriod,  iPosX ):
    outOfFrame    = False
    if(iPosX/10==0 ): outOfFrame = True

    alignY_=3
    alignX_=2
    if( iPosX/10==0 ): alignX_=1
    if( iPosX==0    ): alignY_=1
    if( iPosX/10==1 ): alignX_=1
    if( iPosX/10==2 ): alignX_=2
    if( iPosX/10==3 ): alignX_=3
    align_ = 10*alignX_ + alignY_

    H = pad.GetWh()
    W = pad.GetWw()
    l = pad.GetLeftMargin()
    t = pad.GetTopMargin()
    r = pad.GetRightMargin()
    b = pad.GetBottomMargin()
    e = 0.025

    pad.cd()

    lumiText = ""
    if( iPeriod==1 ):
        lumiText += lumi_7TeV
        lumiText += " (7 TeV)"
    elif ( iPeriod==2 ):
        lumiText += lumi_8TeV
        lumiText += " (8 TeV)"

    elif( iPeriod==3 ):      
        lumiText = lumi_8TeV 
        lumiText += " (8 TeV)"
        lumiText += " + "
        lumiText += lumi_7TeV
        lumiText += " (7 TeV)"
    elif ( iPeriod==4 ):
        lumiText += lumi_13TeV
        lumiText += " (13 TeV)"
    elif ( iPeriod==7 ):
        if( outOfFrame ):lumiText += "#scale[0.85]{"
        lumiText += lumi_13TeV 
        lumiText += " (13 TeV)"
        lumiText += " + "
        lumiText += lumi_8TeV 
        lumiText += " (8 TeV)"
        lumiText += " + "
        lumiText += lumi_7TeV
        lumiText += " (7 TeV)"
        if( outOfFrame): lumiText += "}"
    elif ( iPeriod==12 ):
        lumiText += "8 TeV"
    elif ( iPeriod==0 ):
        lumiText += lumi_sqrtS
            
    print (lumiText)

    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(ROOT.kBlack)    
    
    extraTextSize = extraOverCmsTextSize*cmsTextSize
    
    latex.SetTextFont(42)
    latex.SetTextAlign(31) 
    latex.SetTextSize(lumiTextSize*t)    

    latex.DrawLatex(1-r,1-t+lumiTextOffset*t,lumiText)

    if( outOfFrame ):
        latex.SetTextFont(cmsTextFont)
        latex.SetTextAlign(11) 
        latex.SetTextSize(cmsTextSize*t)    
        latex.DrawLatex(l,1-t+lumiTextOffset*t,cmsText)
  
    pad.cd()

    posX_ = 0
    if( iPosX%10<=1 ):
        posX_ =   l + relPosX*(1-l-r)
    elif( iPosX%10==2 ):
        posX_ =  l + 0.5*(1-l-r)
    elif( iPosX%10==3 ):
        posX_ =  1-r - relPosX*(1-l-r)

    posY_ = 1-t - relPosY*(1-t-b)

    if( not outOfFrame ):
        if( drawLogo ):
            posX_ =   l + 0.045*(1-l-r)*W/H
            posY_ = 1-t - 0.045*(1-t-b)
            xl_0 = posX_
            yl_0 = posY_ - 0.15
            xl_1 = posX_ + 0.15*H/W
            yl_1 = posY_
            CMS_logo = ROOT.TASImage("CMS-BW-label.png")
            pad_logo =  ROOT.TPad("logo","logo", xl_0, yl_0, xl_1, yl_1 )
            pad_logo.Draw()
            pad_logo.cd()
            CMS_logo.Draw("X")
            pad_logo.Modified()
            pad.cd()          
        else:
            latex.SetTextFont(cmsTextFont)
            latex.SetTextSize(cmsTextSize*t)
            latex.SetTextAlign(align_)
            latex.DrawLatex(posX_, posY_, cmsText)
            if( writeExtraText ) :
                latex.SetTextFont(extraTextFont)
                latex.SetTextAlign(align_)
                latex.SetTextSize(extraTextSize*t)
                latex.DrawLatex(posX_, posY_- relExtraDY*cmsTextSize*t, extraText)
    elif( writeExtraText ):
        if( iPosX==0):
            posX_ =   l +  relPosX*(1-l-r)
            posY_ =   1-t+lumiTextOffset*t

        latex.SetTextFont(extraTextFont)
        latex.SetTextSize(extraTextSize*t)
        latex.SetTextAlign(align_)
        latex.DrawLatex(posX_+0.1, posY_, extraText)      

    pad.Update()

from ROOT import TCanvas, TColor, TGaxis, TH1F, TPad
from ROOT import kBlack, kBlue, kRed

def createRatio(h1, h2):
    h3 = h1.Clone("h3")
    h3.SetLineColor(kBlack)
    h3.SetMarkerStyle(21)
    h3.SetTitle("")
    h3.SetMinimum(0.80)
    h3.SetMaximum(1.53)
    # Set up plot for markers and errors
    h3.Sumw2()
    h3.SetStats(0)
    h3.Divide(h2)

    # Adjust y-axis settings
    y = h3.GetYaxis()
    y.SetTitle("Data / MC ")
    y.SetNdivisions(105)
    y.SetTitleSize(20)
    y.SetTitleFont(43)
    y.SetTitleOffset(1.55)
    y.SetLabelFont(43)
    y.SetLabelSize(20)

    # Adjust x-axis settings
    x = h3.GetXaxis()
    x.SetTitleSize(20)
    x.SetTitleFont(43)
    x.SetTitleOffset(4.0)
    x.SetLabelFont(43)
    x.SetLabelSize(20)

    return h3

def HLT_cut(year, arrays, **kwargs):
    if str(year) == '2018':
        HLT_SingleMuon = arrays.loc[:,'HLT_IsoMu24'] == True
        HLT_DoubleMuon = arrays.loc[:,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8'] == True
        HLT_EGamma = arrays.loc[:,'HLT_Ele32_WPTight_Gsf'] == True
        HLT_DoubleEG = arrays.loc[:,'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'] == True
        HLT_MuonEG1 = arrays.loc[:,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'] == True
        HLT_MuonEG2 = arrays.loc[:,'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL'] == True
    elif str(year) == '2017':
        HLT_SingleMuon = arrays.loc[:,'HLT_IsoMu27'] == True
        HLT_DoubleMuon = arrays.loc[:,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8']
        HLT_SingleElectron = arrays.loc[:,'HLT_Ele32_WPTight_Gsf_L1DoubleEG'] == True
        HLT_DoubleEG = arrays.loc[:,'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'] == True
        HLT_MuonEG1 = arrays.loc[:,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'] == True
        HLT_MuonEG2 = arrays.loc[:,'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'] == True
    elif str(year) == '2016Pre':
        HLT_SingleMuon = arrays.loc[:,'HLT_IsoTkMu24'] == True
        HLT_DoubleMuon = arrays.loc[:,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL']
        HLT_SingleElectron = arrays.loc[:,'HLT_Ele27_WPTight_Gsf'] == True
        HLT_DoubleEG = arrays.loc[:,'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'] == True
        HLT_MuonEG1 = arrays.loc[:,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL'] == True
        HLT_MuonEG2 = arrays.loc[:,'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL'] == True
    elif str(year) == '2016Post':
        HLT_SingleMuon = arrays.loc[:,'HLT_IsoTkMu24'] == True
        HLT_DoubleMuon = arrays.loc[:,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL']
        HLT_SingleElectron = arrays.loc[:,'HLT_Ele27_WPTight_Gsf'] == True
        HLT_DoubleEG = arrays.loc[:,'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'] == True
        HLT_MuonEG1 = arrays.loc[:,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL'] == True
        HLT_MuonEG2 = arrays.loc[:,'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL'] == True

    if str(year) == '2018':
        if 'DoubleMuon' in file:
            arrays = arrays.loc[HLT_DoubleMuon, :].copy()
    #         2018 is special
        elif 'EGamma' in file:
            arrays = arrays.loc[~HLT_DoubleMuon & (HLT_EGamma | HLT_DoubleEG) ,:].copy()
        else:
            arrays = arrays.loc[HLT_SingleMuon | HLT_DoubleMuon |  HLT_EGamma | HLT_DoubleEG | HLT_MuonEG1 | HLT_MuonEG2,:].copy() 
    else:
        if 'DoubleMuon' in file:
            arrays = arrays.loc[HLT_DoubleMuon, :].copy()
        elif 'DoubleEG' in file:
            arrays = arrays.loc[~HLT_DoubleMuon & HLT_DoubleEG, :].copy()
        else:
            arrays = arrays.loc[HLT_SingleMuon | HLT_DoubleMuon |  HLT_SingleElectron | HLT_DoubleEG | HLT_MuonEG1 | HLT_MuonEG2,:].copy()

    return arrays

def AddBranches(file, year, branches, **kwargs):
    search_keys = ['photon_sieie', 'photon_vidNestedWPBitmap', 'photon_eta', 'photon_pt', 'photon_pfRelIso03_chg']
    for key in search_keys:
        branches.extend(uproot.open(f'{file}:Events').keys(filter_name=key))
    # branches.append('Generator_weight')
    if str(year) == '2018':
        branches.extend(['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL',\
                        'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',\
                        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ',\
                        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8',\
                        'HLT_Ele32_WPTight_Gsf',\
                        'HLT_IsoMu24'])
    elif str(year) == '2017':
        branches.extend(['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL',\
                        'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',\
                        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ',\
                        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8',\
                        'HLT_Ele32_WPTight_Gsf_L1DoubleEG',\
                        'HLT_IsoMu27'])
    elif str(year) == '2016Pre':
        branches.extend(['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',\
                        'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',\
                        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL',\
                        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL',\
                        'HLT_Ele27_WPTight_Gsf',\
                        'HLT_IsoTkMu24'])
    elif str(year) == '2016Post':
        branches.extend(['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',\
                        'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',\
                        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL',\
                        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL',\
                        'HLT_Ele27_WPTight_Gsf',\
                        'HLT_IsoTkMu24'])
    return branches

def AddHist_data(file, hist, ptrange, isbarrel, year='2018', **kwargs):
    init_branches = []
    init_branches = AddBranches(file, year, init_branches)
    df = uproot.open(f'{file}:Events').arrays(init_branches, library='pd')
    df = HLT_cut(year, df)

    if isbarrel == 1:
        eta_cut = abs(df.loc[:,'photon_eta']) < 1.4442
#         chg_cut = (df.loc[:,'photon_pfRelIso03_chg']*df.loc[:,'photon_pt']) < 1.141
    elif isbarrel == 0:
        eta_cut = abs((df.loc[:,'photon_eta']) > 1.566) & abs((df.loc[:,'photon_eta']) < 2.5)
#         chg_cut = (df.loc[:,'photon_pfRelIso03_chg']*df.loc[:,'photon_pt']) < 1.051
        
    mask_mediumID = (1<<1) | (1<<3) | (1<<5) | (1<<7) |(1<<9) | (1<<11) | (1<<13)
    df['mediumID'] = df['photon_vidNestedWPBitmap'] & mask_mediumID
    df = df.loc[df.loc[:,'mediumID'] == mask_mediumID, :]
    
    pt_cut = (df.loc[:,'photon_pt'] >= ptrange[0]) & (df.loc[:,'photon_pt'] < ptrange[1]) 
    df = df.loc[pt_cut & eta_cut,:]
    
    for i in trange(0, len(df['photon_pt']), desc=f'fill pt for {file}'):
        hist.Fill(float(df['photon_pt'].values[i]))
    
    
def AddHist_mcTruth(file, hist, ptrange, isbarrel, xsec, lumi, year='2018', **kwargs):
    init_branches = []
    init_branches = AddBranches(file, year, init_branches)
    init_branches.extend(['Generator_weight','photon_genPartFlav'])
    true_events = uproot.open(file)['nEventsGenWeighted'].values()[0]
    df = uproot.open(f'{file}:Events').arrays(init_branches, library='pd')
    df = HLT_cut(year, df)
    
    mask_mediumID = (1<<1) | (1<<3) | (1<<5) | (1<<7) | (1<<9) | (1<<11) | (1<<13)
    df['mediumID'] = df['photon_vidNestedWPBitmap'] & mask_mediumID

    mask_invert_IsoChg = (1<<1) | (1<<3) | (1<<5) | (1<<7) | (1<<11) | (1<<13)
    mask_invert_sieie  = (1<<1) | (1<<3) | (1<<5) | (1<<9)  | (1<<11) | (1<<13)
    mask_invert_neuiso = (1<<1) | (1<<3) | (1<<5) | (1<<7)  | (1<<9) | (1<<13)
    mask_invert_phoiso = (1<<1) | (1<<3) | (1<<5) | (1<<7)  | (1<<9) | (1<<11)
    cut_fail_IsoChg = (df.loc[:,'mediumID'] == mask_invert_IsoChg)
    cut_fail_Sieie  = (df.loc[:,'mediumID'] == mask_invert_sieie)
    cut_fail_neuiso = (df.loc[:,'mediumID'] == mask_invert_neuiso)
    cut_fail_phoiso = (df.loc[:,'mediumID'] == mask_invert_phoiso)
    cut_fail_medium = (cut_fail_IsoChg | cut_fail_Sieie | cut_fail_neuiso | cut_fail_phoiso)
    
    df = df.loc[cut_fail_medium, :]
    
    if isbarrel == 1:
        eta_cut = abs(df.loc[:,'photon_eta']) < 1.4442
    elif isbarrel == 0:
        eta_cut = abs((df.loc[:,'photon_eta']) > 1.566) & abs((df.loc[:,'photon_eta']) < 2.5)
    pt_cut = (df.loc[:,'photon_pt'] >= ptrange[0]) & (df.loc[:,'photon_pt'] < ptrange[1]) 
    gen_cut = df.loc[:,'photon_genPartFlav'] == 1
    df = df.loc[pt_cut & eta_cut & gen_cut,:]
    
    df['Generator_weight_sgn'] = df['Generator_weight'].apply(lambda x: 1 if x >= 0 else -1)
    df['true_weight'] = -1 * lumi * xsec * 1000 * df['Generator_weight_sgn'] / true_events
    
    for i in trange(0, len(df['photon_pt']), desc=f'fill pt for {file}'):
        hist.Fill(float(df['photon_pt'].values[i]), float(df['true_weight'].values[i]))
    
def AddHist_dataFake(file, hist, ptrange, isbarrel, year='2018', **kwargs):
    init_branches = []
    init_branches = AddBranches(file, year, init_branches)
    df = uproot.open(f'{file}:Events').arrays(init_branches, library='pd')
    df = HLT_cut(year, df)

    mask_mediumID = (1<<1) | (1<<3) | (1<<5) | (1<<7) | (1<<9) | (1<<11) | (1<<13)
    df['mediumID'] = df['photon_vidNestedWPBitmap'] & mask_mediumID

    mask_invert_IsoChg = (1<<1) | (1<<3) | (1<<5) | (1<<7) | (1<<11) | (1<<13)
    mask_invert_sieie  = (1<<1) | (1<<3) | (1<<5) | (1<<9)  | (1<<11) | (1<<13)
    mask_invert_neuiso = (1<<1) | (1<<3) | (1<<5) | (1<<7)  | (1<<9) | (1<<13)
    mask_invert_phoiso = (1<<1) | (1<<3) | (1<<5) | (1<<7)  | (1<<9) | (1<<11)
    cut_fail_IsoChg = (df.loc[:,'mediumID'] == mask_invert_IsoChg)
    cut_fail_Sieie  = (df.loc[:,'mediumID'] == mask_invert_sieie)
    cut_fail_neuiso = (df.loc[:,'mediumID'] == mask_invert_neuiso)
    cut_fail_phoiso = (df.loc[:,'mediumID'] == mask_invert_phoiso)
    cut_fail_medium = (cut_fail_IsoChg | cut_fail_Sieie | cut_fail_neuiso | cut_fail_phoiso)

    # case II cut fail one of medium cut
    #cut_fail_medium = (df.loc[:,'mediumID'] != mask_mediumID)

    df = df.loc[cut_fail_medium, :]
    if isbarrel == 1:
        eta_cut = abs(df.loc[:,'photon_eta']) < 1.4442
    elif isbarrel == 0:
        eta_cut = abs((df.loc[:,'photon_eta']) > 1.566) & abs((df.loc[:,'photon_eta']) < 2.5)
        
#     chg_cut = ((df.loc[:,"photon_pfRelIso03_chg"]*df.loc[:,"photon_pt"]) > 4) & ((df.loc[:,"photon_pfRelIso03_chg"]*df.loc[:,"photon_pt"]) < 10)
    pt_cut = (df.loc[:,'photon_pt'] >= ptrange[0]) & (df.loc[:,'photon_pt'] < ptrange[1]) 
    df = df.loc[pt_cut & eta_cut,:]
    
    for i in trange(0, len(df['photon_pt']), desc=f'fill pt for {file}'):
        hist.Fill(float(df['photon_pt'].values[i]))
        
@numba.njit
def sgn(num):
    if (num >= 0):
        return 1
    else:
        return -1

if __name__ == '__main__':
    tdrStyle =  ROOT.TStyle("","")

    #for the canvas:
    tdrStyle.SetCanvasBorderMode(0)
    tdrStyle.SetCanvasColor(ROOT.kWhite)
    tdrStyle.SetCanvasDefH(1000) #Height of canvas
    tdrStyle.SetCanvasDefW(800) #Width of canvas
    tdrStyle.SetCanvasDefX(0)   #POsition on screen
    tdrStyle.SetCanvasDefY(0)


    tdrStyle.SetPadBorderMode(0)
    #tdrStyle.SetPadBorderSize(Width_t size = 1)
    tdrStyle.SetPadColor(ROOT.kWhite)
    tdrStyle.SetPadGridX(False)
    tdrStyle.SetPadGridY(False)
    tdrStyle.SetGridColor(0)
    tdrStyle.SetGridStyle(3)
    tdrStyle.SetGridWidth(1)

    #For the frame:
    tdrStyle.SetFrameBorderMode(1)
    tdrStyle.SetFrameBorderSize(1)
    tdrStyle.SetFrameFillColor(0)
    tdrStyle.SetFrameFillStyle(0)
    tdrStyle.SetFrameLineColor(1)
    tdrStyle.SetFrameLineStyle(1)
    tdrStyle.SetFrameLineWidth(1)

    #For the histo:
    #tdrStyle.SetHistFillColor(1)
    #tdrStyle.SetHistFillStyle(0)
    tdrStyle.SetHistLineColor(1)
    tdrStyle.SetHistLineStyle(0)
    tdrStyle.SetHistLineWidth(1)
    #tdrStyle.SetLegoInnerR(Float_t rad = 0.5)
    #tdrStyle.SetNumberContours(Int_t number = 20)

    tdrStyle.SetEndErrorSize(2)
    #tdrStyle.SetErrorMarker(20)
    #tdrStyle.SetErrorX(0.)

    tdrStyle.SetMarkerStyle(20)

    #For the fit/function:
    tdrStyle.SetOptFit(1)
    tdrStyle.SetFitFormat("5.4g")
    tdrStyle.SetFuncColor(2)
    tdrStyle.SetFuncStyle(1)
    tdrStyle.SetFuncWidth(1)

    #For the date:
    tdrStyle.SetOptDate(0)
    # tdrStyle.SetDateX(Float_t x = 0.01)
    # tdrStyle.SetDateY(Float_t y = 0.01)

    # For the statistics box:
    tdrStyle.SetOptFile(0)
    tdrStyle.SetOptStat(0) # To display the mean and RMS:   SetOptStat("mr")
    tdrStyle.SetStatColor(ROOT.kWhite)
    tdrStyle.SetStatFont(42)
    tdrStyle.SetStatFontSize(0.025)
    tdrStyle.SetStatTextColor(1)
    tdrStyle.SetStatFormat("6.4g")
    tdrStyle.SetStatBorderSize(1)
    tdrStyle.SetStatH(0.1)
    tdrStyle.SetStatW(0.15)
    # tdrStyle.SetStatStyle(Style_t style = 1001)
    # tdrStyle.SetStatX(Float_t x = 0)
    # tdrStyle.SetStatY(Float_t y = 0)

    # Margins:
    tdrStyle.SetPadTopMargin(0.10)
    tdrStyle.SetPadBottomMargin(0.10)
    tdrStyle.SetPadLeftMargin(0.10)
    tdrStyle.SetPadRightMargin(0.10)

    # For the Global title:

    tdrStyle.SetOptTitle(0)
    tdrStyle.SetTitleFont(42)
    tdrStyle.SetTitleColor(1)
    tdrStyle.SetTitleTextColor(1)
    tdrStyle.SetTitleFillColor(10)
    tdrStyle.SetTitleFontSize(0.05)
    # tdrStyle.SetTitleH(0) # Set the height of the title box
    # tdrStyle.SetTitleW(0) # Set the width of the title box
    # tdrStyle.SetTitleX(0) # Set the position of the title box
    # tdrStyle.SetTitleY(0.985) # Set the position of the title box
    # tdrStyle.SetTitleStyle(Style_t style = 1001)
    # tdrStyle.SetTitleBorderSize(2)

    # For the axis titles:

    tdrStyle.SetTitleColor(1, "XYZ")
    tdrStyle.SetTitleFont(42, "XYZ")
    tdrStyle.SetTitleSize(0.04, "XYZ")
    #   tdrStyle.SetTitleXSize(Float_t size = 0.02) # Another way to set the size?
    #   tdrStyle.SetTitleYSize(Float_t size = 0.02)
    tdrStyle.SetTitleXOffset(0.9)
    tdrStyle.SetTitleYOffset(1.25)
    # tdrStyle.SetTitleOffset(1.1, "Y") # Another way to set the Offset

    # For the axis labels:

    tdrStyle.SetLabelColor(1, "XYZ")
    tdrStyle.SetLabelFont(42, "XYZ")
    tdrStyle.SetLabelOffset(0.007, "XYZ")
    tdrStyle.SetLabelSize(0.03, "XYZ")

    # For the axis:

    tdrStyle.SetAxisColor(1, "XYZ")
    tdrStyle.SetStripDecimals(True)
    tdrStyle.SetTickLength(0.03, "XYZ")
    tdrStyle.SetNdivisions(510, "XYZ")
    tdrStyle.SetPadTickX(1)  # To get tick marks on the opposite side of the frame
    tdrStyle.SetPadTickY(1)

    # Change for log plots:
    tdrStyle.SetOptLogx(0)
    tdrStyle.SetOptLogy(0)
    tdrStyle.SetOptLogz(0)

    # Postscript options:
    # tdrStyle.SetPaperSize(20.,20.)
    # tdrStyle.SetLineScalePS(Float_t scale = 3)
    # tdrStyle.SetLineStyleString(Int_t i, const char* text)
    # tdrStyle.SetHeaderPS(const char* header)
    # tdrStyle.SetTitlePS(const char* pstitle)

    # tdrStyle.SetBarOffset(Float_t baroff = 0.5)
    # tdrStyle.SetBarWidth(Float_t barwidth = 0.5)
    # tdrStyle.SetPaintTextFormat(const char* format = "g")
    # tdrStyle.SetPalette(Int_t ncolors = 0, Int_t* colors = 0)
    # tdrStyle.SetTimeOffset(Double_t toffset)
    # tdrStyle.SetHistMinimumZero(kTRUE)

    tdrStyle.SetHatchesLineWidth(1)
    tdrStyle.SetHatchesSpacing(0.5)

    tdrStyle.cd()

    if str(args.year) == '2018':
        filelist_data = [
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2018/DoubleMuon_Run2018A_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2018/DoubleMuon_Run2018B_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2018/DoubleMuon_Run2018C_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2018/DoubleMuon_Run2018D_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2018/EGamma_Run2018A_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2018/EGamma_Run2018B_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2018/EGamma_Run2018C_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2018/EGamma_Run2018D_0000.root"
        ]

        filelist_mc = [
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2018/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8_2018_0000.root",
        ]
    elif str(args.year) == '2017':
        filelist_data = [
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/DoubleMuon_Run2017B_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/DoubleMuon_Run2017C_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/DoubleMuon_Run2017D_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/DoubleMuon_Run2017E_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/DoubleMuon_Run2017F_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/DoubleEG_Run2017B_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/DoubleEG_Run2017C_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/DoubleEG_Run2017D_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/DoubleEG_Run2017E_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/DoubleEG_Run2017F_0000.root"
        ]

        filelist_mc = [
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8_2017_0000.root",
        ]
    elif str(args.year) == '2016':
        filelist_data = [
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2016Pre/DoubleMuon_Run2016B_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2016Pre/DoubleMuon_Run2016C_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2016Pre/DoubleMuon_Run2016D_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2016Pre/DoubleMuon_Run2016E_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2016Pre/DoubleMuon_Run2016F_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2016Pre/DoubleEG_Run2016B_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2016Pre/DoubleEG_Run2016C_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2016Pre/DoubleEG_Run2016D_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2016Pre/DoubleEG_Run2016E_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2016Pre/DoubleEG_Run2016F_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2016Post/DoubleMuon_Run2016F_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2016Post/DoubleMuon_Run2016G_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2016Post/DoubleMuon_Run2016H_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2016Post/DoubleEG_Run2016F_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2016Post/DoubleEG_Run2016G_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2016Post/DoubleEG_Run2016H_0000.root",
        ]

        filelist_mc = [
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2016Pre/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8_2016Pre_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2016Post/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8_2016Post_0000.root",
        ]

    # 1: barrel
    # 0: endcap
    if args.isbarrel:
        isbarrel = 1
    else:
        isbarrel = 0

    fakerate = {
        '2018':{
            'barrel':{
                'xbins':[15, 20, 30, 50, 70, 100, 5000],
                'ff':[0.629, 0.463, 0.269, 0.148, 0.110, 0.055],
                'ff_unc':[0.006, 0.006, 0.006, 0.006, 0.007, 0.004]
            },
            'endcap':{
                'xbins':[15, 50, 5000],
                'ff':[0.398, 0.114],
                'ff_unc':[0.008, 0.011]
            }
        },
        '2017':{
            'barrel':{
                'xbins':[15, 20, 30, 50, 70, 100, 5000],
                'ff':[0.641, 0.474, 0.252, 0.154, 0.082, 0.055],
                'ff_unc':[0.008, 0.007, 0.007, 0.008, 0.006, 0.006]
            },
            'endcap':{
                'xbins':[15, 50, 5000],
                'ff':[0.366, 0.062],
                'ff_unc':[0.009, 0.009]
            }
        },
        '2016':{
            'barrel':{
                'xbins':[15, 20, 30, 50, 70, 100, 5000],
                'ff':[0.538, 0.367, 0.211, 0.120, 0.089, 0.042],
                'ff_unc':[0.008, 0.007, 0.007, 0.008, 0.008, 0.005]
            },
            'endcap':{
                'xbins':[15, 50, 5000],
                'ff':[0.440, 0.130],
                'ff_unc':[0.011, 0.015]
            }
        }
    }

    if isbarrel == 1:
        xbins = fakerate[str(args.year)]['barrel']['xbins']
        ff = fakerate[str(args.year)]['barrel']['ff']
        ff_unc = fakerate[str(args.year)]['barrel']['ff_unc']
    else:
        xbins = fakerate[str(args.year)]['endcap']['xbins']
        ff = fakerate[str(args.year)]['endcap']['ff']
        ff_unc = fakerate[str(args.year)]['endcap']['ff_unc']

    from array import array
    hist_data_plj = ROOT.TH1F("","",len(xbins)-1,array('d', xbins))
    hist_datafake_plj = ROOT.TH1F("","",len(xbins)-1,array('d', xbins))
    hist_data_plj.Sumw2()
    hist_datafake_plj.Sumw2()

    for file in filelist_data:
        if str(args.year) == '2016':
            if '2016Pre' in file:
                AddHist_data(file, hist_data_plj, [15,5000], isbarrel, year='2016Pre')
            elif '2016Post' in file:
                AddHist_data(file, hist_data_plj, [15,5000], isbarrel, year='2016Post')
        else:
            AddHist_data(file, hist_data_plj, [15,5000], isbarrel, year=str(args.year))

    for file in filelist_data:
        if str(args.year) == '2016':
            if '2016Pre' in file:
                AddHist_dataFake(file, hist_datafake_plj, [15,5000], isbarrel, year='2016Pre')
            elif '2016Post' in file:
                AddHist_dataFake(file, hist_datafake_plj, [15,5000], isbarrel, year='2016Post')
        else:
            AddHist_dataFake(file, hist_datafake_plj, [15,5000], isbarrel, year=str(args.year))

    for file in filelist_mc:
        if str(args.year) == '2018':
            AddHist_mcTruth(file, hist_datafake_plj, [15,5000], isbarrel,  55.48, 59.7, year=str(args.year))
        elif str(args.year) == '2017':
            AddHist_mcTruth(file, hist_datafake_plj, [15,5000], isbarrel,  55.48, 41.5, year=str(args.year))
        if str(args.year) == '2016':
            if '2016Pre' in file:
                AddHist_mcTruth(file, hist_datafake_plj, [15,5000], isbarrel,  55.48, 19.5, year='2016Pre')
            elif '2016Post' in file:
                AddHist_mcTruth(file, hist_datafake_plj, [15,5000], isbarrel,  55.48, 16.8, year='2016Post')
        
    for i in range(1, len(xbins)):
        deno = hist_datafake_plj.GetBinContent(i)
        nume = hist_data_plj.GetBinContent(i)
        fraction = ff[i-1]
        fraction_unc = ff_unc[i-1]
        print(f'{xbins[i-1]}-{xbins[i]}: {nume}/{deno}*{fraction}+-{fraction_unc} = {nume/deno*fraction}+-{nume/deno*fraction_unc}')
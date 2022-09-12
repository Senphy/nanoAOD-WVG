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

# CMS_lumi
#   Initiated by: Gautier Hamel de Monchenault (Saclay)
#   Translated in Python by: Joshua Hardenbrook (Princeton)
#   Updated by:   Dinko Ferencek (Rutgers)
#

cmsText     = "CMS";
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
lumi_sqrtS = "41.5 fb^{-1} (13 TeV)"

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

        
def AddHist_data(file, hist, ptrange, isbarrel):
    
    init_branches = ['photon_sieie','photon_vidNestedWPBitmap','photon_eta','photon_pt','photon_pfRelIso03_chg',\
                'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL',\
                'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',\
                'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ',\
                'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8',\
                'HLT_Ele32_WPTight_Gsf_L1DoubleEG',\
                'HLT_IsoMu27']
    branches = uproot.open(file+':Events').arrays(init_branches, library='pd')
    HLT_SingleMuon = branches.loc[:,'HLT_IsoMu27'] == True
    HLT_DoubleMuon = branches.loc[:,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8']
    HLT_SingleElectron = branches.loc[:,'HLT_Ele32_WPTight_Gsf_L1DoubleEG'] == True
    HLT_DoubleEG = branches.loc[:,'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'] == True
    HLT_MuonEG1 = branches.loc[:,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'] == True
    HLT_MuonEG2 = branches.loc[:,'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'] == True
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
    
    if isbarrel == 1:
        eta_cut = abs(arrays.loc[:,'photon_eta']) < 1.4442
#         chg_cut = (arrays.loc[:,'photon_pfRelIso03_chg']*arrays.loc[:,'photon_pt']) < 1.141
    elif isbarrel == 0:
        eta_cut = abs((arrays.loc[:,'photon_eta']) > 1.566) & abs((arrays.loc[:,'photon_eta']) < 2.5)
#         chg_cut = (arrays.loc[:,'photon_pfRelIso03_chg']*arrays.loc[:,'photon_pt']) < 1.051
        
    mask_mediumID_withoutsieie = (1<<1) | (1<<3) | (1<<5) | (1<<9) | (1<<11) | (1<<13)
    arrays['mediumID'] = arrays['photon_vidNestedWPBitmap'] & mask_mediumID_withoutsieie
    arrays = arrays.loc[arrays.loc[:,'mediumID'] == mask_mediumID_withoutsieie, :]
    
    pt_cut = (arrays.loc[:,'photon_pt'] >= ptrange[0]) & (arrays.loc[:,'photon_pt'] < ptrange[1]) 
    arrays = arrays.loc[pt_cut & eta_cut,:]
    
    for i in trange(0, len(arrays['photon_sieie']), desc=f'fill sigma ieta ieta for {file}'):
        hist.Fill(float(arrays['photon_sieie'].values[i]))
    
    
def AddHist_mcTruth(file, hist, ptrange, isbarrel, xsec, lumi):
    init_branches = ['Generator_weight',\
                'photon_sieie','photon_vidNestedWPBitmap','photon_genPartFlav','photon_eta','photon_pt','photon_pfRelIso03_chg',\
                'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL',\
                'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',\
                'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ',\
                'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8',\
                'HLT_Ele32_WPTight_Gsf_L1DoubleEG',\
                'HLT_IsoMu27']
    branches = uproot.open(file+':Events').arrays(init_branches, library='pd')
    true_events = uproot.open(file)['nEventsGenWeighted'].values()[0]
    HLT_SingleMuon = branches.loc[:,'HLT_IsoMu27'] == True
    HLT_DoubleMuon = branches.loc[:,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8']
    HLT_SingleElectron = branches.loc[:,'HLT_Ele32_WPTight_Gsf_L1DoubleEG'] == True
    HLT_DoubleEG = branches.loc[:,'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'] == True
    HLT_MuonEG1 = branches.loc[:,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'] == True
    HLT_MuonEG2 = branches.loc[:,'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'] == True
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
    
    if isbarrel == 1:
        eta_cut = abs(arrays.loc[:,'photon_eta']) < 1.4442
    elif isbarrel == 0:
        eta_cut = abs((arrays.loc[:,'photon_eta']) > 1.566) & abs((arrays.loc[:,'photon_eta']) < 2.5)
        
    mask_mediumID_withoutsieie = (1<<1) | (1<<3) | (1<<5) | (1<<9) | (1<<11) | (1<<13)
    arrays['mediumID'] = arrays['photon_vidNestedWPBitmap'] & mask_mediumID_withoutsieie
    arrays = arrays.loc[arrays.loc[:,'mediumID'] == mask_mediumID_withoutsieie, :]
    
    pt_cut = (arrays.loc[:,'photon_pt'] >= ptrange[0]) & (arrays.loc[:,'photon_pt'] < ptrange[1]) 
    gen_cut = arrays.loc[:,'photon_genPartFlav'] != 0
    arrays = arrays.loc[pt_cut & eta_cut & gen_cut,:]
    
    arrays['Generator_weight_sgn'] = arrays['Generator_weight'].apply(lambda x: 1 if x >= 0 else -1)
    arrays['true_weight'] = lumi * xsec * 1000 * arrays['Generator_weight_sgn'] / true_events
    
    for i in trange(0, len(arrays['photon_sieie']), desc=f'fill sigma ieta ieta for {file}'):
        hist.Fill(float(arrays['photon_sieie'].values[i]), float(arrays['true_weight'].values[i]))
        
    
def AddHist_dataFake(file, hist, ptrange, isbarrel):
    init_branches = ['photon_sieie','photon_vidNestedWPBitmap','photon_eta','photon_pt','photon_pfRelIso03_chg',\
                'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL',\
                'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',\
                'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ',\
                'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8',\
                'HLT_Ele32_WPTight_Gsf_L1DoubleEG',\
                'HLT_IsoMu27']
    branches = uproot.open(file+':Events').arrays(init_branches, library='pd')
    HLT_SingleMuon = branches.loc[:,'HLT_IsoMu27'] == True
    HLT_DoubleMuon = branches.loc[:,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8']
    HLT_SingleElectron = branches.loc[:,'HLT_Ele32_WPTight_Gsf_L1DoubleEG'] == True
    HLT_DoubleEG = branches.loc[:,'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'] == True
    HLT_MuonEG1 = branches.loc[:,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'] == True
    HLT_MuonEG2 = branches.loc[:,'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'] == True
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
        
    if isbarrel == 1:
        eta_cut = abs(arrays.loc[:,'photon_eta']) < 1.4442
    elif isbarrel == 0:
        eta_cut = abs((arrays.loc[:,'photon_eta']) > 1.566) & abs((arrays.loc[:,'photon_eta']) < 2.5)
        
    chg_cut = ((arrays.loc[:,"photon_pfRelIso03_chg"]*arrays.loc[:,"photon_pt"]) > 4) & ((arrays.loc[:,"photon_pfRelIso03_chg"]*arrays.loc[:,"photon_pt"]) < 10)
    pt_cut = (arrays.loc[:,'photon_pt'] >= ptrange[0]) & (arrays.loc[:,'photon_pt'] < ptrange[1]) 
    arrays = arrays.loc[pt_cut & eta_cut & chg_cut ,:]
    
    for i in trange(0, len(arrays['photon_sieie']), desc=f'fill sigma ieta ieta for {file}'):
        hist.Fill(float(arrays['photon_sieie'].values[i]))
        
# def FakeFraction_Fit(hist_data, hist_mcTruth, hist_dataFake):
    
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

    # 1: barrel
    # 0: endcap
    isbarrel = 1

    if isbarrel:
        xbins = 28
        xleft = 0.00615
        xright = 0.02015
        ptlist = [20, 30, 50, 80, 120, 5000]
    else:
        xbins = 40
        xleft = 0.0172
        xright = 0.0572
        ptlist = [20, 50, 5000]

    for i, ptlow in enumerate(ptlist[:len(ptlist)-1]):
        pthigh = ptlist[i+1]
        ptrange = [ptlow,pthigh]
        print(f'preparing for {ptrange}')
        hist_data = ROOT.TH1F("","",xbins,xleft,xright)
        hist_mctruth = ROOT.TH1F("","",xbins,xleft,xright)
        hist_datafake = ROOT.TH1F("","",xbins,xleft,xright)
        hist_data.Sumw2()
        hist_mctruth.Sumw2()
        hist_datafake.Sumw2()

        filelist_data = [
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/SingleMuon_Run2017B_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/SingleMuon_Run2017C_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/SingleMuon_Run2017D_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/SingleMuon_Run2017E_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/SingleMuon_Run2017F_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/DoubleMuon_Run2017B_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/DoubleMuon_Run2017C_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/DoubleMuon_Run2017D_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/DoubleMuon_Run2017E_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/DoubleMuon_Run2017F_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/SingleElectron_Run2017B_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/SingleElectron_Run2017C_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/SingleElectron_Run2017D_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/SingleElectron_Run2017E_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/SingleElectron_Run2017F_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/DoubleEG_Run2017B_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/DoubleEG_Run2017C_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/DoubleEG_Run2017D_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/DoubleEG_Run2017E_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/DoubleEG_Run2017F_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/MuonEG_Run2017B_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/MuonEG_Run2017C_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/MuonEG_Run2017D_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/MuonEG_Run2017E_0000.root",
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/MuonEG_Run2017F_0000.root",
        ]

        filelist_mc = [
            "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/CR/2017/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8_2017_0000.root",
        ]

        for file in filelist_data:
            AddHist_data(file, hist_data, ptrange, isbarrel)
        for file in filelist_mc:
            AddHist_mcTruth(file, hist_mctruth, ptrange, isbarrel,  55.48, 59.7)
        for file in filelist_data:
            AddHist_dataFake(file, hist_datafake, ptrange, isbarrel)

        # Observable
        sieie = ROOT.RooRealVar("sieie","sieie",xleft,xright)

        # Import hist
        data_hist = ROOT.RooDataHist("data_hist", "data with x(sieie)", ROOT.RooArgList(sieie), ROOT.RooFit.Import(hist_data))
        TruePhotons_hist = ROOT.RooDataHist("TruePhotons_hist", "true photons MC with x(sieie)", ROOT.RooArgList(sieie), ROOT.RooFit.Import(hist_mctruth))
        FakePhotons_hist = ROOT.RooDataHist("FakePhotons_hist", "fake photons data with x(sieie)", ROOT.RooArgList(sieie), ROOT.RooFit.Import(hist_datafake))

        ndata = hist_data.GetSumOfWeights()

        # Parameters
        # TrueFraction = ROOT.RooRealVar("TrueFraction","fraction of true photons", 0, 1)
        # FakeFraction = ROOT.RooRealVar("FakeFraction","fraction of fake photons", 0, 1)

        ntrue = ROOT.RooRealVar("true number", "true number", 0.5*ndata, 0, ndata)
        nfake = ROOT.RooRealVar("fake number", "fake number", 0.5*ndata, 0, ndata)

        # PDF
        true_pdf = ROOT.RooHistPdf("true_pdf", "truepdf", sieie, TruePhotons_hist)
        fake_pdf = ROOT.RooHistPdf("fake_pdf", "fakepdf", sieie, FakePhotons_hist)

        etrue_pdf = ROOT.RooExtendPdf("ntrue", "ntrue", true_pdf, ntrue)
        efake_pdf = ROOT.RooExtendPdf("nfake", "nfake", fake_pdf, nfake)

        fullpdf = ROOT.RooAddPdf("fullpdf", "true plus fake", ROOT.RooArgList(etrue_pdf, efake_pdf))

        # Fit
        fullpdf.fitTo(data_hist, ROOT.RooFit.SumW2Error(True), ROOT.RooFit.Extended(True))

        chi2 = ROOT.RooChi2Var("chi2", "chi2", fullpdf, data_hist)
        chi2ToNDF = chi2.getVal() / xbins

        # Plot
        if isbarrel == 1:
            region_mark = "Barrel"
        else:
            region_mark = "Endcap"
            
        xframe = sieie.frame(ROOT.RooFit.Title(f"{region_mark} region, {ptrange[0]} GeV < photon PT < {ptrange[1]}"), ROOT.RooFit.Bins(xbins))
        xframe.GetXaxis().SetTitle("#sigma_{i#etai#eta}")
        xframe.GetYaxis().SetTitle("events / bin")
        xframe.GetYaxis().SetTitleSize(48)
        xframe.GetYaxis().SetTitleFont(43)
        xframe.GetYaxis().SetTitleOffset(1.50)
        xframe.GetYaxis().SetLabelFont(43)
        xframe.GetYaxis().SetLabelSize(28)
        xframe.GetYaxis().SetLabelOffset(0.020)

        xframe.GetXaxis().SetTitleSize(48)
        xframe.GetXaxis().SetTitleFont(43)
        xframe.GetXaxis().SetTitleOffset(1.3)
        xframe.GetXaxis().SetLabelFont(43)
        xframe.GetXaxis().SetLabelSize(28)
        xframe.GetXaxis().SetLabelOffset(0.035)
        xframe.GetXaxis().SetTitle("#sigma_{i#etai#eta}")
        xframe.GetYaxis().SetTitle("events / bin")

        data_hist.plotOn(xframe)
        fullpdf.plotOn(xframe, ROOT.RooFit.Name("sum"), ROOT.RooFit.FillStyle(4100), ROOT.RooFit.FillColor(20), ROOT.RooFit.DrawOption("F"))
        fullpdf.plotOn(xframe, ROOT.RooFit.Components("ntrue"), ROOT.RooFit.Name("true"), ROOT.RooFit.LineColor(4), ROOT.RooFit.LineStyle(9))
        fullpdf.plotOn(xframe, ROOT.RooFit.Components("nfake"), ROOT.RooFit.Name("fake"), ROOT.RooFit.LineColor(2), ROOT.RooFit.LineStyle(9))
        data_hist.plotOn(xframe)

        c1 = ROOT.TCanvas("","",1000,1000)
        c1.Draw()
        xframe.Draw()

        legend = ROOT.TLegend(0.55, 0.60, 0.70, 0.85)
        legend.SetBorderSize(0)
        legend.SetFillColor(0)
        legend.SetTextSize(0.025)
        legend.SetLineWidth(1)
        legend.SetLineStyle(0)
        legend.AddEntry(hist_data,'data template')
        hist_fit_NaN = hist_data.Clone() # Just for plot
        hist_fit_NaN.SetLineColor(20)
        hist_fit_NaN.SetLineWidth(0)
        hist_fit_NaN.SetFillColor(20)
        hist_fit_NaN.SetMarkerStyle(0)
        legend.AddEntry(hist_fit_NaN,'Fit result', "F")
        legend.AddEntry(hist_mctruth,'True photons (from MC)')
        legend.AddEntry(hist_datafake,'Fake photons (from data)')
        legend.Draw("SAME")

        hist_mctruth.SetMarkerStyle(0)
        hist_mctruth.SetLineColor(4)
        hist_mctruth.SetLineWidth(3)

        hist_datafake.SetMarkerStyle(0)
        hist_datafake.SetLineColor(2)
        hist_datafake.SetLineWidth(3)

        textChi2 = ROOT.TLatex()
        textChi2.SetNDC()
        textChi2.SetTextSize(0.025)
        textChi2.DrawLatex(0.55, 0.55, "#chi^{2}/n="+str("%.2f" % chi2ToNDF))
        textChi2.DrawLatex(0.55, 0.50, str(ptrange[0])+" GeV < #gamma P_{T} < "+str(ptrange[1])+" GeV")

        # Calculate fake fraction within original sieie cut
        result_nfake = nfake.getVal()
        result_nfake_err = nfake.getAsymErrorHi()
        result_ntrue = ntrue.getVal()
        result_ntrue_err = ntrue.getAsymErrorHi()
        if isbarrel == 1:
            sieie.setRange('window', 0.00515, 0.01015)
        else:
            sieie.setRange('window', 0.0172, 0.0272)
        fakeratio = efake_pdf.createIntegral(sieie, sieie, 'window')
        nfake_window = result_nfake*fakeratio.getVal()
        nfake_window_err = numpy.sqrt(result_nfake_err*result_nfake_err*fakeratio.getVal()*fakeratio.getVal())

        trueratio = etrue_pdf.createIntegral(sieie, sieie, 'window')
        ntrue_window = result_ntrue*trueratio.getVal()
        ntrue_window_err = numpy.sqrt(result_ntrue_err*result_ntrue_err*trueratio.getVal()*trueratio.getVal())

        fake_fraction = nfake_window / (nfake_window + ntrue_window)
        fake_fraction_err = numpy.sqrt(pow(nfake_window/pow(ntrue_window+nfake_window,2),2)*pow(ntrue_window_err,2) + pow(ntrue_window/pow(nfake_window+ntrue_window,2),2)*pow(nfake_window_err,2))
        textChi2.DrawLatex(0.55, 0.45, "Fake Fraction: "+ str("%.3f" % fake_fraction) + "#pm " + str("%.3f" % fake_fraction_err)) 


        c1.SetBottomMargin(0.15)
        c1.SetTopMargin(0.10)
        c1.SetRightMargin(0.05)
        c1.SetLeftMargin(0.15)
        CMS_lumi(c1, 0, 0)

        c1.SaveAs(f'2017/{region_mark}_pt{str(ptrange[0])}_{str(ptrange[1])}_v9.pdf')
        c1.SaveAs(f'2017/{region_mark}_pt{str(ptrange[0])}_{str(ptrange[1])}_v9.png')
        # print (ntrue.getVal())
        # print (ntrue.getAsymErrorHi())
        # print (ntrue.getAsymErrorLo())

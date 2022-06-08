from typing import Set
import ROOT
import os,sys
from array import array
import time

sys.path.append(os.getcwd())
from Control_pad import channel_map
from Control_pad import channel
from Control_pad import UpDown_map
from Control_pad import filelist_MC
from Control_pad import branch
from Control_pad import UpDown
sys.path.append('..')
import tdr as tdrStyle
from lumi import CMS_lumi
from AddHist_help import SetHistStyle
from ratio import createRatio
        
def Plot():

    time_total_init = time.time()

    file_hist = ROOT.TFile(f'./test/{channel_map[channel]}.root',"OPEN")
    hist_data = {}
    for branch_name in branch:
        plot_branch = branch[branch_name]["name"]
        hist_data[plot_branch] = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_data_{str(UpDown_map[0])}')

    for file in filelist_MC:
        hist_MC = {}
        for branch_name in branch:
            plot_branch = branch[branch_name]["name"]
            hist_MC[plot_branch] = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{str(UpDown_map[UpDown])}')
            
        filelist_MC[file]["hist"] = hist_MC
    
    hist_FakeLep = {}
    for branch_name in branch:
        plot_branch = branch[branch_name]["name"]
        hist_FakeLep[plot_branch] = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_FakeLep_{str(UpDown_map[0])}')

    hist_FakePho= {}
    for branch_name in branch:
        plot_branch = branch[branch_name]["name"]
        hist_FakePho[plot_branch] = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_FakePho_{str(UpDown_map[0])}')

    tdrStyle.setTDRStyle()
    tdrStyle.gtdr()

    for branch_name in branch:
        plot_branch = branch[branch_name]["name"]
        c1 = ROOT.TCanvas("","",1000,1000)

        if branch[branch_name].__contains__("bin_array"):
            MC_err = ROOT.TH1D("","",len(branch[plot_branch]["bin_array"])-1,array('d', branch[plot_branch]["bin_array"]))
            ggZZ_sum = ROOT.TH1D("","",len(branch[plot_branch]["bin_array"])-1,array('d', branch[plot_branch]["bin_array"]))
        else:
            MC_err = ROOT.TH1D("","",branch[plot_branch]["xbins"],branch[plot_branch]["xleft"],branch[plot_branch]["xright"])
            ggZZ_sum = ROOT.TH1D("","",branch[plot_branch]["xbins"],branch[plot_branch]["xleft"],branch[plot_branch]["xright"])
        SetHistStyle(ggZZ_sum, filelist_MC["ggZZ_4e"]["color"])
        MC_err.Sumw2()
        MC_err.SetFillColor(ROOT.kGray+2)
        MC_err.SetFillStyle(3345)
        MC_err.SetMarkerSize(0.)
        MC_err.SetMarkerColor(ROOT.kGray+2)
        MC_err.SetLineWidth(2)
        MC_err.SetLineColor(0)
        MC_err.SetStats(0)
        MC_err.SetXTitle(f'{branch[plot_branch]["axis_name"]}')
        MC_err.SetYTitle(f'events / bin')

        stack_mc = ROOT.THStack("","")
        MC_err.Add(hist_FakeLep[plot_branch])
        stack_mc.Add(hist_FakeLep[plot_branch])
        MC_err.Add(hist_FakePho[plot_branch])
        stack_mc.Add(hist_FakePho[plot_branch])
        for file in filelist_MC:
            if 'ggZZ' in file:
                ggZZ_sum.Add(filelist_MC[file]["hist"][plot_branch])
                continue
            
            if 'WZG' in file:
                continue
                
            SetHistStyle(filelist_MC[file]["hist"][plot_branch], filelist_MC[file]["color"])
            stack_mc.Add(filelist_MC[file]["hist"][plot_branch])
            MC_err.Add(filelist_MC[file]["hist"][plot_branch])
            
        stack_mc.Add(ggZZ_sum)
        MC_err.Add(ggZZ_sum)
        stack_mc.Add(filelist_MC['WZG']["hist"][plot_branch])
        MC_err.Add(filelist_MC['WZG']["hist"][plot_branch])


        legend = ROOT.TLegend(0.20, 0.45, 0.85, 0.85)
        legend.SetNColumns(2)
        legend.SetBorderSize(0)
        legend.SetFillColor(0)
        legend.SetTextSize(0.035)
        legend.SetLineWidth(1)
        legend.SetLineStyle(0)
        for file in filelist_MC:
            if 'ggZZ' in file:
                continue
            if 'WZG' in file:
                continue
            legend.AddEntry(filelist_MC[file]["hist"][plot_branch], f'{filelist_MC[file]["name"]}: {format(filelist_MC[file]["hist"][plot_branch].GetSumOfWeights(), ".2f")}','F')
            
        legend.AddEntry(filelist_MC["WZG"]["hist"][plot_branch], f'{filelist_MC["WZG"]["name"]}: {format(filelist_MC[file]["hist"][plot_branch].GetSumOfWeights(), ".2f")}','F')
        legend.AddEntry(ggZZ_sum,f'ggZZ: {format(ggZZ_sum.GetSumOfWeights(), ".2f")}', 'F')
        print(ggZZ_sum.GetSumOfWeights())
        legend.AddEntry(hist_FakeLep[plot_branch],f'Nonprompt l: {format(hist_FakeLep[plot_branch].GetSumOfWeights(), ".2f")}', 'F')
        if not (channel in [0,1,2,3,4]):
            legend.AddEntry(hist_data[plot_branch], f'data: {format(hist_data[plot_branch].GetSumOfWeights(), ".2f")}')
        if channel in [0,1,2,3,4,30,31,32,20,21,22,23,24]:
            legend.AddEntry(hist_FakePho[plot_branch],f'Nonprompt #gamma: {format(hist_FakePho[plot_branch].GetSumOfWeights(), ".2f")}', 'F')
        Stat_Unc_Total = sum([MC_err.GetBinError(Bin) for Bin in range(1, MC_err.GetNbinsX()+1)])
        legend.AddEntry(MC_err, f'Stat Unc.: {format(Stat_Unc_Total, ".2f")}', 'F')


        c1.Draw()
        pad1 = ROOT.TPad("pad1", "pad1", 0, 0.30, 1, 1.00)
        pad1.SetTopMargin(0.1)  # joins upper and lower plot
        pad1.SetBottomMargin(0.035)  # joins upper and lower plot
        # pad1.SetGridx()
        pad1.Draw()
        # Lower ratio plot is pad2
        c1.cd()  # returns to main canvas before defining pad2
        pad2 = ROOT.TPad("pad2", "pad2", 0, 0.00, 1, 0.30)
        pad2.SetTopMargin(0.040)  # joins upper and lower plot
        pad2.SetBottomMargin(0.40)  # joins upper and lower plot
        pad2.SetGridy()
        pad2.Draw()

        # draw everything
        pad1.cd()
        if not (channel in [0,1,2,3,4]):
            hist_data[plot_branch].SetXTitle(f'{branch[plot_branch]["axis_name"]}')
            SetHistStyle(hist_data[plot_branch], 1)
            hist_data[plot_branch].Draw("E0X0p")
            # hist_data.SetMinimum(10)
            hist_data[plot_branch].SetMaximum(3.5*hist_data[plot_branch].GetMaximum())
            stack_mc.Draw("HIST SAME")
            MC_err.Draw("e2 SAME")
            hist_data[plot_branch].Draw("E0X0p SAME")
            hist_data[plot_branch].GetXaxis().SetLabelSize(0)
        else:
            MC_err.Draw("e2")
            MC_err.SetMaximum(3.5 * MC_err.GetMaximum())
            stack_mc.Draw("HIST SAME")
            MC_err.Draw("e2 SAME")
        legend.Draw("SAME")
        # ROOT.gPad.SetLogy()
        ROOT.gPad.RedrawAxis()

        # h1.GetXaxis().SetLabelSize(0)
        pad2.cd()
        h3 = createRatio(hist_data[plot_branch], MC_err)
        SetHistStyle(h3, 1)
        h3.SetYTitle("Data/Pred.")
        h4 = createRatio(MC_err, MC_err)
        SetHistStyle(h4, 1)
        if not (channel in [0,1,2,3,4]):
            h3.Draw("E0X0p")
            h4.Draw("e2 SAME")
        else:
            h4.Draw("e2")
        ROOT.gPad.RedrawAxis()
        ROOT.gStyle.SetPadLeftMargin(0.15)

        CMS_lumi(pad1, 0, 0)
        c1.Update()
        c1.SaveAs(f'./test/{channel_map[channel]}_{plot_branch}_{str(UpDown_map[UpDown])}.pdf')
        c1.SaveAs(f'./test/{channel_map[channel]}_{plot_branch}_{str(UpDown_map[UpDown])}.png')
        del c1,pad1,pad2
        print (time.time()-time_total_init)

if __name__ == "__main__":
    sys.exit(Plot())
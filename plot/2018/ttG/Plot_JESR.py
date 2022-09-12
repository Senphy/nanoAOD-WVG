import ROOT
import os,sys
from array import array
import time

sys.path.append('..')
from lumi import CMS_lumi
from AddHist_help import SetHistStyle
from ratio import createRatio
from Control_pad import channel_map
from Control_pad import channel
from Control_pad import UpDown_map
from Control_pad import filelist_MC
from Control_pad import branch
        
def Plot_JESR():

    time_total_init = time.time()

    file_hist = ROOT.TFile(f'./test/{channel_map[channel]}.root',"OPEN")

    for file in filelist_MC:
        hist_MC_nominal = {}
        hist_MC_jesup = {}
        hist_MC_jesdown = {}
        hist_MC_jerup = {}
        hist_MC_jerdown  = {}
        for branch_name in branch:
            plot_branch = branch[branch_name]["name"]
            hist_MC_nominal[plot_branch] = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{str(UpDown_map[0])}')
            hist_MC_jesup[plot_branch] = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{str(UpDown_map[1])}')
            hist_MC_jesdown[plot_branch] = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{str(UpDown_map[2])}')
            hist_MC_jerup[plot_branch] = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{str(UpDown_map[3])}')
            hist_MC_jerdown[plot_branch] = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{str(UpDown_map[4])}')
            
        filelist_MC[file]["hist"] = hist_MC_nominal
        filelist_MC[file]["hist_jesup"] = hist_MC_jesup
        filelist_MC[file]["hist_jesdown"] = hist_MC_jesup
        filelist_MC[file]["hist_jerup"] = hist_MC_jerup
        filelist_MC[file]["hist_jerdown"] = hist_MC_jerdown
    
    tdrStyle =  ROOT.TStyle("","")

    #for the canvas:
    tdrStyle.SetCanvasBorderMode(1)
    tdrStyle.SetCanvasColor(ROOT.kWhite)
    tdrStyle.SetCanvasDefH(1000) #Height of canvas
    tdrStyle.SetCanvasDefW(800) #Width of canvas
    tdrStyle.SetCanvasDefX(0)   #POsition on screen
    tdrStyle.SetCanvasDefY(0)


    tdrStyle.SetPadBorderMode(1)
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
    tdrStyle.SetPadTopMargin(0.15)
    tdrStyle.SetPadBottomMargin(0.42)
    tdrStyle.SetPadLeftMargin(0.11)
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
    tdrStyle.SetTitleSize(0.05, "XYZ")
    #   tdrStyle.SetTitleXSize(Float_t size = 0.02) # Another way to set the size?
    #   tdrStyle.SetTitleYSize(Float_t size = 0.02)
    tdrStyle.SetTitleXOffset(1.20)
    tdrStyle.SetTitleYOffset(1.20)
    # tdrStyle.SetTitleOffset(1.1, "Y") # Another way to set the Offset

    # For the axis labels:

    tdrStyle.SetLabelColor(1, "XYZ")
    tdrStyle.SetLabelFont(42, "XYZ")
    tdrStyle.SetLabelOffset(0.010, "XYZ")
    tdrStyle.SetLabelSize(0.05, "XYZ")

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

    for jesr in ['jes', 'jer']:
        for branch_name in branch:
            for file in filelist_MC:
                plot_branch = branch[branch_name]["name"]
                c1 = ROOT.TCanvas("","",1000,800)

                MC_err = ROOT.TH1D("","",branch[plot_branch]["xbins"],branch[plot_branch]["xleft"],branch[plot_branch]["xright"])
                MC_err.Sumw2()
                SetHistStyle(MC_err, 1)
                MC_err.SetXTitle(f'{branch[plot_branch]["axis_name"]}')
                MC_err.SetYTitle(f'events / bin')

                MC_err_up = MC_err.Clone()
                MC_err_up.SetLineColor(3)
                MC_err_up.SetLineWidth(2)
                MC_err_down = MC_err.Clone()
                MC_err_down.SetLineColor(4)
                MC_err_down.SetLineWidth(2)

                MC_err.Add(filelist_MC[file]["hist"][plot_branch])
                MC_err_up.Add(filelist_MC[file][f"hist_{jesr}down"][plot_branch])
                MC_err_down.Add(filelist_MC[file][f"hist_{jesr}up"][plot_branch])

                legend = ROOT.TLegend(0.65, 0.45, 0.85, 0.80)
                # legend.SetNColumns(3)
                legend.SetBorderSize(0)
                legend.SetFillColor(0)
                legend.SetTextSize(0.040)
                legend.SetLineWidth(1)
                legend.SetLineStyle(0)
                    
                legend.AddEntry(MC_err, f'{jesr}Total central')
                legend.AddEntry(MC_err_up, f'{jesr}Total up', 'l')
                legend.AddEntry(MC_err_down, f'{jesr}Total down', 'l')

                texts1 = ROOT.TText(.2, .75, "Samples: "+str(filelist_MC[file]["name"]))
                texts1.SetNDC()
                texts1.SetTextFont(42)
                texts1.SetTextSize(0.04)
                texts2 = ROOT.TText(.2, .7, "Region: "+str(channel_map[channel]))
                texts2.SetNDC()
                texts2.SetTextFont(42)
                texts2.SetTextSize(0.04)

                c1.Draw()
                pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
                pad1.SetBottomMargin(0.015)  # joins upper and lower plot
                # pad1.SetGridx()
                pad1.Draw()
                # Lower ratio plot is pad2
                c1.cd()  # returns to main canvas before defining pad2
                pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.29)
                pad2.SetTopMargin(0)  # joins upper and lower plot
                pad2.SetGridy()
                pad2.Draw()

                # draw everything
                pad1.cd()
                MC_err.Draw("ep")
                MC_err.SetMaximum(2.0 * MC_err.GetMaximum())
                MC_err_up.Draw("HIST SAME")
                MC_err_down.Draw("HIST SAME")
                legend.Draw("SAME")
                texts1.Draw("SAME")
                texts2.Draw("SAME")
                # ROOT.gPad.SetLogy()
                ROOT.gPad.RedrawAxis()

                # h1.GetXaxis().SetLabelSize(0)
                pad2.cd()
                h3 = createRatio(MC_err_up, MC_err)
                h3.SetLineColor(3)
                h4 = createRatio(MC_err_down, MC_err)
                h4.SetLineColor(4)
                h5 = createRatio(MC_err, MC_err)
                h5.Draw("ep")
                h3.Draw("HIST SAME")
                h4.Draw("HIST SAME")
                h5.GetXaxis().SetTitleOffset(4.0)
                h5.SetYTitle("ratio")
                ROOT.gPad.RedrawAxis()

                CMS_lumi(pad1, 0, 0)
                c1.Update()
                c1.SaveAs(f'./test/jesr/{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{jesr}Total.pdf')
                c1.SaveAs(f'./test/jesr/{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{jesr}Total.png')
                del c1,pad1,pad2
                print (time.time()-time_total_init)

if __name__ == "__main__":
    sys.exit(Plot_JESR())
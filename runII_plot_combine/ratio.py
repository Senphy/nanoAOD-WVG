from ROOT import TCanvas, TColor, TGaxis, TH1F, TPad
from ROOT import kBlack, kBlue, kRed

def createRatio(h1, h2):
    h3 = h1.Clone("h3")
    h3.SetLineColor(kBlack)
    h3.SetMarkerStyle(21)
    h3.SetTitle("")
    h3.SetMinimum(0.50)
    h3.SetMaximum(1.50)
    # Set up plot for markers and errors
    h3.Sumw2()
    h3.SetStats(0)
    h3.Divide(h2)

    # Adjust y-axis settings
    y = h3.GetYaxis()
    y.SetTitle("Data / MC ")
    y.SetNdivisions(103)
    y.SetTitleSize(35)
    y.SetTitleFont(43)
    y.SetTitleOffset(1.50)
    y.SetLabelFont(43)
    y.SetLabelSize(35)

    # Adjust x-axis settings
    x = h3.GetXaxis()
    x.SetTitleSize(35)
    x.SetTitleFont(43)
    x.SetTitleOffset(4.5)
    x.SetLabelFont(43)
    x.SetLabelSize(35)

    return h3

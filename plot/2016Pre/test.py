import sys,os
import ROOT
from copy import deepcopy

a = ROOT.TH1D("","",10,0,10)
b = deepcopy(a)
c = deepcopy(a)

b.Fill(0)

print(b.GetBinContent(1))
print(c.GetBinContent(1))

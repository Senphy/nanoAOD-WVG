#include <iostream>
#include <cstdlib>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <algorithm>
#include <functional>
#include <assert.h>


#include "TTree.h"
#include "TFile.h"
#include "TLorentzVector.h"
#include "Math/Vector3D.h"
#include "Math/Vector4D.h"

#include "TRandom.h"

void electron_pt_comparison(){
    TFile *file1 = TFile::Open("WZG_skim.root");
    TFile *file2 = TFile::Open("TTWJetsToLNu_skim.root");

    TTree* tree_1 = (TTree*) file1-> Get("Events");
    TH1F* electron_pt1_h = new TH1F ("electron_pt1_h","electron_comparison",100,0,900);
    tree_1->Draw("electron_pt >> electron_pt1_h","","goff");

    TTree* tree_2 = (TTree*) file2-> Get("Events");
    TH1F* electron_pt2_h = new TH1F ("electron_pt2_h","electron_comparison",100,0,900);
    tree_2->Draw("electron_pt >> electron_pt2_h","","goff");

    double integral_scale = electron_pt1_h->Integral();
    std::cout << " integral_scale = " << integral_scale << std::endl;
    electron_pt1_h->Scale (1. / integral_scale);
    electron_pt1_h->SetTitle("electron P_{T} comparison");
    electron_pt1_h->GetXaxis()->SetTitle ("electron p_{T} [GeV]");
    electron_pt1_h->GetYaxis()->SetTitle ("a.u.");
    // electron_pt1_h->GetYaxis()->CenterTitle();
    electron_pt1_h->SetLineWidth(2);
    electron_pt1_h->SetLineColor(kBlack);
    electron_pt1_h->SetMarkerStyle(20);
    electron_pt1_h->SetStats(kFALSE);
    
    double integral_scale = electron_pt2_h->Integral();
    electron_pt2_h->Scale (1. / integral_scale);
    electron_pt2_h->SetTitle("electron P_{T} comparison");
    electron_pt2_h->GetXaxis()->SetTitle ("electron p_{T} [GeV]");
    electron_pt2_h->GetYaxis()->SetTitle ("a.u.");
    // electron_pt2_h->GetYaxis()->CenterTitle();
    electron_pt2_h->SetLineWidth(2);
    electron_pt2_h->SetLineColor(kRed);
    electron_pt2_h->SetStats(kFALSE);

    TCanvas* electron_pt_canvas = new TCanvas ("electron_pt_canvas","electron_pt_canvas",1000,800);
    electron_pt2_h->Draw("");
    electron_pt1_h->Draw("same");

    TLegend *legend = new TLegend(.75,.80,.95,.95); 
    legend->AddEntry(electron_pt1_h,"WZG"); 
    legend->AddEntry(electron_pt2_h,"TTWJetsToLNu");
    legend->Draw();
    electron_pt_canvas->SetGrid();
    electron_pt_canvas->SetLogx();
    electron_pt_canvas->SaveAs("electron_pt_comparison.png");

}
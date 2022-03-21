channel = 10
channel_map = {
    0: "WZG",
    1: "WZG_emm",
    2: "WZG_mee",
    3: "WZG_eee",
    4: "WZG_mmm",

    10: "ttZ",
    11: "ttZ_emm",
    12: "ttZ_mee",
    13: "ttZ_eee",
    14: "ttZ_mmm",

    20: "ttG",
    21: "ttG_emm",
    22: "ttG_mee",
    23: "ttG_eee",
    24: "ttG_mmm",

    9: "ZZ",
    5: "ZZ_eemm",
    6: "ZZ_mmee",
    7: "ZZ_eeee",
    8: "ZZ_mmmm"
}

lumi = 41.5
year = "2017"

UpDown = 0
UpDown_map={
    0:None,
    1:"jesTotalUp",
    2:"jesTotalDown",
    3:"jerUp",
    4:"jerDown"
}
# 0: nominal
# 1: JESup 
# 2: JESdown
# 3: JERup
# 4: JERdown

branch = {
    "ttZ_dileptonmass":{
        "name":"ttZ_dileptonmass",
        "axis_name":"m_{Z} [GeV]",
        "xbins":20,
        "xleft":0,
        "xright":200,
    },
    "ttZ_trileptonmass":{
        "name":"ttZ_trileptonmass",
        "axis_name":"m_{lll} [GeV]",
        "bin_array":[100,150,200,250,300,500],
    },
    "ttZ_lepton1_pt":{
        "name":"ttZ_lepton1_pt",
        "axis_name":"P_{T, W} [GeV]",
        "xbins":10,
        "xleft":0,
        "xright":200,
    },
    "ttZ_lepton1_eta":{
        "name":"ttZ_lepton1_eta",
        "axis_name":"#eta_{W}",
        "xbins":6,
        "xleft":-2.5,
        "xright":2.5,
    },
    "ttZ_lepton2_pt":{
        "name":"ttZ_lepton2_pt",
        "axis_name":"P_{T, Z1} [GeV]",
        "xbins":10,
        "xleft":0,
        "xright":200,
    },
    "ttZ_lepton2_eta":{
        "name":"ttZ_lepton2_eta",
        "axis_name":"#eta_{Z1}",
        "xbins":6,
        "xleft":-2.5,
        "xright":2.5,
    },
    "MET":{
        "name":"MET",
        "axis_name":"MET [GeV]",
        "xbins":10,
        "xleft":30,
        "xright":120,
    },
    "nJets":{
        "name":"nJets",
        "axis_name":"nJets",
        "xbins":8,
        "xleft":0,
        "xright":8,
    },
    "nbJets":{
        "name":"nbJets",
        "axis_name":"nbJets",
        "xbins":8,
        "xleft":0,
        "xright":8,
    }
}

filelist_data = [
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2017/SingleMuon_Run2017B_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2017/SingleMuon_Run2017C_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2017/SingleMuon_Run2017D_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2017/SingleMuon_Run2017E_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2017/SingleMuon_Run2017F_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2017/DoubleMuon_Run2017B_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2017/DoubleMuon_Run2017C_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2017/DoubleMuon_Run2017D_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2017/DoubleMuon_Run2017E_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2017/DoubleMuon_Run2017F_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2017/SingleElectron_Run2017B_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2017/SingleElectron_Run2017C_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2017/SingleElectron_Run2017D_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2017/SingleElectron_Run2017E_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2017/SingleElectron_Run2017F_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2017/DoubleEG_Run2017B_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2017/DoubleEG_Run2017C_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2017/DoubleEG_Run2017D_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2017/DoubleEG_Run2017E_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2017/DoubleEG_Run2017F_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2017/MuonEG_Run2017B_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2017/MuonEG_Run2017C_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2017/MuonEG_Run2017D_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2017/MuonEG_Run2017E_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2017/MuonEG_Run2017F_0000.root",
]

filelist_MC = {
    "TTG":
            {"name":"TTGJets", 
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2017/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_2017_0000.root", 
            "xsec":3.697,
            "color":3},
    "TTZ":
            {"name":"TTZToLLNuNu", 
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2017/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8_2017_0000.root", 
            "xsec":0.2529,
            "color":4},
    "TTW":
            {"name":"TTWJetsToLNu", 
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2017/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_2017_0000.root", 
            "xsec":0.2043,
            "color":5},
    "tZq":
            {"name":"tZq_ll", 
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2017/tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8_2017_0000.root", 
            "xsec":0.07358,
            "color":6},
    "WWW":
            {"name":"WWW", 
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2017/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8_2017_0000.root", 
            "xsec":0.2086,
            "color":7},
    "WZ":
            {"name":"WZ", 
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2017/WZ_TuneCP5_13TeV-pythia8_2017_0000.root", 
            "xsec":47.13,
            "color":8},
    "ZGToLLG":
            {"name":"ZGToLLG",
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2017/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8_2017_0000.root", 
            "xsec":55.48,
            "color":9},
        "qqZZ":
            {"name":"qqZZ",
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2017/ZZ_TuneCP5_13TeV-pythia8_2017_0000.root",
            "xsec":16.523,
            "color":12},
        "ggZZ_2e2mu":
            {"name":"ggZZ_2e2mu",
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2017/GluGluToContinToZZTo2e2mu_TuneCP5_13TeV-mcfm701-pythia8_2017_0000.root",
            "xsec":0.00319,
            "color":13},
        "ggZZ_2e2nu":
            {"name":"ggZZ_2e2nu",
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2017/GluGluToContinToZZTo2e2nu_TuneCP5_13TeV-mcfm701-pythia8_2017_0000.root",
            "xsec":0.00319,
            "color":13},
        "ggZZ_2e2tau":
            {"name":"ggZZ_2e2tau",
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2017/GluGluToContinToZZTo2e2tau_TuneCP5_13TeV-mcfm701-pythia8_2017_0000.root",
            "xsec":0.00319,
            "color":13},
        "ggZZ_2mu2nu":
            {"name":"ggZZ_2mu2nu",
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2017/GluGluToContinToZZTo2mu2nu_TuneCP5_13TeV-mcfm701-pythia8_2017_0000.root",
            "xsec":0.00319,
            "color":13},
        "ggZZ_2mu2tau":
            {"name":"ggZZ_2mu2tau",
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2017/GluGluToContinToZZTo2mu2tau_TuneCP5_13TeV-mcfm701-pythia8_2017_0000.root",
            "xsec":0.00319,
            "color":13},
        "ggZZ_4e":
            {"name":"ggZZ_4e",
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2017/GluGluToContinToZZTo4e_TuneCP5_13TeV-mcfm701-pythia8_2017_0000.root",
            "xsec":0.00159,
            "color":13},
        "ggZZ_4mu":
            {"name":"ggZZ_4mu",
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2017/GluGluToContinToZZTo4mu_TuneCP5_13TeV-mcfm701-pythia8_2017_0000.root",
            "xsec":0.00159,
            "color":13},
        "ggZZ_4tau":
            {"name":"ggZZ_4tau",
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2017/GluGluToContinToZZTo4tau_TuneCP5_13TeV-mcfm701-pythia8_2017_0000.root",
            "xsec":0.00159,
            "color":13},
        "WZG":
            {"name":"WZG",
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2017/wza_UL17_sum_Skim.root",
            "xsec":0.0384,
            "color":38}
    }

filelist_data_FakeLep = [
    "/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/SingleMuon_Run2017B_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/SingleMuon_Run2017C_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/SingleMuon_Run2017D_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/SingleMuon_Run2017E_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/SingleMuon_Run2017F_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/DoubleMuon_Run2017B_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/DoubleMuon_Run2017C_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/DoubleMuon_Run2017D_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/DoubleMuon_Run2017E_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/DoubleMuon_Run2017F_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/SingleElectron_Run2017B_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/SingleElectron_Run2017C_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/SingleElectron_Run2017D_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/SingleElectron_Run2017E_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/SingleElectron_Run2017F_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/DoubleEG_Run2017B_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/DoubleEG_Run2017C_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/DoubleEG_Run2017D_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/DoubleEG_Run2017E_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/DoubleEG_Run2017F_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/MuonEG_Run2017B_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/MuonEG_Run2017C_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/MuonEG_Run2017D_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/MuonEG_Run2017E_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/MuonEG_Run2017F_0000_Skim.root",
]

filelist_MC_FakeLep = {
   "TTG":
        {"name":"TTGJets", 
        "path":"/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_2017_0000_Skim.root", 
        "xsec":3.697,
        "color":3},
   "TTZ":
        {"name":"TTZToLLNuNu", 
        "path":"/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8_2017_0000_Skim.root", 
        "xsec":0.2529,
        "color":4},
   "TTW":
        {"name":"TTWJetsToLNu", 
        "path":"/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_2017_0000_Skim.root", 
        "xsec":0.2043,
        "color":5},
   "tZq":
        {"name":"tZq_ll", 
        "path":"/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8_2017_0000_Skim.root", 
        "xsec":0.0758,
        "color":6},
   "WWW":
        {"name":"WWW", 
        "path":"/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8_2017_0000_Skim.root", 
        "xsec":0.2086,
        "color":7},
   "WZ":
        {"name":"WZ", 
        "path":"/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/WZ_TuneCP5_13TeV-pythia8_2017_0000_Skim.root", 
        "xsec":47.13,
        "color":8},
   "ZGToLLG":
        {"name":"ZGToLLG",
        "path":"/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8_2017_0000_Skim.root", 
        "xsec":55.48,
        "color":9},
    "qqZZ":
        {"name":"qqZZ",
        "path":"/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/ZZ_TuneCP5_13TeV-pythia8_2017_0000_Skim.root", 
        "xsec":16.523,
        "color":12},
    "ggZZ_2e2mu":
        {"name":"ggZZ_2e2mu",
        "path":"/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/GluGluToContinToZZTo2e2mu_TuneCP5_13TeV-mcfm701-pythia8_2017_0000_Skim.root",
        "xsec":0.00319,
        "color":13},
    "ggZZ_2e2nu":
        {"name":"ggZZ_2e2nu",
        "path":"/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/GluGluToContinToZZTo2e2nu_TuneCP5_13TeV-mcfm701-pythia8_2017_0000_Skim.root",
        "xsec":0.00319,
        "color":13},
    "ggZZ_2e2tau":
        {"name":"ggZZ_2e2tau",
        "path":"/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/GluGluToContinToZZTo2e2tau_TuneCP5_13TeV-mcfm701-pythia8_2017_0000_Skim.root",
        "xsec":0.00319,
        "color":13},
    "ggZZ_2mu2nu":
        {"name":"ggZZ_2mu2nu",
        "path":"/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/GluGluToContinToZZTo2mu2nu_TuneCP5_13TeV-mcfm701-pythia8_2017_0000_Skim.root",
        "xsec":0.00319,
        "color":13},
    "ggZZ_2mu2tau":
        {"name":"ggZZ_2mu2tau",
        "path":"/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/GluGluToContinToZZTo2mu2tau_TuneCP5_13TeV-mcfm701-pythia8_2017_0000_Skim.root",
        "xsec":0.00319,
        "color":13},
    "ggZZ_4e":
        {"name":"ggZZ_4e",
        "path":"/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/GluGluToContinToZZTo4e_TuneCP5_13TeV-mcfm701-pythia8_2017_0000_Skim.root",
        "xsec":0.00159,
        "color":13},
    "ggZZ_4mu":
        {"name":"ggZZ_4mu",
        "path":"/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/GluGluToContinToZZTo4mu_TuneCP5_13TeV-mcfm701-pythia8_2017_0000_Skim.root",
        "xsec":0.00159,
        "color":13},
    "ggZZ_4tau":
        {"name":"ggZZ_4tau",
        "path":"/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/GluGluToContinToZZTo4tau_TuneCP5_13TeV-mcfm701-pythia8_2017_0000_Skim.root",
        "xsec":0.00159,
        "color":13},
    "WZG":
        {"name":"signal",
        "path":"/eos/user/s/sdeng/WZG_analysis/fake_lepton_template/AR/2017/final/wza_UL17_sum_Skim_Skim.root", 
        "xsec":0.0384,
        "color":21}
}

filelist_data_FakePho= [
    "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/SingleMuon_Run2017B_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/SingleMuon_Run2017C_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/SingleMuon_Run2017D_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/SingleMuon_Run2017E_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/SingleMuon_Run2017F_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/DoubleMuon_Run2017B_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/DoubleMuon_Run2017C_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/DoubleMuon_Run2017D_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/DoubleMuon_Run2017E_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/DoubleMuon_Run2017F_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/SingleElectron_Run2017B_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/SingleElectron_Run2017C_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/SingleElectron_Run2017D_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/SingleElectron_Run2017E_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/SingleElectron_Run2017F_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/DoubleEG_Run2017B_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/DoubleEG_Run2017C_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/DoubleEG_Run2017D_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/DoubleEG_Run2017E_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/DoubleEG_Run2017F_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/MuonEG_Run2017B_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/MuonEG_Run2017C_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/MuonEG_Run2017D_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/MuonEG_Run2017E_0000_Skim.root",
    "/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/MuonEG_Run2017F_0000_Skim.root",
]

filelist_MC_FakePho = {
"TTG":
        {"name":"TTGJets", 
        "path":"/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_2017_0000_Skim.root", 
        "xsec":3.697,
        "color":3},
"TTZ":
        {"name":"TTZToLLNuNu", 
        "path":"/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8_2017_0000_Skim.root", 
        "xsec":0.2529,
        "color":4},
"TTW":
        {"name":"TTWJetsToLNu", 
        "path":"/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_2017_0000_Skim.root", 
        "xsec":0.2043,
        "color":5},
"tZq":
        {"name":"tZq_ll", 
        "path":"/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8_2017_0000_Skim.root", 
        "xsec":0.0758,
        "color":6},
"WWW":
        {"name":"WWW", 
        "path":"/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8_2017_0000_Skim.root", 
        "xsec":0.2086,
        "color":7},
#    "WZ":
#         {"name":"WZ", 
#         "path":"/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/WZ_TuneCP5_13TeV-pythia8_2017_0000_Skim.root", 
#         "xsec":47.13,
#         "color":8},
"ZGToLLG":
        {"name":"ZGToLLG",
        "path":"/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8_2017_0000_Skim.root", 
        "xsec":55.48,
        "color":9},
    "qqZZ":
        {"name":"qqZZ",
        "path":"/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/ZZ_TuneCP5_13TeV-pythia8_2017_0000_Skim.root", 
        "xsec":16.523,
        "color":12},
    "WZG":
        {"name":"signal",
        "path":"/eos/user/s/sdeng/WZG_analysis/fake_photon_template/AR/2017/final/wza_UL17_sum_Skim_Skim.root", 
        "xsec":0.0384,
        "color":21}
}
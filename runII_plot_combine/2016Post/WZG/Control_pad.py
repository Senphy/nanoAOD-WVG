channel = 0
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

lumi = 16.8
year = "2016Post"

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
    "channel_mark":{
        "name":"channel_mark",
        "axis_name":"channel",
        "bin_array":[1,2,3,4,5],
    },
    "mwa":{
        "name":"mwa",
        "axis_name":"m_{l_{W}#gamma} [GeV]",
        "bin_strategy":"average",
        "xbins":10,
        "xleft":0,
        "xright":200,
    },
    "WZG_dileptonmass":{
        "name":"WZG_dileptonmass",
        "axis_name":"m_{Z} [GeV]",
        "bin_strategy":"average",
        "xbins":5,
        "xleft":75,
        "xright":105,
    },
    "WZG_trileptonmass":{
        "name":"WZG_trileptonmass",
        "axis_name":"m_{lll} [GeV]",
        "bin_array":[100,200,500],
    },
    "WZG_mlla":{
        "name":"WZG_mlla",
        "axis_name":"m_{ll#gamma} [GeV]",
        "bin_array":[80,150,500],
    },
    "WZG_lepton1_pt":{
        "name":"WZG_lepton1_pt",
        "axis_name":"P_{T, W} [GeV]",
        "xbins":10,
        "xleft":0,
        "xright":200,
    },
    "WZG_lepton1_eta":{
        "name":"WZG_lepton1_eta",
        "axis_name":"|#eta_{W}|",
        "xbins":6,
        "xleft":-2.5,
        "xright":2.5,
    },
    "WZG_lepton2_pt":{
        "name":"WZG_lepton2_pt",
        "axis_name":"P_{T, Z1} [GeV]",
        "xbins":10,
        "xleft":0,
        "xright":200,
    },
    "WZG_lepton2_eta":{
        "name":"WZG_lepton2_eta",
        "axis_name":"|#eta_{Z1}|",
        "xbins":6,
        "xleft":-2.5,
        "xright":2.5,
    },
    "WZG_photon_pt":{
        "name":"WZG_photon_pt",
        "axis_name":"P_{T, #gamma} [GeV]",
        "xbins":10,
        "xleft":0,
        "xright":200,
    },
    "WZG_photon_eta":{
        "name":"WZG_photon_eta",
        "axis_name":"|#eta_{#gamma}|",
        "xbins":6,
        "xleft":-2.5,
        "xright":2.5,
    },
    "MET":{
        "name":"MET",
        "axis_name":"MET [GeV]",
        "xbins":5,
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
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/SingleMuon_Run2016F_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/SingleMuon_Run2016G_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/SingleMuon_Run2016H_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/DoubleMuon_Run2016F_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/DoubleMuon_Run2016G_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/DoubleMuon_Run2016H_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/SingleElectron_Run2016F_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/SingleElectron_Run2016G_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/SingleElectron_Run2016H_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/DoubleEG_Run2016F_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/DoubleEG_Run2016G_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/DoubleEG_Run2016H_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/MuonEG_Run2016F_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/MuonEG_Run2016G_0000.root",
    "/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/MuonEG_Run2016H_0000.root",
]

filelist_MC = {
    "TTG":
            {"name":"TTGJets", 
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_2016Post_0000.root", 
            "xsec":3.697,
            "color":3},
    "TTZLLNuNu":
            {"name":"TTZToLLNuNu", 
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8_2016Post_0000.root", 
            "xsec":0.2529,
            "color":4},
    "TTZLL":
            {"name":"TTZToLL", 
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8_2016Post_0000.root", 
            "xsec":0.05324,
            "color":44},
    "TTW":
            {"name":"TTWJetsToLNu", 
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_2016Post_0000.root", 
            "xsec":0.2043,
            "color":5},
    "TTTT":
            {"name":"TTTT", 
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/TTTT_TuneCP5_13TeV-amcatnlo-pythia8_2016Post_0000.root", 
            "xsec":0.008213,
            "color":45},
    "tZq":
            {"name":"tZq_ll", 
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8_2016Post_0000.root", 
            "xsec":0.07358,
            "color":6},
    "sT":
            {"name":"sT top", 
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/ST_tW_top_5f_DS_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8_2016Post_0000.root", 
            "xsec":33.67,
            "color":46},
    "sT_anti":
            {"name":"sT antitop", 
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/ST_tW_antitop_5f_DS_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8_2016Post_0000.root", 
            "xsec":35.13,
            "color":46},
    "WWW":
            {"name":"WWW", 
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8_2016Post_0000.root", 
            "xsec":0.2086,
            "color":7},
    "WWZ":
            {"name":"WWZ", 
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8_2016Post_0000.root", 
            "xsec":0.1707,
            "color":47},
    #    "WZ":
    #         {"name":"WZ", 
    #         "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/WZ_TuneCP5_13TeV-pythia8_2016Post_0000.root", 
    #         "xsec":47.13,
    #         "color":8},
    "ZGToLLG":
            {"name":"ZGToLLG",
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8_2016Post_0000.root", 
            "xsec":55.48,
            "color":9},
    "WG":
            {"name":"WGToLNuG",
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/WGToLNuG_01J_5f_PDFWeights_TuneCP5_13TeV-amcatnloFXFX-pythia8_2016Post_0000.root", 
            "xsec":190.8,
            "color":39},
        "qqZZ":
            {"name":"qqZZ",
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/ZZTo4L_TuneCP5_13TeV_powheg_pythia8_2016Post_0000.root",
            "xsec":1.325,
            "color":12},
        "ggZZ_2e2mu":
            {"name":"ggZZ_2e2mu",
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/GluGluToContinToZZTo2e2mu_TuneCP5_13TeV-mcfm701-pythia8_2016Post_0000.root",
            "xsec":0.00319,
            "color":13},
        # "ggZZ_2e2nu":
        #     {"name":"ggZZ_2e2nu",
        #     "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/GluGluToContinToZZTo2e2nu_TuneCP5_13TeV-mcfm701-pythia8_2016Post_0000.root",
        #     "xsec":0.00319,
        #     "color":13},
        "ggZZ_2e2tau":
            {"name":"ggZZ_2e2tau",
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/GluGluToContinToZZTo2e2tau_TuneCP5_13TeV-mcfm701-pythia8_2016Post_0000.root",
            "xsec":0.00319,
            "color":13},
        "ggZZ_2mu2nu":
            {"name":"ggZZ_2mu2nu",
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/GluGluToContinToZZTo2mu2nu_TuneCP5_13TeV-mcfm701-pythia8_2016Post_0000.root",
            "xsec":0.00319,
            "color":13},
        "ggZZ_2mu2tau":
            {"name":"ggZZ_2mu2tau",
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/GluGluToContinToZZTo2mu2tau_TuneCP5_13TeV-mcfm701-pythia8_2016Post_0000.root",
            "xsec":0.00319,
            "color":13},
        "ggZZ_4e":
            {"name":"ggZZ_4e",
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/GluGluToContinToZZTo4e_TuneCP5_13TeV-mcfm701-pythia8_2016Post_0000.root",
            "xsec":0.00159,
            "color":13},
        "ggZZ_4mu":
            {"name":"ggZZ_4mu",
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/GluGluToContinToZZTo4mu_TuneCP5_13TeV-mcfm701-pythia8_2016Post_0000.root",
            "xsec":0.00159,
            "color":13},
        "ggZZ_4tau":
            {"name":"ggZZ_4tau",
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/GluGluToContinToZZTo4tau_TuneCP5_13TeV-mcfm701-pythia8_2016Post_0000.root",
            "xsec":0.00159,
            "color":13},
        "WZG":
            {"name":"WZG",
            "path":"/eos/user/s/sdeng/WZG_analysis/final_skim/2016Post/LLWA_WToLNu_4FS_TuneCP5_13TeV-amcatnlo-pythia8_2016Post_0000.root",
            "xsec":0.0384,
            "color":38}
    }
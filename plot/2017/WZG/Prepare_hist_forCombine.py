import os,sys
import ROOT

from Control_pad import channel_map
from Control_pad import channel
from Control_pad import UpDown_map
from Control_pad import filelist_MC
from Control_pad import branch
from Control_pad import year

if __name__ == '__main__':

    Top_list = ["TTGJets", "TTZToLLNuNu", "TTWJetsToLNu", "tZq_ll"]
    VVV_list = ["WWW","WWZ","ZZZ","WZZ"]
    VV_list = ["qqZZ","ggZZ","WZ","ZGToLLG"]
    index_list = ["None", "jesTotalUp", "jesTotalDown", "jerUp", "jerDown", "MuonIDup", "MuonIDdown", "ElectronIDup", "ElectronIDdown", "ElectronRECOup", "ElectronRECOdown"]

    
    try:
        file_hist = ROOT.TFile(f'./test/{channel_map[channel]}.root',"OPEN")
    except:
        print ("nonvalid root file")
        sys.exit(0)

    new_file_hist = ROOT.TFile(f'./{channel_map[channel]}_{year}.root',"RECREATE")
    new_file_hist.cd()

    # Merge hist
    for index in index_list:

        for branch_name in branch:

            hist_Top_list = []
            hist_VVV_list = []
            hist_VV_list = []
            hist_WZG_list = []
            plot_branch = branch[branch_name]["name"]

            for file in filelist_MC:
                # print(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{index}')
                hist_temp = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{index}')
                # print(type(hist_temp))

                if filelist_MC[file]["name"] in Top_list:
                    hist_Top_list.append(hist_temp)

                elif filelist_MC[file]["name"] in VVV_list:
                    hist_VVV_list.append(hist_temp)

                elif filelist_MC[file]["name"] in VV_list or 'ggZZ' in filelist_MC[file]["name"] or 'qqZZ' in filelist_MC[file]["name"]:
                    hist_VV_list.append(hist_temp)
                
                elif 'WZG' in filelist_MC[file]["name"]:
                    hist_WZG_list.append(hist_temp)

            if len(hist_Top_list) > 0:
                hist_Top = hist_Top_list[0].Clone()
                for i in range(1, len(hist_Top_list)):
                    hist_Top.Add(hist_Top_list[i])
                hist_Top.SetName(f'{channel_map[channel]}_{plot_branch}_Top_{index}')
                hist_Top.Write()

            if len(hist_VVV_list) > 0:
                hist_VVV = hist_VVV_list[0].Clone()
                for i in range(1, len(hist_VVV_list)):
                    hist_VVV.Add(hist_VVV_list[i])
                hist_VVV.SetName(f'{channel_map[channel]}_{plot_branch}_VVV_{index}')
                hist_VVV.Write()

            if len(hist_VV_list) > 0:
                hist_VV = hist_VV_list[0].Clone()
                for i in range(1, len(hist_VV_list)):
                    hist_VV.Add(hist_VV_list[i])
                hist_VV.SetName(f'{channel_map[channel]}_{plot_branch}_VV_{index}')
                hist_VV.Write()

            if len(hist_WZG_list) == 0:
                print('!!!Warning: No signal input!!!')
            else:
                hist_WZG = hist_WZG_list[0].Clone()
                if len(hist_WZG_list) > 1:
                    print('!!!Warning: More than 1 signal input!!!')
                    for i in range(1, len(hist_WZG_list)):
                        hist_WZG.Add(hist_WZG_list[i])
                hist_WZG.SetName(f'{channel_map[channel]}_{plot_branch}_WZG_{index}')
                hist_WZG.Write()

    for branch_name in branch:
        plot_branch = branch[branch_name]["name"]
        hist_data = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_data_None')
        hist_data.SetName(f'{channel_map[channel]}_{plot_branch}_data_None')
        hist_data.Write()

        hist_FakeLep = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_FakeLep_None')
        hist_FakeLep.SetName(f'{channel_map[channel]}_{plot_branch}_FakeLep_None')
        hist_FakeLep.Write()

        hist_FakePho = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_FakePho_None')
        hist_FakePho.SetName(f'{channel_map[channel]}_{plot_branch}_FakePho_None')
        hist_FakePho.Write()

    new_file_hist.Close()
    file_hist.Close()
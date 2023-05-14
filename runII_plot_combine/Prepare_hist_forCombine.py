import os,sys
import ROOT
import argparse

sys.path.append(os.getcwd())
from AddHist_help import unc_map 

parser = argparse.ArgumentParser(description='plot input')
parser.add_argument('-y', dest='year', default='2018', choices=['2016Pre','2016Post','2017','2018'])
parser.add_argument('-r', dest='region', choices=['ttZ','ZZ','ZGJ','WZG'], default='ttZ')
parser.add_argument('-m', dest='mode', choices=['local','condor'], default='local')
args = parser.parse_args()

def corr_suffix(year):
    if year == '2018':
        return '18'
    elif year == '2017':
        return 17
    elif year == '2016Pre' or '2016Post':
        return 16

if __name__ == '__main__':

    year = args.year
    region = args.region
    sys.path.append(f'./{year}/{region}')
    from Control_pad import channel_map
    from Control_pad import channel
    from Control_pad import UpDown_map
    from Control_pad import filelist_MC
    from Control_pad import branch
    from Control_pad import year

    Top_list = ["ttgjets", "ttztollnunu", "ttztoll", "ttwjetstolnu", "tttt", "tZq_ll", "st antitop", "st top"]
    VVV_list = ["www","wwz","zzz","wzz"]
    VV_list = ["qqzz","ggzz","wz"]
    VG_list = ["zgtollg","wgtolnug"]
    index_list = ["None"]
    for unc in unc_map:
        if unc_map[unc]['corr'] != None:
            index_list.append(f'{unc}Up_{corr_suffix(year)}')
            index_list.append(f'{unc}Down_{corr_suffix(year)}')
        else:
            index_list.append(f'{unc}Up')
            index_list.append(f'{unc}Down')
    index_list.extend(["jesTotalUp", "jesTotalDown", "jerUp", "jerDown"])
    print(index_list)

    
    try:
        file_hist = ROOT.TFile(f'./{year}/{channel_map[channel]}_{year}.root',"OPEN")
    except:
        print ("nonvalid root file")
        sys.exit(0)

    new_file_hist = ROOT.TFile(f'./{year}/{channel_map[channel]}_combine_{year}.root',"RECREATE")
    new_file_hist.cd()

    # Merge hist
    for index in index_list:

        for branch_name in branch:

            hist_Top_list = []
            hist_VVV_list = []
            hist_VV_list = []
            hist_VG_list = []
            hist_WZG_list = []
            plot_branch = branch[branch_name]["name"]

            for file in filelist_MC:
                # print(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{index}')
                hist_temp = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{index}')
                # print(type(hist_temp))

                if filelist_MC[file]["name"].lower() in Top_list:
                    hist_Top_list.append(hist_temp)

                elif filelist_MC[file]["name"].lower() in VVV_list:
                    hist_VVV_list.append(hist_temp)

                elif filelist_MC[file]["name"].lower() in VV_list or 'ggZZ' in filelist_MC[file]["name"] or 'qqZZ' in filelist_MC[file]["name"]:
                    hist_VV_list.append(hist_temp)
                
                elif filelist_MC[file]["name"].lower() in VG_list:
                    hist_VG_list.append(hist_temp)

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

            if len(hist_VG_list) > 0:
                hist_VG = hist_VG_list[0].Clone()
                for i in range(1, len(hist_VG_list)):
                    hist_VG.Add(hist_VG_list[i])
                hist_VG.SetName(f'{channel_map[channel]}_{plot_branch}_VG_{index}')
                hist_VG.Write()

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
        hist_data.SetName(f'{channel_map[channel]}_{plot_branch}_data_obs_None')
        hist_data.Write()

        hist_FakeLep = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_FakeLep_None')
        hist_FakeLep.SetName(f'{channel_map[channel]}_{plot_branch}_FakeLep_None')
        hist_FakeLep.Write()

        hist_FakePho = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_FakePho_None')
        hist_FakePho.SetName(f'{channel_map[channel]}_{plot_branch}_FakePho_None')
        hist_FakePho.Write()

    new_file_hist.Close()
    file_hist.Close()
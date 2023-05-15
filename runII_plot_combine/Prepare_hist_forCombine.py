import os,sys
import ROOT
import argparse
from copy import deepcopy

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

def GetUnc():
    pass
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

    index_list = deepcopy(unc_map)
    index_list['jesTotal'] = {}
    index_list['jer'] = {}
    index_list['jesTotal']['corr'] = None
    index_list['jer']['corr'] = None
    print(unc_map)

    hist_list_sample = {
        "VV":{
            "name":["qqzz","ggzz","wz"],
        },
        "VG":{  
            "name":["zgtollg","wgtolnug"],
        },
        "VVV":{
            "name":["www","wwz","zzz","wzz"],
        },
        "Top":{
            "name":["ttgjets", "ttztollnunu", "ttztoll", "ttwjetstolnu", "tttt", "tZq_ll", "st antitop", "st top"],
        },
        "WZG":{
            "name":["wzg"],
        },
    }
    
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
            hist_list = deepcopy(hist_list_sample)

            plot_branch = branch[branch_name]["name"]

            for cate in hist_list:
                hist_list[cate]["hists_up"] = []
                hist_list[cate]["hists_down"] = []
            for file in filelist_MC:
                # print(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{index}')
                hist_temp_up = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{index}Up')
                hist_temp_down = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_{index}Down')
                # print(type(hist_temp))

                for cate in hist_list:
                    if filelist_MC[file]["name"].lower() in hist_list[cate]["name"]:
                        hist_list[cate]["hists_up"].append(hist_temp_up)
                        hist_list[cate]["hists_down"].append(hist_temp_down)

            # hist_list[cate]['final_hist']
            # for cate in hist_list:
            #     if len(hist_list[cate]["hists"]) > 0:
            #         for i in range(0, len(hist_list[cate]["hists"])):
            #             hist_temp_up.Add(hist_list[cate]["hists_up"][i])
            #             hist_temp_down.Add(hist_list[cate]["hists_up"][i])
            #         hist_temp
            for cate in hist_list:
                if len(hist_list[cate]["hists_up"]) == 0:
                    hist_temp_up = ROOT.TH1D()
                    hist_temp_down= ROOT.TH1D()
                else:
                    hist_temp_up = hist_list[cate]["hists_up"][0].Clone()
                    hist_temp_down = hist_list[cate]["hists_down"][0].Clone()
                    for i in range(1,len(hist_list[cate]["hists_up"])):
                        hist_temp_up.Add(hist_list[cate]["hists_up"][i])
                        hist_temp_down.Add(hist_list[cate]["hists_down"][i])

                if index_list[index]['corr'] != None:
                    hist_temp_up.SetName(f'{channel_map[channel]}_{plot_branch}_{cate}_{index}Up')
                    hist_temp_up.Write()
                    hist_temp_down.SetName(f'{channel_map[channel]}_{plot_branch}_{cate}_{index}Down')
                    hist_temp_down.Write()
                else:
                    hist_temp_up.SetName(f'{channel_map[channel]}_{plot_branch}_{cate}_{index}_{corr_suffix(year)}Up')
                    hist_temp_up.Write()
                    hist_temp_down.SetName(f'{channel_map[channel]}_{plot_branch}_{cate}_{index}_{corr_suffix(year)}Down')
                    hist_temp_down.Write()


            # if len(hist_VG_list) > 0:
            #     hist_VG = hist_VG_list[0].Clone()
            #     for i in range(1, len(hist_VG_list)):
            #         hist_VG.Add(hist_VG_list[i])
            #     hist_VG.SetName(f'{channel_map[channel]}_{plot_branch}_VG_{index}')
            #     hist_VG.Write()

            del hist_list

    for branch_name in branch:
        hist_list = deepcopy(hist_list_sample)
        plot_branch = branch[branch_name]["name"]
        for cate in hist_list:
            hist_list[cate]["hists_None"] = []
        for file in filelist_MC:
            hist_temp = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_{filelist_MC[file]["name"]}_None')
            for cate in hist_list:
                if filelist_MC[file]["name"].lower() in hist_list[cate]["name"]:
                    hist_list[cate]["hists_None"].append(hist_temp)
        for cate in hist_list:
            del hist_temp
            if len(hist_list[cate]["hists_None"]) == 0:
                hist_temp = ROOT.TH1D()
            else:
                hist_temp = hist_list[cate]["hists_None"][0].Clone()
                for i in range(1,len(hist_list[cate]["hists_None"])):
                    hist_temp.Add(hist_list[cate]["hists_None"][i])
            hist_temp.SetName(f'{channel_map[channel]}_{plot_branch}_{cate}_None')
            hist_temp.Write()
        del hist_list
            
        hist_data = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_data_None')
        hist_data.SetName(f'{channel_map[channel]}_{plot_branch}_data_obs_None')
        hist_data.Write()

        hist_FakeLep = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_FakeLep_None')
        hist_FakeLep.SetName(f'{channel_map[channel]}_{plot_branch}_FakeLep_None')
        hist_FakeLep.Write()
        for suffix in ['Up','Down']:
            hist_FakeLep = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_FakeLep_fakerate{suffix}')
            hist_FakeLep.SetName(f'{channel_map[channel]}_{plot_branch}_FakeLep_fakerate_{corr_suffix(year)}{suffix}')
            hist_FakeLep.Write()

        hist_FakePho = file_hist.Get(f'{channel_map[channel]}_{plot_branch}_FakePho_None')
        hist_FakePho.SetName(f'{channel_map[channel]}_{plot_branch}_FakePho_None')
        hist_FakePho.Write()

    new_file_hist.Close()
    file_hist.Close()
import os,sys
import argparse

parser = argparse.ArgumentParser(description="merge log")
parser.add_argument('-f', dest='file', default='', help='file path')

def merge_log(path):

    MET_pass    =  0 
    muon_pass   =   0
    electron_pass   =   0
    photon_pass     =   0

    none_photon_reject  =   0
    none_lepton_reject  =   0
    none_3lepton_reject     =   0
    same_charge_reject_eee  =   0
    same_charge_reject_mumumu   =   0

    emumu_pass  =   0
    muee_pass   =   0
    eee_pass    =   0
    mumumu_pass     =   0
    btagjet_reject  =   0

    total = 0

    list = ['MET_pass', 'muon_pass', 'electron_pass', 'photon_pass', 'none_photon_reject', 'none_lepton_reject', 'none_3lepton_reject', 'same_charge_reject_eee',\
            'same_charge_reject_mumumu', 'emumu_pass', 'muee_pass', 'eee_pass', 'mumumu_pass', 'btagjet_reject', 'total']

    list_value = []
    
    merge = []

    for i in range(0,len(list)):
        list_value.append(0)


    for filename in os.listdir(path+"/log/"):

        if not filename.endswith(".output"):
            continue

        with open(path+"log/"+filename,"r") as f:
            
            valid = f.read()
            if not 'pass' in valid:
                print filename," corrupted, skipping"
                continue

            f.seek(0,0)
            lines = f.readlines()
            for line in lines:
                line = line.rstrip("\n")
                if (not 'pass' in line) and (not 'reject' in line) and (not 'total' in line):
                    pass

                else: 
                    for j in list:
                        if j in line:
                            # print int(line.split('=')[1].strip())
                            list_value[list.index(j)] += int(line.split('=')[1].strip()) 
                        

            f.close()
        
        merge.append(filename)
        print filename, " merged"
    

    with open(path + path.rstrip('/') + '_merge.log','w+') as f:
        for j in range(0,len(list)):
            f.write(list[j] + '\t=\t' + str(list_value[j]) + '\n')

        for j in merge:
            f.write(j + " merged\n") 
        
        f.write("total " + str(len(merge)) + " files merged")

        f.close()



    print "total ",len(merge)," files merged"



if __name__ == '__main__':
    # print parser.parse_args().file
    merge_log(parser.parse_args().file)
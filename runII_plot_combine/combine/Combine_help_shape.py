#! /bin/python3
import sys,os
import uproot
import json
import argparse
import pandas as pd
from decimal import Decimal
import shutil
import logging

parser = argparse.ArgumentParser(description='prepare combined cards')
parser.add_argument('-f', dest='file', default='./test.json', help='input json with configuration')
parser.add_argument('-o', dest='output_card', default='test18', help='output card name')
args = parser.parse_args()

class region_combine():

    def __init__(self, config_json=None, utils=None, **kwargs):
        self.jsons = config_json
        self.imax = int(utils['imax'])
        self.autoMCStats_threshold = int(utils['autoMCStats_threshold'])

        self.file_name= self.jsons['file_name']
        self.region_name = self.jsons['region_name']
        self.region_plotname = self.jsons['final_name']
        self.tag = utils['tag']
        self.variable = self.jsons['variable']
        self.variable_plotname = self.jsons['variable_plotname']

        self.df_unc = pd.read_csv(self.jsons['csv'])
        self.processes = []
        self.processes_abrev = []
        self.printlength = max(len(self.file_name), len(self.region_name))
        self.printlength = max(self.printlength, 30)

        for process in self.df_unc.columns:
            # skip type and uncertainty columns
            if ('type' in process) or ('uncertainty' in process):
                continue
            self.processes.append(f'{self.region_name}_{self.variable}_{process}_None')
            self.processes_abrev.append(f'{process}')
            self.printlength = max(self.printlength, len(process))
        self.df_nominal = uproot.open(f'store/{self.file_name}')

    def cal_ijk(self, f):
        self.jmax = len(self.processes)-1
        self.kmax = len(self.df_unc.index)
        f.write(f'imax\t{str(self.imax)}\n')
        f.write(f'jmax\t{str(self.jmax)}\n')
        f.write(f'kmax\t{str(self.kmax)}\n')
        f.write('----------\n')

    def cal_shape_input(self, f):
        #*FIXME* Only support one shape source currently#
        # shapes [process] [channel] [file] [histogram] [histogram_with_systematics]
        shape_string = f'shapes * {self.region_plotname} store/{self.file_name} {self.region_name}_{self.variable}_$PROCESS_None {self.region_name}_{self.variable}_$PROCESS_$SYSTEMATIC'
        f.write(f'{shape_string}\n')
        f.write('----------\n')

    def cal_observation(self, f):
        bin_string = f'bin \t {self.region_plotname}'
        self.obs = 0
        self.rate = []
        for process in self.processes:
            temp_sum = self.df_nominal[f'{process}'].to_hist().sum()
            if type(temp_sum) == float:
                self.rate.append(temp_sum)
                self.obs += temp_sum
            else:
                self.rate.append(temp_sum.value)
                self.obs += temp_sum.value
        # obs_string = f'observation \t {str(Decimal(str(self.obs)).quantize(Decimal("0.001")))}'
        obs_string = f'observation \t -1'
        f.write(f'{bin_string}\n')
        f.write(f'{obs_string}\n')
        f.write('----------\n')

    def cal_rate(self, f):
        bin_string = 'bin '.ljust(self.printlength)
        process_string = 'process'.ljust(self.printlength)
        process_string2 = 'process '.ljust(self.printlength)
        rate_string = 'rate '.ljust(self.printlength)
        for n, process in enumerate(self.processes_abrev):
            bin_string += f'{self.region_plotname.ljust(self.printlength)}'
            process_string += f'{process.ljust(self.printlength)}'
            process_string2 += f'{str(n).ljust(self.printlength)}'
            rate_string += f'{str(Decimal(str(self.rate[n])).quantize(Decimal("0.001"))).ljust(self.printlength)}'
        f.write(f'{bin_string}\n')
        f.write(f'{process_string}\n')
        f.write(f'{process_string2}\n')
        f.write(f'{rate_string}\n')
        f.write('----------\n')


    def cal_unc(self, f):
        # print(self.df_unc.index)
        for row in self.df_unc.index:
            row_string = f'{self.df_unc.iloc[row, 0].ljust(self.printlength)}'
            row_string += f'{self.df_unc.iloc[row, 1].ljust(self.printlength)}'
            if str(self.df_unc.iloc[row, 1]).lower() in ['lnn','shape']:
                for i in range(len(self.df_unc.iloc[row, 2:])):
                    para = str(self.df_unc.iloc[row, i+2])[0:5]
                    if para == 'nan':
                        row_string += '-'.ljust(self.printlength)
                    else:
                        row_string += para.ljust(self.printlength)
            # elif str(self.df_unc.iloc[row, 1]).lower() in ['rateparam']:
            #     for i in range(len(self.df_unc.iloc[row, 2:])):
            #         para = str(self.df_unc.iloc[row, i+2])
            #         row_string += '-'.ljust(self.printlength)
            f.write(f'{row_string}\n')

        for temp_rate in self.jsons['rateParam']:
            f.write(f'{temp_rate.ljust(self.printlength)}{"rateParam".ljust(self.printlength)}')
            for temp_para in self.jsons['rateParam'][temp_rate]:
                f.write(f'{temp_para.ljust(self.printlength)}')
            f.write('\n')
        f.write('\n')


        # [channel] autoMCStats [threshold] [include-signal = 0] [hist-mode = 1]
        f.write(f'* autoMCStats {str(self.autoMCStats_threshold)} 1\n')
        pass
    
    def gen_shape(self):
        pass


    def run(self, cards_map=None):
        with open(f'card_{self.region_plotname}_{self.tag}.txt', 'w+') as f:
            self.cal_ijk(f)
            self.cal_shape_input(f)
            self.cal_observation(f)
            self.cal_rate(f)
            self.cal_unc(f)
            cards_map[str(self.region_plotname)] = {}
            cards_map[str(self.region_plotname)]['channel'] = str(self.region_plotname)
            cards_map[str(self.region_plotname)]['file'] = str(f'card_{self.region_plotname}_{str(self.tag)}.txt')
        # print(cards_map)
        return(cards_map)

if __name__ == '__main__':

    with open(f'{args.file}', 'r') as j:
        jsons = json.load(j)
    logging.basicConfig(level=logging.DEBUG)
    if os.path.isfile(f'cards_map_{jsons["utils"]["tag"]}.json'):
        logging.warning('cards_map exists, removing')
        os.remove(f'cards_map_{jsons["utils"]["tag"]}.json')
    cards_map = {}

    for region in jsons['regions']:
        region = jsons['regions'][region]
        # print(region)
        p = region_combine(config_json=region, utils=jsons['utils'] )
        cards_map = p.run(cards_map)

    with open(f'cards_map_{jsons["utils"]["tag"]}.json', 'w+') as f:
        json.dump(cards_map, f)

    cards = ''
    with open(f'cards_map_{jsons["utils"]["tag"]}.json', 'r') as f:
        jsons_map = json.load(f)
    for region in jsons_map:
        logging.info('Preparing cards for region {region}'.format(region=region))
        region = jsons_map[region]
        cards += f'{region["channel"]}={region["file"]} '
    print(cards)
    
    os.system('combineCards.py -S {cards} >& {name}_shape.txt'.format(cards=cards, name=args.output_card))
    pass
    
    codes = '''
combine -M Significance --expectSignal=1 -t -1 {name}_shape.txt > result_{name}.txt
combine -M Significance --expectSignal=1 -t -1 {name}_shape.txt --freezeParameters all > result_freezeAll{name}.txt

combine -M FitDiagnostics -t -1 --expectSignal=1 -d {name}_shape.txt -m 125 --saveShapes --saveWithUncertainties
text2workspace.py {name}_shape.txt -m 125
combineTool.py -M Impacts -d {name}_shape.root -t -1 --expectSignal=1 -m 125 --doInitialFit --robustFit 1
combineTool.py -M Impacts -d {name}_shape.root -t -1 --expectSignal=1 -m 125 --robustFit 1 --doFits --parallel 4
combineTool.py -M Impacts -d {name}_shape.root -t -1 --expectSignal=1 -m 125 -o impacts_{name}.json
plotImpacts.py -i impacts_{name}.json -o impacts_{name}
    '''

    os.system(codes.format(name=args.output_card))
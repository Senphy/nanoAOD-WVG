import os,sys
import logging
import json

def loop_json(cards, jsons):
    for region in jsons:
        logging.info('Preparing cards for region {region}'.format(region=region))
        region = jsons[region]
        for bin in region:
            bin = region[bin]
            logging.info('Preparing cards for {tag}'.format(tag=bin['tag']))
            cards = cards + '{tag}={file} '.format(tag=bin['tag'], file=bin['file'])
    return cards

def prepare_cards(name):
    cards = ''
    logging.basicConfig(level=logging.DEBUG)
    if not os.path.isfile('cards_map_2016.json'):
        logging.warning('cards_map not exist, please check')
    with open('cards_map_2016.json', 'r') as f:
        jsons = json.load(f)
        f.close()
    cards = loop_json(cards, jsons)

    if not os.path.isfile('cards_map_2017.json'):
        logging.warning('cards_map not exist, please check')
    with open('cards_map_2017.json', 'r') as f:
        jsons = json.load(f)
        f.close()
    cards = loop_json(cards, jsons)
    
    if not os.path.isfile('cards_map_2018.json'):
        logging.warning('cards_map not exist, please check')
    with open('cards_map_2018.json', 'r') as f:
        jsons = json.load(f)
        f.close()
    cards = loop_json(cards, jsons)
    
    os.system('combineCards.py {cards} >& {name}.txt'.format(cards=cards, name=name))
    os.system('combineCards.py -S {cards} >& {name}_shape.txt'.format(cards=cards, name=name))
    pass

if __name__ == '__main__':
    name = 'fullrun2'
    prepare_cards(name)
    
    codes = '''
combine -M Significance --expectSignal=1 -t -1 {name}.txt > result_{name}.txt
combine -M Significance --expectSignal=1 -t -1 {name}.txt --freezeParameters all > result_freezeAll{name}.txt

combine -M FitDiagnostics -t -1 --expectSignal=1 -d {name}_shape.txt -m 125 --saveShapes --saveWithUncertainties
text2workspace.py {name}_shape.txt -m 125
combineTool.py -M Impacts -d {name}_shape.root -t -1 --expectSignal=1 -m 125 --doInitialFit --robustFit 1
combineTool.py -M Impacts -d {name}_shape.root -t -1 --expectSignal=1 -m 125 --robustFit 1 --doFits --parallel 4
combineTool.py -M Impacts -d {name}_shape.root -t -1 --expectSignal=1 -m 125 -o impacts_{name}.json
plotImpacts.py -i impacts_{name}.json -o impacts_{name}
    '''

    os.system(codes.format(name=name))
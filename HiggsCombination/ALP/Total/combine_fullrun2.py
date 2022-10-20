import os,sys
import shutil
import logging
import json

def loop_json(cards, jsons, year, mass):
    for region in jsons:
        logging.info('Preparing cards for region {region}'.format(region=region))
        region = jsons[region]
        for bin in region:
            bin = region[bin]
            logging.info('Preparing cards for {tag}'.format(tag=bin['tag']))
            cards = cards + '{tag}=cards_{year}_m{mass}/{file} '.format(tag=bin['tag'], file=bin['file'], year=year, mass=mass)
    return cards

def prepare_cards(name, mass):
    cards = ''
    logging.basicConfig(level=logging.DEBUG)

    ini_dir = os.getcwd()
    for year in ['2016', '2017', '2018']:

        os.popen('sed -i "s/ALP_mx/ALP_m{mass}/g" ..\/{year}\/combine_SR.csv'.format(year=year, mass=mass))
        os.chdir('../{year}'.format(year=year))
        os.system('python Combine_help.py')
        os.chdir(ini_dir)
        os.popen('sed -i "s/ALP_m{mass}/ALP_mx/g" ..\/{year}\/combine_SR.csv'.format(year=year, mass=mass))

        if os.path.isdir('cards_{year}_m{mass}'.format(year=year, mass=mass)):
            shutil.rmtree('cards_{year}_m{mass}'.format(year=year, mass=mass))
        os.makedirs('cards_{year}_m{mass}'.format(year=year, mass=mass))
        shutil.copyfile('../{year}/cards_map_{year}.json'.format(year=year), 'cards_{year}_m{mass}/cards_map_{year}_m{mass}.json'.format(year=year, mass=mass))
        os.system('mv ../{year}/cards* cards_{year}_m{mass}/'.format(year=year, mass=mass))

        cards_json = 'cards_{year}_m{mass}/cards_map_{year}_m{mass}.json'.format(year=year, mass=mass)
        if not os.path.isfile(cards_json):
            logging.warning('cards_map not exist, please check')
        with open(cards_json, 'r') as f:
            jsons = json.load(f)
            f.close()
        cards = loop_json(cards, jsons, year, mass)

    os.system('combineCards.py cards_{year}_m{mass}/{cards} >& {name}_{year}_m{mass}.txt'.format(cards=cards, name=name, mass=mass, year=year))
    # os.system('combineCards.py -S cards_{year}_m{mass}/{cards} >& {name}_{year}_m{mass}_shape.txt'.format(cards=cards, name=name, mass=mass, year=year))

    codes = '''
combine -M AsymptoticLimits --run blind {name}_{year}_m{mass}.txt > result_limits_{name}_m{mass}.txt
# combine -M Significance --expectSignal=1 -t -1 {name}_{year}_m{mass}.txt > result_{name}.txt
# combine -M Significance --expectSignal=1 -t -1 {name}_{year}_m{mass}.txt --freezeParameters all > result_freezeAll{name}.txt
    '''

    os.system(codes.format(name=name, year=year, mass=mass))
    pass

if __name__ == '__main__':
    name = 'fullrun2'
    for mass in ['50', '90', '100', '110', '160', '200']:
        prepare_cards(name, mass)
    
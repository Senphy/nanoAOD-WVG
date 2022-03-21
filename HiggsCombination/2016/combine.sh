name=test16
combineCards.py cards_CR1_2016Pre/*.txt cards_CR2_2016Pre/*.txt cards_SR_2016Pre/*.txt cards_CR1_2016Post/*.txt cards_CR2_2016Post/*.txt cards_SR_2016Post/*.txt>& ${name}.txt

combine -M Significance --expectSignal=1 -t -1 ${name}.txt > result_${name}.txt
combine -M Significance --expectSignal=1 -t -1 ${name}.txt --freezeParameters all > result_freezeAll${name}.txt

text2workspace.py ${name}.txt -m 125
combineTool.py -M Impacts -d ${name}.root -t -1 --expectSignal=1 -m 125 --doInitialFit --robustFit 1
combineTool.py -M Impacts -d ${name}.root -t -1 --expectSignal=1 -m 125 --robustFit 1 --doFits --parallel 4
combineTool.py -M Impacts -d ${name}.root -t -1 --expectSignal=1 -m 125 -o impacts_${name}.json
plotImpacts.py -i impacts_${name}.json -o impacts_${name}
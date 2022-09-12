name=testfullrun2
# combineCards.py cards_CR1_2016Pre/*.txt cards_CR2_2016Pre/*.txt cards_SR_2016Pre/*.txt cards_CR1_2016Post/*.txt cards_CR2_2016Post/*.txt cards_SR_2016Post/*.txt cards_CR1_2017/*.txt cards_CR2_2017/*.txt cards_SR_2017/*.txt cards_CR1_2018/*.txt cards_CR2_2018/*.txt cards_SR_2018/*.txt>& ${name}.txt
combineCards.py cards_CR1_2016/*.txt cards_CR2_2016/*.txt cards_CR3_2016/*.txt cards_SR_2016/*.txt cards_CR1_2017/*.txt cards_CR2_2017/*.txt cards_CR3_2017/*.txt cards_SR_2017/*.txt cards_CR1_2018/*.txt cards_CR2_2018/*.txt cards_CR3_2018/*.txt cards_SR_2018/*.txt>& ${name}.txt
combineCards.py -S cards_CR1_2016/*.txt cards_CR2_2016/*.txt cards_CR3_2016/*.txt cards_SR_2016/*.txt cards_CR1_2017/*.txt cards_CR2_2017/*.txt cards_CR3_2017/*.txt cards_SR_2017/*.txt cards_CR1_2018/*.txt cards_CR2_2018/*.txt cards_CR3_2018/*.txt cards_SR_2018/*.txt>& ${name}_shape.txt
# combineCards.py cards_CR1_2017/*.txt cards_CR2_2017/*.txt cards_CR3_2017/*.txt cards_SR_2017/*.txt cards_CR1_2018/*.txt cards_CR2_2018/*.txt cards_CR3_2018/*.txt cards_SR_2018/*.txt>& ${name}.txt

combine -M Significance --expectSignal=1 -t -1 ${name}.txt > result_${name}.txt
combine -M Significance --expectSignal=1 -t -1 ${name}.txt --freezeParameters all > result_freezeAll${name}.txt

combine -M FitDiagnostics -t -1 --expectSignal=1 -d ${name}_shape.txt -m 125 --saveShapes --saveWithUncertainties
text2workspace.py ${name}_shape.txt -m 125
combineTool.py -M Impacts -d ${name}_shape.root -t -1 --expectSignal=1 -m 125 --doInitialFit --robustFit 1
combineTool.py -M Impacts -d ${name}_shape.root -t -1 --expectSignal=1 -m 125 --robustFit 1 --doFits --parallel 10
combineTool.py -M Impacts -d ${name}_shape.root -t -1 --expectSignal=1 -m 125 -o impacts_${name}.json
plotImpacts.py -i impacts_${name}.json -o impacts_${name}
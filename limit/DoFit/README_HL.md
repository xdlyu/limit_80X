Control Plots:

python g1_exo_doFit_class.py --control -c el -b

python g1_exo_doFit_class.py --control -c mu -b




Do Full Analysis:

##for WprimeWZ

python runLimitsB2GWW.py --channel mu --makeCards -b --signalmodel WprimeWZ --batchMode --lxbatchCern &
 
python runLimitsB2GWW.py --channel el --makeCards -b --signalmodel WprimeWZ --batchMode --lxbatchCern &
 

rename datacards direcotory "cards_B2GWW_XXXX" to "cards_B2GWW", for example, ln -s cards_B2GWW_closuretest0_HP_ExpN cards_B2GWW

python runLimitsB2GWW.py --channel mu --computeLimits --signalmodel WprimeWZ
 
python runLimitsB2GWW.py --channel el --computeLimits --signalmodel WprimeWZ
 
python runLimitsB2GWW.py --channel em --computeLimits --signalmodel WprimeWZ

 
python runLimitsB2GWW.py --channel mu --plotLimits -b --signalmodel WprimeWZ
 
python runLimitsB2GWW.py --channel el --plotLimits -b --signalmodel WprimeWZ
 
python runLimitsB2GWW.py --channel em --plotLimits -b --signalmodel WprimeWZ
 

##for WprimeWZ-HVT-A

python runLimitsB2GWW.py --channel mu --makeCards -b --signalmodel WprimeWZ-HVT-A --batchMode --lxbatchCern &
 
python runLimitsB2GWW.py --channel el --makeCards -b --signalmodel WprimeWZ-HVT-A --batchMode --lxbatchCern &
 

rename datacards direcotory "cards_B2GWW_XXXX" to "cards_B2GWW", for example, ln -s cards_B2GWW_closuretest0_HP_ExpN cards_B2GWW

python runLimitsB2GWW.py --channel mu --computeLimits --signalmodel WprimeWZ-HVT-A
 
python runLimitsB2GWW.py --channel el --computeLimits --signalmodel WprimeWZ-HVT-A
 
python runLimitsB2GWW.py --channel em --computeLimits --signalmodel WprimeWZ-HVT-A

 
python runLimitsB2GWW.py --channel mu --plotLimits -b --signalmodel WprimeWZ-HVT-A
 
python runLimitsB2GWW.py --channel el --plotLimits -b --signalmodel WprimeWZ-HVT-A
 
python runLimitsB2GWW.py --channel em --plotLimits -b --signalmodel WprimeWZ-HVT-A
 



# for BulkGravWW


python runLimitsB2GWW.py --channel mu --makeCards -b --signalmodel BulkGravWW 

python runLimitsB2GWW.py --channel el --makeCards -b --signalmodel BulkGravWW  

#batchMode at cern lxplus
python runLimitsB2GWW.py --channel mu --masswindow W --makeCards -b --signalmodel BulkGravWW --category HP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel el --masswindow W --makeCards -b --signalmodel BulkGravWW --category HP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel mu --masswindow Z --makeCards -b --signalmodel BulkGravWW --category HP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel el --masswindow Z --makeCards -b --signalmodel BulkGravWW --category HP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel mu --masswindow W --makeCards -b --signalmodel BulkGravWW --category LP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel el --masswindow W --makeCards -b --signalmodel BulkGravWW --category LP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel mu --masswindow Z --makeCards -b --signalmodel BulkGravWW --category LP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel el --masswindow Z --makeCards -b --signalmodel BulkGravWW --category LP --batchMode --lxbatchCern &

rename datacards direcotory "cards_B2GWW_XXXX" to "cards_B2GWW", for example, ln -s cards_B2GWW_closuretest0_ExpN cards_B2GWW

###combine channel, masswingdow, purity

python runLimitsB2GWW.py --channel em --masswindow W --computeLimits --signalmodel BulkGravWW --category HP --onlyCombine
python runLimitsB2GWW.py --channel em --masswindow Z --computeLimits --signalmodel BulkGravWW --category HP --onlyCombine
python runLimitsB2GWW.py --channel mu --masswindow WZ --computeLimits --signalmodel BulkGravWW --category HP --onlyCombine
python runLimitsB2GWW.py --channel el --masswindow WZ --computeLimits --signalmodel BulkGravWW --category HP --onlyCombine
python runLimitsB2GWW.py --channel em --masswindow WZ --computeLimits --signalmodel BulkGravWW --category HP --onlyCombine

python runLimitsB2GWW.py --channel em --masswindow W --computeLimits --signalmodel BulkGravWW --category LP --onlyCombine
python runLimitsB2GWW.py --channel em --masswindow Z --computeLimits --signalmodel BulkGravWW --category LP --onlyCombine
python runLimitsB2GWW.py --channel mu --masswindow WZ --computeLimits --signalmodel BulkGravWW --category LP --onlyCombine
python runLimitsB2GWW.py --channel el --masswindow WZ --computeLimits --signalmodel BulkGravWW --category LP --onlyCombine
python runLimitsB2GWW.py --channel em --masswindow WZ --computeLimits --signalmodel BulkGravWW --category LP --onlyCombine

python runLimitsB2GWW.py --channel mu --masswindow W --computeLimits --signalmodel BulkGravWW --category HL --onlyCombine
python runLimitsB2GWW.py --channel el --masswindow W --computeLimits --signalmodel BulkGravWW --category HL --onlyCombine
python runLimitsB2GWW.py --channel em --masswindow W --computeLimits --signalmodel BulkGravWW --category HL --onlyCombine
python runLimitsB2GWW.py --channel mu --masswindow Z --computeLimits --signalmodel BulkGravWW --category HL --onlyCombine
python runLimitsB2GWW.py --channel el --masswindow Z --computeLimits --signalmodel BulkGravWW --category HL --onlyCombine
python runLimitsB2GWW.py --channel em --masswindow Z --computeLimits --signalmodel BulkGravWW --category HL --onlyCombine
python runLimitsB2GWW.py --channel mu --masswindow WZ --computeLimits --signalmodel BulkGravWW --category HL --onlyCombine
python runLimitsB2GWW.py --channel el --masswindow WZ --computeLimits --signalmodel BulkGravWW --category HL --onlyCombine
python runLimitsB2GWW.py --channel em --masswindow WZ --computeLimits --signalmodel BulkGravWW --category HL --onlyCombine

###calculate limit

python runLimitsB2GWW.py --channel mu --masswindow W --computeLimits --signalmodel BulkGravWW --category HP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel el --masswindow W --computeLimits --signalmodel BulkGravWW --category HP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel em --masswindow W --computeLimits --signalmodel BulkGravWW --category HP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel mu --masswindow Z --computeLimits --signalmodel BulkGravWW --category HP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel el --masswindow Z --computeLimits --signalmodel BulkGravWW --category HP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel em --masswindow Z --computeLimits --signalmodel BulkGravWW --category HP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel mu --masswindow WZ --computeLimits --signalmodel BulkGravWW --category HP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel el --masswindow WZ --computeLimits --signalmodel BulkGravWW --category HP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel em --masswindow WZ --computeLimits --signalmodel BulkGravWW --category HP --batchMode --lxbatchCern &

python runLimitsB2GWW.py --channel mu --masswindow W --computeLimits --signalmodel BulkGravWW --category LP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel el --masswindow W --computeLimits --signalmodel BulkGravWW --category LP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel em --masswindow W --computeLimits --signalmodel BulkGravWW --category LP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel mu --masswindow Z --computeLimits --signalmodel BulkGravWW --category LP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel el --masswindow Z --computeLimits --signalmodel BulkGravWW --category LP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel em --masswindow Z --computeLimits --signalmodel BulkGravWW --category LP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel mu --masswindow WZ --computeLimits --signalmodel BulkGravWW --category LP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel el --masswindow WZ --computeLimits --signalmodel BulkGravWW --category LP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel em --masswindow WZ --computeLimits --signalmodel BulkGravWW --category LP --batchMode --lxbatchCern &

python runLimitsB2GWW.py --channel mu --masswindow W --computeLimits --signalmodel BulkGravWW --category HL --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel el --masswindow W --computeLimits --signalmodel BulkGravWW --category HL --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel em --masswindow W --computeLimits --signalmodel BulkGravWW --category HL --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel mu --masswindow Z --computeLimits --signalmodel BulkGravWW --category HL --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel el --masswindow Z --computeLimits --signalmodel BulkGravWW --category HL --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel em --masswindow Z --computeLimits --signalmodel BulkGravWW --category HL --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel mu --masswindow WZ --computeLimits --signalmodel BulkGravWW --category HL --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel el --masswindow WZ --computeLimits --signalmodel BulkGravWW --category HL --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel em --masswindow WZ --computeLimits --signalmodel BulkGravWW --category HL --batchMode --lxbatchCern &

###Draw limit

python runLimitsB2GWW.py --channel mu --masswindow W --plotLimits -b --signalmodel BulkGravWW  

python runLimitsB2GWW.py --channel el --masswindow W --plotLimits -b --signalmodel BulkGravWW  

python runLimitsB2GWW.py --channel em --masswindow W --plotLimits -b --signalmodel BulkGravWW  

python runLimitsB2GWW.py --channel mu --masswindow Z --plotLimits -b --signalmodel BulkGravWW

python runLimitsB2GWW.py --channel el --masswindow Z --plotLimits -b --signalmodel BulkGravWW

python runLimitsB2GWW.py --channel em --masswindow Z --plotLimits -b --signalmodel BulkGravWW

python runLimitsB2GWW.py --channel mu --masswindow WZ --plotLimits -b --signalmodel BulkGravWW

python runLimitsB2GWW.py --channel el --masswindow WZ --plotLimits -b --signalmodel BulkGravWW

python runLimitsB2GWW.py --channel em --masswindow WZ --plotLimits -b --signalmodel BulkGravWW

###diff NP step1

python runLimitsB2GWW.py --channel mu --masswindow W --closurechecks --signalmodel BulkGravWW --category HP --Bonly 0 

python runLimitsB2GWW.py --channel el --masswindow W --closurechecks --signalmodel BulkGravWW --category HP --Bonly 0

python runLimitsB2GWW.py --channel mu --masswindow Z --closurechecks --signalmodel BulkGravWW --category HP --Bonly 0

python runLimitsB2GWW.py --channel el --masswindow Z --closurechecks --signalmodel BulkGravWW --category HP --Bonly 0

python runLimitsB2GWW.py --channel mu --masswindow W --closurechecks --signalmodel BulkGravWW --category LP --Bonly 0

python runLimitsB2GWW.py --channel el --masswindow W --closurechecks --signalmodel BulkGravWW --category LP --Bonly 0

python runLimitsB2GWW.py --channel mu --masswindow Z --closurechecks --signalmodel BulkGravWW --category LP --Bonly 0

python runLimitsB2GWW.py --channel el --masswindow Z --closurechecks --signalmodel BulkGravWW --category LP --Bonly 0

python runLimitsB2GWW.py --channel mu --masswindow W --closurechecks --signalmodel BulkGravWW --category HP --Bonly 1

python runLimitsB2GWW.py --channel el --masswindow W --closurechecks --signalmodel BulkGravWW --category HP --Bonly 1

python runLimitsB2GWW.py --channel mu --masswindow Z --closurechecks --signalmodel BulkGravWW --category HP --Bonly 1

python runLimitsB2GWW.py --channel el --masswindow Z --closurechecks --signalmodel BulkGravWW --category HP --Bonly 1

python runLimitsB2GWW.py --channel mu --masswindow W --closurechecks --signalmodel BulkGravWW --category LP --Bonly 1

python runLimitsB2GWW.py --channel el --masswindow W --closurechecks --signalmodel BulkGravWW --category LP --Bonly 1

python runLimitsB2GWW.py --channel mu --masswindow Z --closurechecks --signalmodel BulkGravWW --category LP --Bonly 1

python runLimitsB2GWW.py --channel el --masswindow Z --closurechecks --signalmodel BulkGravWW --category LP --Bonly 1

###diff NP step2

python runLimitsB2GWW.py --channel mu --masswindow W --diffNuisances --signalmodel BulkGravWW --category HP --Bonly 0

python runLimitsB2GWW.py --channel el --masswindow W --diffNuisances --signalmodel BulkGravWW --category HP --Bonly 0

python runLimitsB2GWW.py --channel mu --masswindow Z --diffNuisances --signalmodel BulkGravWW --category HP --Bonly 0

python runLimitsB2GWW.py --channel el --masswindow Z --diffNuisances --signalmodel BulkGravWW --category HP --Bonly 0

python runLimitsB2GWW.py --channel mu --masswindow W --diffNuisances --signalmodel BulkGravWW --category LP --Bonly 0

python runLimitsB2GWW.py --channel el --masswindow W --diffNuisances --signalmodel BulkGravWW --category LP --Bonly 0

python runLimitsB2GWW.py --channel mu --masswindow Z --diffNuisances --signalmodel BulkGravWW --category LP --Bonly 0

python runLimitsB2GWW.py --channel el --masswindow Z --diffNuisances --signalmodel BulkGravWW --category LP --Bonly 0

python runLimitsB2GWW.py --channel mu --masswindow W --diffNuisances --signalmodel BulkGravWW --category HP --Bonly 1

python runLimitsB2GWW.py --channel el --masswindow W --diffNuisances --signalmodel BulkGravWW --category HP --Bonly 1

python runLimitsB2GWW.py --channel mu --masswindow Z --diffNuisances --signalmodel BulkGravWW --category HP --Bonly 1

python runLimitsB2GWW.py --channel el --masswindow Z --diffNuisances --signalmodel BulkGravWW --category HP --Bonly 1

python runLimitsB2GWW.py --channel mu --masswindow W --diffNuisances --signalmodel BulkGravWW --category LP --Bonly 1

python runLimitsB2GWW.py --channel el --masswindow W --diffNuisances --signalmodel BulkGravWW --category LP --Bonly 1

python runLimitsB2GWW.py --channel mu --masswindow Z --diffNuisances --signalmodel BulkGravWW --category LP --Bonly 1

python runLimitsB2GWW.py --channel el --masswindow Z --diffNuisances --signalmodel BulkGravWW --category LP --Bonly 1

###diff NP step0 is need

python runLimitsB2GWW.py --channel mu --masswindow W --text2workspace --signalmodel BulkGravWW --category HP

python runLimitsB2GWW.py --channel el --masswindow W --text2workspace --signalmodel BulkGravWW --category HP

python runLimitsB2GWW.py --channel mu --masswindow Z --text2workspace --signalmodel BulkGravWW --category HP

python runLimitsB2GWW.py --channel el --masswindow Z --text2workspace --signalmodel BulkGravWW --category HP

python runLimitsB2GWW.py --channel mu --masswindow W --text2workspace --signalmodel BulkGravWW --category LP

python runLimitsB2GWW.py --channel el --masswindow W --text2workspace --signalmodel BulkGravWW --category LP

python runLimitsB2GWW.py --channel mu --masswindow Z --text2workspace --signalmodel BulkGravWW --category LP

python runLimitsB2GWW.py --channel el --masswindow Z --text2workspace --signalmodel BulkGravWW --category LP

###draw post-fit plots

python runLimitsB2GWW.py --channel mu --masswindow W --drawpostfit --signalmodel BulkGravWW --category HP --Bonly 1

python runLimitsB2GWW.py --channel el --masswindow W --drawpostfit --signalmodel BulkGravWW --category HP --Bonly 1

python runLimitsB2GWW.py --channel mu --masswindow W --drawpostfit --signalmodel BulkGravWW --category LP --Bonly 1

python runLimitsB2GWW.py --channel el --masswindow W --drawpostfit --signalmodel BulkGravWW --category LP --Bonly 1

python runLimitsB2GWW.py --channel mu --masswindow Z --drawpostfit --signalmodel BulkGravWW --category HP --Bonly 1

python runLimitsB2GWW.py --channel el --masswindow Z --drawpostfit --signalmodel BulkGravWW --category HP --Bonly 1

python runLimitsB2GWW.py --channel mu --masswindow Z --drawpostfit --signalmodel BulkGravWW --category LP --Bonly 1

python runLimitsB2GWW.py --channel el --masswindow Z --drawpostfit --signalmodel BulkGravWW --category LP --Bonly 1


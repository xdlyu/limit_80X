Control Plots:

python g1_exo_doFit_class.py --control -c el -b

python g1_exo_doFit_class.py --control -c mu -b




Do Full Analysis:

# for WprimeWZ


python runLimitsB2GWW.py --channel mu --makeCards -b --signalmodel WprimeWZ 

python runLimitsB2GWW.py --channel el --makeCards -b --signalmodel WprimeWZ  

#batchMode at cern lxplus
python runLimitsB2GWW.py --channel mu --masswindow W --makeCards -b --signalmodel WprimeWZ --category HP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel el --masswindow W --makeCards -b --signalmodel WprimeWZ --category HP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel mu --masswindow Z --makeCards -b --signalmodel WprimeWZ --category HP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel el --masswindow Z --makeCards -b --signalmodel WprimeWZ --category HP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel mu --masswindow W --makeCards -b --signalmodel WprimeWZ --category LP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel el --masswindow W --makeCards -b --signalmodel WprimeWZ --category LP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel mu --masswindow Z --makeCards -b --signalmodel WprimeWZ --category LP --batchMode --lxbatchCern &
python runLimitsB2GWW.py --channel el --masswindow Z --makeCards -b --signalmodel WprimeWZ --category LP --batchMode --lxbatchCern &

rename datacards direcotory "cards_B2GWW_XXXX" to "cards_B2GWW", for example, ln -s cards_B2GWZ_closuretest0_ExpN cards_B2GWZ

###calculate limit & combine channel, masswingdow, purity

python runLimitsB2GWW.py --channel mu --masswindow W --computeLimits --signalmodel WprimeWZ --category HP
python runLimitsB2GWW.py --channel el --masswindow W --computeLimits --signalmodel WprimeWZ --category HP
python runLimitsB2GWW.py --channel em --masswindow W --computeLimits --signalmodel WprimeWZ --category HP
python runLimitsB2GWW.py --channel mu --masswindow Z --computeLimits --signalmodel WprimeWZ --category HP
python runLimitsB2GWW.py --channel el --masswindow Z --computeLimits --signalmodel WprimeWZ --category HP
python runLimitsB2GWW.py --channel em --masswindow Z --computeLimits --signalmodel WprimeWZ --category HP
python runLimitsB2GWW.py --channel mu --masswindow WZ --computeLimits --signalmodel WprimeWZ --category HP
python runLimitsB2GWW.py --channel el --masswindow WZ --computeLimits --signalmodel WprimeWZ --category HP
python runLimitsB2GWW.py --channel em --masswindow WZ --computeLimits --signalmodel WprimeWZ --category HP

python runLimitsB2GWW.py --channel mu --masswindow W --computeLimits --signalmodel WprimeWZ --category LP
python runLimitsB2GWW.py --channel el --masswindow W --computeLimits --signalmodel WprimeWZ --category LP
python runLimitsB2GWW.py --channel em --masswindow W --computeLimits --signalmodel WprimeWZ --category LP
python runLimitsB2GWW.py --channel mu --masswindow Z --computeLimits --signalmodel WprimeWZ --category LP
python runLimitsB2GWW.py --channel el --masswindow Z --computeLimits --signalmodel WprimeWZ --category LP
python runLimitsB2GWW.py --channel em --masswindow Z --computeLimits --signalmodel WprimeWZ --category LP
python runLimitsB2GWW.py --channel mu --masswindow WZ --computeLimits --signalmodel WprimeWZ --category LP
python runLimitsB2GWW.py --channel el --masswindow WZ --computeLimits --signalmodel WprimeWZ --category LP
python runLimitsB2GWW.py --channel em --masswindow WZ --computeLimits --signalmodel WprimeWZ --category LP

python runLimitsB2GWW.py --channel mu --masswindow W --computeLimits --signalmodel WprimeWZ --category HL
python runLimitsB2GWW.py --channel el --masswindow W --computeLimits --signalmodel WprimeWZ --category HL
python runLimitsB2GWW.py --channel em --masswindow W --computeLimits --signalmodel WprimeWZ --category HL
python runLimitsB2GWW.py --channel mu --masswindow Z --computeLimits --signalmodel WprimeWZ --category HL
python runLimitsB2GWW.py --channel el --masswindow Z --computeLimits --signalmodel WprimeWZ --category HL
python runLimitsB2GWW.py --channel em --masswindow Z --computeLimits --signalmodel WprimeWZ --category HL
python runLimitsB2GWW.py --channel mu --masswindow WZ --computeLimits --signalmodel WprimeWZ --category HL
python runLimitsB2GWW.py --channel el --masswindow WZ --computeLimits --signalmodel WprimeWZ --category HL
python runLimitsB2GWW.py --channel em --masswindow WZ --computeLimits --signalmodel WprimeWZ --category HL

###Draw limit

python runLimitsB2GWW.py --channel mu --masswindow W --plotLimits -b --signalmodel WprimeWZ --category HP  
python runLimitsB2GWW.py --channel el --masswindow W --plotLimits -b --signalmodel WprimeWZ --category HP  
python runLimitsB2GWW.py --channel em --masswindow W --plotLimits -b --signalmodel WprimeWZ --category HP  
python runLimitsB2GWW.py --channel mu --masswindow Z --plotLimits -b --signalmodel WprimeWZ --category HP
python runLimitsB2GWW.py --channel el --masswindow Z --plotLimits -b --signalmodel WprimeWZ --category HP
python runLimitsB2GWW.py --channel em --masswindow Z --plotLimits -b --signalmodel WprimeWZ --category HP
python runLimitsB2GWW.py --channel mu --masswindow WZ --plotLimits -b --signalmodel WprimeWZ --category HP
python runLimitsB2GWW.py --channel el --masswindow WZ --plotLimits -b --signalmodel WprimeWZ --category HP
python runLimitsB2GWW.py --channel em --masswindow WZ --plotLimits -b --signalmodel WprimeWZ --category HP

python runLimitsB2GWW.py --channel mu --masswindow W --plotLimits -b --signalmodel WprimeWZ --category LP
python runLimitsB2GWW.py --channel el --masswindow W --plotLimits -b --signalmodel WprimeWZ --category LP
python runLimitsB2GWW.py --channel em --masswindow W --plotLimits -b --signalmodel WprimeWZ --category LP
python runLimitsB2GWW.py --channel mu --masswindow Z --plotLimits -b --signalmodel WprimeWZ --category LP
python runLimitsB2GWW.py --channel el --masswindow Z --plotLimits -b --signalmodel WprimeWZ --category LP
python runLimitsB2GWW.py --channel em --masswindow Z --plotLimits -b --signalmodel WprimeWZ --category LP
python runLimitsB2GWW.py --channel mu --masswindow WZ --plotLimits -b --signalmodel WprimeWZ --category LP
python runLimitsB2GWW.py --channel el --masswindow WZ --plotLimits -b --signalmodel WprimeWZ --category LP
python runLimitsB2GWW.py --channel em --masswindow WZ --plotLimits -b --signalmodel WprimeWZ --category LP

python runLimitsB2GWW.py --channel mu --masswindow W --plotLimits -b --signalmodel WprimeWZ --category HL
python runLimitsB2GWW.py --channel el --masswindow W --plotLimits -b --signalmodel WprimeWZ --category HL
python runLimitsB2GWW.py --channel em --masswindow W --plotLimits -b --signalmodel WprimeWZ --category HL
python runLimitsB2GWW.py --channel mu --masswindow Z --plotLimits -b --signalmodel WprimeWZ --category HL
python runLimitsB2GWW.py --channel el --masswindow Z --plotLimits -b --signalmodel WprimeWZ --category HL
python runLimitsB2GWW.py --channel em --masswindow Z --plotLimits -b --signalmodel WprimeWZ --category HL
python runLimitsB2GWW.py --channel mu --masswindow WZ --plotLimits -b --signalmodel WprimeWZ --category HL
python runLimitsB2GWW.py --channel el --masswindow WZ --plotLimits -b --signalmodel WprimeWZ --category HL
python runLimitsB2GWW.py --channel em --masswindow WZ --plotLimits -b --signalmodel WprimeWZ --category HL


###diff NP step1

python runLimitsB2GWW.py --channel mu --masswindow W --closurechecks --signalmodel WprimeWZ --category HP --Bonly 0 

python runLimitsB2GWW.py --channel el --masswindow W --closurechecks --signalmodel WprimeWZ --category HP --Bonly 0

python runLimitsB2GWW.py --channel mu --masswindow Z --closurechecks --signalmodel WprimeWZ --category HP --Bonly 0

python runLimitsB2GWW.py --channel el --masswindow Z --closurechecks --signalmodel WprimeWZ --category HP --Bonly 0

python runLimitsB2GWW.py --channel mu --masswindow W --closurechecks --signalmodel WprimeWZ --category LP --Bonly 0

python runLimitsB2GWW.py --channel el --masswindow W --closurechecks --signalmodel WprimeWZ --category LP --Bonly 0

python runLimitsB2GWW.py --channel mu --masswindow Z --closurechecks --signalmodel WprimeWZ --category LP --Bonly 0

python runLimitsB2GWW.py --channel el --masswindow Z --closurechecks --signalmodel WprimeWZ --category LP --Bonly 0

python runLimitsB2GWW.py --channel mu --masswindow W --closurechecks --signalmodel WprimeWZ --category HP --Bonly 1

python runLimitsB2GWW.py --channel el --masswindow W --closurechecks --signalmodel WprimeWZ --category HP --Bonly 1

python runLimitsB2GWW.py --channel mu --masswindow Z --closurechecks --signalmodel WprimeWZ --category HP --Bonly 1

python runLimitsB2GWW.py --channel el --masswindow Z --closurechecks --signalmodel WprimeWZ --category HP --Bonly 1

python runLimitsB2GWW.py --channel mu --masswindow W --closurechecks --signalmodel WprimeWZ --category LP --Bonly 1

python runLimitsB2GWW.py --channel el --masswindow W --closurechecks --signalmodel WprimeWZ --category LP --Bonly 1

python runLimitsB2GWW.py --channel mu --masswindow Z --closurechecks --signalmodel WprimeWZ --category LP --Bonly 1

python runLimitsB2GWW.py --channel el --masswindow Z --closurechecks --signalmodel WprimeWZ --category LP --Bonly 1

###diff NP step2

python runLimitsB2GWW.py --channel mu --masswindow W --diffNuisances --signalmodel WprimeWZ --category HP --Bonly 0

python runLimitsB2GWW.py --channel el --masswindow W --diffNuisances --signalmodel WprimeWZ --category HP --Bonly 0

python runLimitsB2GWW.py --channel mu --masswindow Z --diffNuisances --signalmodel WprimeWZ --category HP --Bonly 0

python runLimitsB2GWW.py --channel el --masswindow Z --diffNuisances --signalmodel WprimeWZ --category HP --Bonly 0

python runLimitsB2GWW.py --channel mu --masswindow W --diffNuisances --signalmodel WprimeWZ --category LP --Bonly 0

python runLimitsB2GWW.py --channel el --masswindow W --diffNuisances --signalmodel WprimeWZ --category LP --Bonly 0

python runLimitsB2GWW.py --channel mu --masswindow Z --diffNuisances --signalmodel WprimeWZ --category LP --Bonly 0

python runLimitsB2GWW.py --channel el --masswindow Z --diffNuisances --signalmodel WprimeWZ --category LP --Bonly 0

python runLimitsB2GWW.py --channel mu --masswindow W --diffNuisances --signalmodel WprimeWZ --category HP --Bonly 1

python runLimitsB2GWW.py --channel el --masswindow W --diffNuisances --signalmodel WprimeWZ --category HP --Bonly 1

python runLimitsB2GWW.py --channel mu --masswindow Z --diffNuisances --signalmodel WprimeWZ --category HP --Bonly 1

python runLimitsB2GWW.py --channel el --masswindow Z --diffNuisances --signalmodel WprimeWZ --category HP --Bonly 1

python runLimitsB2GWW.py --channel mu --masswindow W --diffNuisances --signalmodel WprimeWZ --category LP --Bonly 1

python runLimitsB2GWW.py --channel el --masswindow W --diffNuisances --signalmodel WprimeWZ --category LP --Bonly 1

python runLimitsB2GWW.py --channel mu --masswindow Z --diffNuisances --signalmodel WprimeWZ --category LP --Bonly 1

python runLimitsB2GWW.py --channel el --masswindow Z --diffNuisances --signalmodel WprimeWZ --category LP --Bonly 1

###diff NP step0 is need

python runLimitsB2GWW.py --channel mu --masswindow W --text2workspace --signalmodel WprimeWZ --category HP

python runLimitsB2GWW.py --channel el --masswindow W --text2workspace --signalmodel WprimeWZ --category HP

python runLimitsB2GWW.py --channel mu --masswindow Z --text2workspace --signalmodel WprimeWZ --category HP

python runLimitsB2GWW.py --channel el --masswindow Z --text2workspace --signalmodel WprimeWZ --category HP

python runLimitsB2GWW.py --channel mu --masswindow W --text2workspace --signalmodel WprimeWZ --category LP

python runLimitsB2GWW.py --channel el --masswindow W --text2workspace --signalmodel WprimeWZ --category LP

python runLimitsB2GWW.py --channel mu --masswindow Z --text2workspace --signalmodel WprimeWZ --category LP

python runLimitsB2GWW.py --channel el --masswindow Z --text2workspace --signalmodel WprimeWZ --category LP

###draw post-fit plots

python runLimitsB2GWW.py --channel mu --masswindow W --drawpostfit --signalmodel WprimeWZ --category HP --Bonly 1

python runLimitsB2GWW.py --channel el --masswindow W --drawpostfit --signalmodel WprimeWZ --category HP --Bonly 1

python runLimitsB2GWW.py --channel mu --masswindow W --drawpostfit --signalmodel WprimeWZ --category LP --Bonly 1

python runLimitsB2GWW.py --channel el --masswindow W --drawpostfit --signalmodel WprimeWZ --category LP --Bonly 1

python runLimitsB2GWW.py --channel mu --masswindow Z --drawpostfit --signalmodel WprimeWZ --category HP --Bonly 1

python runLimitsB2GWW.py --channel el --masswindow Z --drawpostfit --signalmodel WprimeWZ --category HP --Bonly 1

python runLimitsB2GWW.py --channel mu --masswindow Z --drawpostfit --signalmodel WprimeWZ --category LP --Bonly 1

python runLimitsB2GWW.py --channel el --masswindow Z --drawpostfit --signalmodel WprimeWZ --category LP --Bonly 1


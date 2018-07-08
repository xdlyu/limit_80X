reference: https://github.com/lbrianza/boostedWWAnalysis/blob/master/README.md


Pratical examples for the Bias study:

1> signal injection
-> generate toys with a specific model without signal, foe a mass point :

    
    python runLimits_run2exo_new.py --computeLimits --generateOnly --datacardDIR cards_B2GWW_closuretest0_ExpN --channel mu --massPoint 4000  --injectSingalStrenght 0 --nToys 1000 --inputGeneratedDataset Generated_SB --outputTree 0 --batchMode --lxbatchCern  


-> Make Fit and generation together (not crossed study --> exampl generate with ExpN and re-fit with Exp for signal injection test):

    python runLimits_run2exo_new.py --computeLimits --maximumLikelihood --batchMode --lxbatchCern --datacardDIR cards_B2GWW_closuretest0_ExpN --channel mu --massPoint 4000 --injectSingalStrenght 1 --nToys 1000 --outputTree 0 --crossedToys 0

2> cross bias test
-> Make the Fit on a set of generated dataset, using a different model between generation and fit 

First of all you must generate toys according with a defined model as explained above.

Then you have to:

    python runLimits_run2exo_new.py --computeLimits --generateOnly --datacardDIR cards_B2GWW_closuretest0_Exp/ --channel mu --massPoint 4000 --injectSingalStrenght 1 --nToys 1000 --inputGeneratedDataset cards_B2GWW_closuretest0_Exp4000/ --outputTree 0 --batchMode --lxbatchCern 
    python runLimits_run2exo_new.py --computeLimits --maximumLikelihood --datacardDIR cards_B2GWW_closuretest0_Exp/cards_B2GWW_closuretest0_Exp4000/ --channel mu --massPoint 4000 --nToys 1000 --inputGeneratedDataset cards_B2GWW_closuretest0_Exp4000/ --outputTree 0 --crossedToys  1 --batchMode --lxbatchCern 


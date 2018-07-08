####Set up environment####

export SCRAM_ARCH=slc6_amd64_gcc530

cmsrel CMSSW_8_1_0

cd CMSSW_8_1_0/src

cmsenv

git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit

cd HiggsAnalysis/CombinedLimit

cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit

git fetch origin

git checkout v7.0.7

scramv1 b clean

scramv1 b

####For BulkGravWW####

git clone https://github.com/chengchen1993/limit.git 

cd limit/DoFit

vi newstyle_B2GWW_doFit_class.py

% Modify location of file_Directory (line 216)

% For muon and electron channel, only W masswindow

mkdir cards_B2GWW_closuretest0_ExpN cards_B2GWW

ln -s cards_B2GWW_closuretest0_ExpN cards_B2GWW

. fit.sh

. combin.sh

. calculatelimits.sh

. draw.sh

% If always fail, use: source autorun.sh

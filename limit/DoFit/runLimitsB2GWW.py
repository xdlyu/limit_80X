#! /usr/bin/env python
import os
#import glob
#import math
#import array
#import sys
import time
import CMS_lumi

from array import array

import ROOT
from ROOT import gROOT, gStyle, gSystem, TLatex, TH1D, TString, TPaveText, TGaxis, TLine, kBlack
#import subprocess
#from subprocess import Popen
from optparse import OptionParser

############################################
#             Job steering                 #
############################################

parser = OptionParser()

parser.add_option('-b', action='store_true', dest='noX', default=True, help='no X11 windows')

### to make the full analysis fit + datacards
parser.add_option('--makeCards', action='store_true', dest='makeCards', default=False, help='make datacards plus whole analysis')

### to compute limits
parser.add_option('--computeLimits', action='store_true', dest='computeLimits', default=False, help='compute limits')
### only combine, not calculate
parser.add_option('--onlyCombine', action='store_true', dest='onlyCombine', default=False, help='only combine')
### to plot limits
parser.add_option('--plotLimits', action='store_true', dest='plotLimits', default=False, help='plot limits')
### to do Closure checks:https: //twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsWG/HiggsPAGPreapprovalChecks
parser.add_option('--closurechecks', action='store_true', dest='closurechecks', default=False, help='Closure checks')
### run 2nd step
parser.add_option('--diffNuisances', action='store_true', dest='diffNuisances', default=False, help='diffNuisances')
###run 0th step if need
parser.add_option('--text2workspace', action='store_true', dest='text2workspace', default=False, help='text2workspace')
###draw post-fit plots
parser.add_option('--drawpostfit', action='store_true', dest='drawpostfit', default=False, help='Draw post-fit plots')
### set --expectSignal, --expectSignal 0 is B only, 1 is s+b
parser.add_option('--Bonly', action='store',type="int", dest='Bonly', default=0, help='Bonly')

parser.add_option('--lvqqBR', action='store_true', dest='lvqqBR', default=False, help='computing with munu BR')

### to do just signal lineshape fits
parser.add_option('--fitSignal', action='store_true', dest='fitSignal', default=False, help='do signal lineshape fits')

### other options 
parser.add_option('--signalmodel',action="store",type="string",dest="signalmodel",default="BulkGravWW")
#parser.add_option('--signalmodel',action="store",type="string",dest="signalmodel",default="WprimeWZ")
parser.add_option('--channel',action="store",type="string",dest="channel",default="mu")
parser.add_option('--masswindow',action="store",type="string",dest="masswindow",default="W")
parser.add_option('--massPoint',action="store",type="int",dest="massPoint",default=-1)
#parser.add_option('--cPrime',action="store",type="int",dest="cPrime",default=-1)
parser.add_option('--odir',action="store",type="string",dest="odir",default=".")
parser.add_option('--category',action="store",type="string",dest="category",default="HL") #"HP")
parser.add_option('--closuretest', action='store',type="int", dest='closuretest', default=0, help='closure test; 0: no test; 1: A1->A2; 2: A->B')
parser.add_option('--limitMode', action='store',type="int", dest='limitMode', default=0, help='limit Mode; 0: AsymptoticLimits ; 1: ProfileLikelihood ; 2: FullCLs ; 3: MaxLikelihoodFit')
#parser.add_option('--isReReco', action='store',type="int", dest='isReReco', default=1, help='limit Mode; 0: Old signal samples ; 1: New signal Samples')
parser.add_option('--keepblind', action='store',type="int", dest='keepblind', default=0, help='1: keepblind; 0: unblind')
parser.add_option('--Sys', action='store',type="int", dest='Sys', default=1, help='run limit with or without systematic')
#parser.add_option('--plotPvalue', action='store',type="int", default=0, dest='plotPvalue', help='plot p value')
#parser.add_option('--signalWidth', action='store',type="int", default=0, dest='signalWidth', help='analysis on non-narrow signals')

##### submit jobs to condor, lxbatch and hercules 
parser.add_option('--batchMode',      action='store_true', dest='batchMode',      default=False, help='to run jobs on condor fnal')
parser.add_option('--lxbatchCern',    action='store_true', dest='lxbatchCern',    default=False, help='run jobs on lxbatch system at cern, default is condor fnal')
parser.add_option('--herculesMilano', action='store_true', dest='herculesMilano', default=False, help='run jobs on hercules system at Milano, default is condor fnal')
parser.add_option('--queque',      action="store", type="string", dest="queque",      default="1nw")




(options, args) = parser.parse_args()


#########################################
### Global Variables for running jobs ###
#########################################


Lumi=35.867

if options.signalmodel=="BulkGravWW":
    ### mass point for signal to be fitted
    mass      = [1000,1200,1400,1600,1800,2000,2500,3000,3500,4000,4500]
    binwidth  = [1,1,1,1,1,1,1,1,1,1,1]
    ### mass window for couting analysis
    ccmlo     = [ 900,1100,1300,1500,1700,1900,2400,2900,3400,3900,4400 ] 
    ccmhi     = [1100,1300,1500,1700,1900,2100,2600,3100,3600,4100,4600 ]
    ### jet mass range
    mjlo      = [  40,  40,  40,  40,  40,  40,  40,  40,  40,  40,  40]
    mjhi      = [ 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150]
    ### mlvj range min and max used when run with option --makeCards
    #fit range
    mlo       = [ 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800]
    #mlo       = [  600, 600, 600, 600, 600, 600,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000]
    mhi       = [5000,5000,5000,5000,5000,5000,5000,5000,5000,5000,5000]
    ### shape to be used for bkg when --makeCards

####set1,ExpN+Pow
    shape    = ["ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN"]
    shapeAlt = ["Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow"]
####set2,Pow+ExpN
    #shape    = [ "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow"]
    #shapeAlt = ["ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN"]
####set3,Exp+ExpN
    #shape    = [ "Exp", "Exp", "Exp", "Exp", "Exp", "Exp", "Exp", "Exp", "Exp", "Exp", "Exp"]
    #shapeAlt = ["ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN"]


    ### shape to be used for bkg when --fitSignal
    #shape_sig_width  = ["BWDoubleCB" ,"BWDoubleCB" , "BWDoubleCB" , "BWDoubleCB" , "BWDoubleCB" ,  "BWDoubleCB", "BWDoubleCB" ,"BWDoubleCB" , "BWDoubleCB" , "BWDoubleCB" , "BWDoubleCB" ,  "BWDoubleCB", "BWDoubleCB" , "BWDoubleCB" , "BWDoubleCB" ,  "BWDoubleCB"]
    #shape_sig_narrow = ["DoubleCB_v1","DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1","DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1"]
    
    
    ##################################################
    #  cross-sections for HVT and LH model  #
    ##################################################
    xsDict =  {
            600:    647.3*1e-3, 
            700:    267.8*1e-3,
#            750:    110.500282*1e-3,
            800:    126.6*1e-3, 
            900:    63.7*1e-3, 
            1000:   35.1*1e-3,
            1200: 14.3   *1e-3,  
            1400: 5.86*1e-3,  
            1600: 2.41*1e-3,  
            1800: 0.979 *1e-3,  
            2000: 0.478*1e-3,  
            2500: 0.0967*1e-3,  
            3000: 0.0259*1e-3,  
            3500: 0.00586*1e-3,  
            4000: 0.00162*1e-3,  
            4500: 0.000451*1e-3
            }
    xsDict_PDF =  {
                    600 : 0.09,
                    700 : 0.10,
                    750 : 0.10,
                    800 : 0.11,
                    900 : 0.13,
                    1000: 0.13,
                    1200: 0.14,
                    1400: 0.17,
                    1600: 0.19,
                    1800: 0.22,
                    2000: 0.25,
                    2500: 0.34,
                    3000: 0.45,
                    3500: 0.59,
                    4000: 0.78,
                    4500: 1.0   }
    xsDict_scale =  {
                    600 : 0.08,
                    700 : 0.09,
                    750 : 0.10,
                    800 : 0.10,
                    900 : 0.11,
                    1000: 0.11,
                    1200: 0.12,
                    1400: 0.13,
                    1600: 0.14,
                    1800: 0.15,
                    2000: 0.16,
                    2500: 0.17,
                    3000: 0.19,
                    3500: 0.20,
                    4000: 0.22,
                    4500: 0.23  }

    xsDict_lvj =  {
            600:    647.3*1e-3*0.44, 
            700:    267.8*1e-3*0.44, 
#            750:    110.500282*1e-3*0.44,    
            800:    126.6*1e-3*0.44, 
            900:    63.7*1e-3*0.44, 
            1000:   35.1*1e-3*0.44,
            1200: 14.3   *1e-3*0.44,  
            1400: 5.86*1e-3*0.44,  
            1600: 2.41*1e-3*0.44,  
            1800: 0.979 *1e-3*0.44,  
            2000: 0.478*1e-3*0.44,  
            2500: 0.0967*1e-3*0.44,  
            3000: 0.0259*1e-3*0.44,  
            3500: 0.00586*1e-3*0.44,  
            4000: 0.00162*1e-3*0.44,  
            4500: 0.000451*1e-3*0.44
            }
    
    table_signalscale =  {
             600: 1, 
             700: 1,
#             750: 1,    
             800: 1, 
             900: 1, 
            1000: 1,
            1200: 1,  
            1400: 1,  
            1600: 3,  
            1800: 5,  
            2000: 10,  
            2500: 50,  
            3000: 300,  
            3500: 2000,  
            4000: 5000,  
            4500: 20000
            }


elif options.signalmodel=="WprimeWZ":
    ### mass point for signal to be fitted
    mass      = [1000,1200,1400,1600,1800,2000,2500,3000,3500,4000,4500]
    binwidth  = [1,1,1,1,1,1,1,1,1,1,1]
    ### mass window for couting analysis
    ccmlo     = [ 900,1100,1300,1500,1700,1900,2400,2900,3400,3900,4400 ] 
    ccmhi     = [1100,1300,1500,1700,1900,2100,2600,3100,3600,4100,4600 ]
    ### jet mass range
    mjlo      = [ 40,  40,  40,  40,  40,  40,  40,  40,  40,  40,  40]
    mjhi      = [150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150]
    ### mlvj range min and max used when run with option --makeCards
    #fit range
    mlo       = [ 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800]
    #mlo       = [ 600, 600,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000]
    mhi       = [5000,5000,5000,5000,5000,5000,5000,5000,5000,5000,5000]
    ### shape to be used for bkg when --makeCards
    shape    = ["ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN"]
    shapeAlt = [ "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow"]

    ### shape to be used for bkg when --fitSignal
    #shape_sig_width  = ["BWDoubleCB" ,"BWDoubleCB" , "BWDoubleCB" , "BWDoubleCB" , "BWDoubleCB" ,  "BWDoubleCB", "BWDoubleCB" ,"BWDoubleCB" , "BWDoubleCB" , "BWDoubleCB" , "BWDoubleCB" ,  "BWDoubleCB", "BWDoubleCB" , "BWDoubleCB" , "BWDoubleCB" ,  "BWDoubleCB"]
    #shape_sig_narrow = ["DoubleCB_v1","DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1","DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1"]
    
    
    ##################################################
    #  cross-sections for HVT and LH model  #
    ##################################################
    xsDict =  { # Z->hadron 69.91%, W->lnu 10.8%, W-> hadron 67.67%
             800: 153.25     *1e-3/0.2265, 
            1000: 102.236    *1e-3/0.2265, 
            1200: 56.357     *1e-3/0.2265, 
            1400: 31.283     *1e-3/0.2265,   
            1600: 17.844     *1e-3/0.2265, 
            1800: 10.458     *1e-3/0.2265,   
            2000: 6.273      *1e-3/0.2265,   
            2500: 1.8842     *1e-3/0.2265,   
            3000: 0.6039     *1e-3/0.2265,   
            3500: 0.19991    *1e-3/0.2265,   
            4000: 0.064901   *1e-3/0.2265,   
            4500: 0.021981241*1e-3/0.2265  
            }
    xsDict_lvj =  {
             800: 153.25     *1e-3, 
            1000: 102.236    *1e-3,
            1200: 56.357     *1e-3,  
            1400: 31.283     *1e-3,  
            1600: 17.844     *1e-3,  
            1800: 10.458     *1e-3,  
            2000: 6.273      *1e-3,  
            2500: 1.8842     *1e-3,  
            3000: 0.6039     *1e-3,  
            3500: 0.19991    *1e-3,  
            4000: 0.064901   *1e-3,  
            4500: 0.021981241*1e-3
            }
    xsDict_PDF =  {
                    600 : 0.04,
                    700 : 0.04,
                    750 : 0.04,
                    800 : 0.04,
                    900 : 0.04,
                    1000: 0.04,
                    1200: 0.04,
                    1400: 0.05,
                    1600: 0.05,
                    1800: 0.05,
                    2000: 0.05,
                    2500: 0.07,
                    3000: 0.08,
                    3500: 0.12,
                    4000: 0.18,
                    4500: 0.31  }
    xsDict_scale = {
                    600 : 0.01,
                    700 : 0.02,
                    750 : 0.02,
                    800 : 0.03,
                    900 : 0.03,
                    1000: 0.04,
                    1200: 0.05,
                    1400: 0.06,
                    1600: 0.07,
                    1800: 0.07,
                    2000: 0.08,
                    2500: 0.10,
                    3000: 0.11,
                    3500: 0.13,
                    4000: 0.14,
                    4500: 0.15  }

    
    table_signalscale =  {
                 800: 1, 
                1000: 1,
                1200: 1,  
                1400: 1,  
                1600: 1,  
                1800: 1,  
                2000: 1,  
                2500: 1,  
                3000: 3,  
                3500: 20,  
                4000: 50,  
                4500: 200 }

elif options.signalmodel=="WprimeWZ-HVT-A":
    ### mass point for signal to be fitted
    mass      = [600,800,1000,1200,1400,1600,1800,2000,2500,3000,3500,4000,4500]
    binwidth  = [0,0,0,1,1,1,1,1,1,1,1,1,1]
    ### mass window for couting analysis
    ccmlo     = [500, 700, 900,1100,1300,1500,1700,1900,2400,2900,3400,3900,4400 ] 
    ccmhi     = [700, 900,1100,1300,1500,1700,1900,2100,2600,3100,3600,4100,4600 ]
    ### jet mass range
    mjlo      = [ 40,  40,  40,  40,  40,  40,  40,  40,  40,  40,  40,  40,  40]
    mjhi      = [150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150]
    ### mlvj range min and max used when run with option --makeCards
    #fit range
    mlo       = [ 600, 600, 600, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800]
    mhi       = [1500,1500,1500,5000,5000,5000,5000,5000,5000,5000,5000,5000,5000]
    ### shape to be used for bkg when --makeCards
    shape    = ["ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN","ExpN"]
    shapeAlt = [ "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow", "Pow"]

    ### shape to be used for bkg when --fitSignal
    #shape_sig_width  = ["BWDoubleCB" ,"BWDoubleCB" , "BWDoubleCB" , "BWDoubleCB" , "BWDoubleCB" ,  "BWDoubleCB", "BWDoubleCB" ,"BWDoubleCB" , "BWDoubleCB" , "BWDoubleCB" , "BWDoubleCB" ,  "BWDoubleCB", "BWDoubleCB" , "BWDoubleCB" , "BWDoubleCB" ,  "BWDoubleCB"]
    #shape_sig_narrow = ["DoubleCB_v1","DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1","DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1", "DoubleCB_v1"]
    
    
    ##################################################
    #  cross-sections for HVT and LH model  #
    ##################################################
    xsDict =  { # Z->hadron 69.91%, W->lnu 10.8%, W-> hadron 67.67%
             600:938.7692472 *1e-3/0.2265,
             800:283.2686754 *1e-3/0.2265, 
            1000: 110.823309 *1e-3/0.2265, 
            1200: 47.6329732 *1e-3/0.2265, 
            1400: 25.2858598 *1e-3/0.2265,   
            1600: 12.9944181 *1e-3/0.2265, 
            1800: 7.63895053 *1e-3/0.2265,   
            2000: 4.33381797 *1e-3/0.2265,   
            2500: 1.26058651 *1e-3/0.2265,   
            3000: 0.40236999 *1e-3/0.2265,   
            3500: 0.13144619 *1e-3/0.2265,   
            4000: 0.04344501 *1e-3/0.2265,   
            4500: 0.01424789 *1e-3/0.2265  
            }
    xsDict_lvj =  {
             600:938.7692472 *1e-3,
             800:283.2686754 *1e-3,
            1000: 110.823309 *1e-3,
            1200: 47.6329732 *1e-3,  
            1400: 25.2858598 *1e-3,  
            1600: 12.9944181 *1e-3,  
            1800: 7.63895053 *1e-3,  
            2000: 4.33381797 *1e-3,  
            2500: 1.26058651 *1e-3,  
            3000: 0.40236999 *1e-3,  
            3500: 0.13144619 *1e-3,  
            4000: 0.04344501 *1e-3,  
            4500: 0.01424789 *1e-3
            }
    
    table_signalscale =  {
                 600: 1, 
                 800: 1, 
                1000: 1,
                1200: 1,  
                1400: 1,  
                1600: 1,  
                1800: 1,  
                2000: 1,  
                2500: 1,  
                3000: 3,  
                3500: 20,  
                4000: 50,  
                4500: 200 }
########################################
###### Submit batch job for cards ######
########################################

def submitBatchJob( command, fn ):
       
    currentDir = os.getcwd();
    CMSSWDir = currentDir+"/../";
       
    # create a dummy bash/csh
    outScript = open(fn+".sh","w");
    
    if not options.lxbatchCern and not options.herculesMilano :
        outScript.write('#!/bin/bash');
        outScript.write("\n"+'date');
        outScript.write("\n"+'source /uscmst1/prod/sw/cms/bashrc prod');
        outScript.write("\n"+'echo "condor dir: " ${_CONDOR_SCRATCH_DIR}');    
        outScript.write("\n"+'cd '+currentDir);
        outScript.write("\n"+'eval `scram runtime -sh`');
        outScript.write("\n"+'cd -');    
        outScript.write("\n"+'export PATH=${PATH}:'+currentDir);
        outScript.write("\n"+'echo ${PATH}');
        outScript.write("\n"+'ls'); 
        outScript.write("\n"+command);  
        outScript.write("\n"+'tar -cvzf outputFrom_'+fn+'.tar.gz *');    
        outScript.close();
   
        condorScript = open("condor_"+fn,"w");
        condorScript.write('universe = vanilla')
        condorScript.write("\n"+"Executable = "+fn+".sh")
        condorScript.write("\n"+'Requirements = Memory >= 199 &&OpSys == "LINUX"&& (Arch != "DUMMY" )&& Disk > 1000000')
        condorScript.write("\n"+'Should_Transfer_Files = YES')
        #condorScript.write("\n"+'Transfer_Input_Files = doFit_class_higgs.py, BiasStudy/do_fitBias_higgs.py, AutoDict_std__map_std__string_std__string__cxx.so')    
        condorScript.write("\n"+'Transfer_Input_Files = newstyle_B2GWW_doFit_class.py, CMS_lumi.py, tdrstyle.py, ./PDFs/PdfDiagonalizer_cc.so, ./PDFs/Util_cxx.so, ./PDFs/HWWLVJRooPdfs_cxx.so')    
        condorScript.write("\n"+'WhenToTransferOutput  = ON_EXIT_OR_EVICT')
        condorScript.write("\n"+'Output = out_$(Cluster).stdout')
        condorScript.write("\n"+'Error  = out_$(Cluster).stderr')
        condorScript.write("\n"+'Error  = out_$(Cluster).stderr')
        condorScript.write("\n"+'Log    = out_$(Cluster).log')
        condorScript.write("\n"+'Notification    = Error')
        condorScript.write("\n"+'Queue 1')
        condorScript.close();
   
        print ("condor_submit "+"condor_"+fn);
        os.system("condor_submit "+"condor_"+fn);
   
    elif options.lxbatchCern and not options.herculesMilano and options.makeCards:
        outScript.write('#!/bin/bash');
        outScript.write("\n"+'cd '+CMSSWDir);
        outScript.write("\n"+'eval `scram runtime -sh`');
        outScript.write("\n"+'cd -');
        outScript.write("\necho $PWD");
        outScript.write("\nls");
        #outScript.write("\ncp -r "+currentDir+"/PDFs ./")
        #outScript.write("\ncp -r "+currentDir+"/PKUTree_final_6p26fb_Jul18 ./")
        outScript.write("\ncp -r "+currentDir+"/CMS_lumi.py ./")
        outScript.write("\ncp -r "+currentDir+"/tdrstyle.py ./")
        outScript.write("\ncp -r "+currentDir+"/newstyle_B2GWW_doFit_class.py ./")

        outScript.write("\n"+command);
        #outScript.write("\n"+'rm *.out');  
        outScript.write("\ncp -r cards* "+currentDir)
        outScript.write("\ncp -r doFit_plots* "+currentDir)

        outScript.close();
               
        os.system("chmod 777 "+currentDir+"/"+fn+".sh");
        if options.queque != "":
            print ("bsub -q "+options.queque+" -cwd "+currentDir+" "+fn+".sh");
            os.system("bsub -q "+options.queque+" -cwd "+currentDir+" "+fn+".sh");
        else:
            print ("bsub -q cmscaf1nd -cwd "+currentDir+" "+fn+".sh");
            os.system("bsub -q cmscaf1nd -cwd "+currentDir+" "+fn+".sh");

    elif options.lxbatchCern and not options.herculesMilano and options.computeLimits: 
        outScript.write('#!/bin/bash');
        outScript.write("\n"+'cd '+CMSSWDir);
        outScript.write("\n"+'eval `scram runtime -sh`');
        outScript.write("\n"+'cd -');
        outScript.write("\necho $PWD");
        outScript.write("\nls");
        #outScript.write("\ncp -r "+currentDir+"/PDFs ./")
        #outScript.write("\ncp -r "+currentDir+"/PKUTree_final_6p26fb_Jul18 ./")
        #outScript.write("\ncp -r "+currentDir+"/CMS_lumi.py ./")
        #outScript.write("\ncp -r "+currentDir+"/tdrstyle.py ./")
        #outScript.write("\ncp -r "+currentDir+"/newstyle_B2GWW_doFit_class.py ./")
        outScript.write("\ncp -r "+currentDir+"/wwlvj_%s%03d_%s_%s_%s_unbin.txt ./"%(options.signalmodel ,mass[i],options.channel, options.category,options.masswindow))
#        outScript.write("\ncp -r "+currentDir+"/wwlvj_%s%03d_%s_%s_%s_workspace.root ./"%(options.signalmodel ,mass[i],options.channel, options.category,options.masswindow))
        outScript.write("\ncp -r "+currentDir+"/wwlvj_%s%03d_mu_HP_W_workspace.root ./"%(options.signalmodel ,mass[i]))
        outScript.write("\ncp -r "+currentDir+"/wwlvj_%s%03d_el_HP_W_workspace.root ./"%(options.signalmodel ,mass[i]))
        outScript.write("\ncp -r "+currentDir+"/wwlvj_%s%03d_mu_LP_W_workspace.root ./"%(options.signalmodel ,mass[i]))
        outScript.write("\ncp -r "+currentDir+"/wwlvj_%s%03d_el_LP_W_workspace.root ./"%(options.signalmodel ,mass[i]))


        outScript.write("\n"+command);
        #outScript.write("\n"+'rm *.out');  
        outScript.write("\ncp -r higgsCombine* "+currentDir)
        #outScript.write("\ncp -r doFit_plots* "+currentDir)

        outScript.close();

        os.system("chmod 777 "+currentDir+"/"+fn+".sh");
        if options.queque != "":
            print ("bsub -q "+options.queque+" -cwd "+currentDir+" "+fn+".sh");
            os.system("bsub -q "+options.queque+" -cwd "+currentDir+" "+fn+".sh");
        else:
            print ("bsub -q cmscaf1nd -cwd "+currentDir+" "+fn+".sh");
            os.system("bsub -q cmscaf1nd -cwd "+currentDir+" "+fn+".sh");



            
    elif not options.lxbatchCern and options.herculesMilano:
        outScript.write('#!/bin/bash');
        outScript.write("\n"+'cd '+currentDir);
        outScript.write("\n"+'eval `scram runtime -sh`');
        outScript.write("\n"+'cd -');
        outScript.write("\n"+'cp '+currentDir+'/BiasStudy/do_fitBias_higgs.py ./');
        outScript.write("\n"+'cp '+currentDir+'/doFit_class_higgs.py ./');
        outScript.write("\n"+'ls');  
        outScript.write("\n"+"unbuffer "+command+" > /gwteray/users/brianza/output"+fn+".txt");
        outScript.close();
               
        os.system("chmod 777 "+currentDir+"/"+fn+".sh");
        
        if options.queque != "":
            os.system("qsub -V -d "+currentDir+" -q "+options.queque+" "+currentDir+"/"+fn+".sh");
        else:
            os.system("qsub -V -d "+currentDir+" -q longcms "+currentDir+"/"+fn+".sh");
      



################################
## style setup for doUL plots ##
################################
def setStyle():

  gStyle.SetPadBorderMode(0);
  gStyle.SetFrameBorderMode(0);
  gStyle.SetPadBottomMargin(0.12);
  gStyle.SetPadLeftMargin(0.12);
  gStyle.SetCanvasColor(ROOT.kWhite);
  gStyle.SetCanvasDefH(600); #Height of canvas
  gStyle.SetCanvasDefW(600); #Width of canvas
  gStyle.SetCanvasDefX(0);   #POsition on screen
  gStyle.SetCanvasDefY(0);

  gStyle.SetPadTopMargin(0.05);
  gStyle.SetPadBottomMargin(0.15);#0.13);
  gStyle.SetPadLeftMargin(0.15);#0.16);
  gStyle.SetPadRightMargin(0.05);#0.02);

  # For the Pad:
  gStyle.SetPadBorderMode(0);
  # gStyle.SetPadBorderSize(Width_t size = 1);
  gStyle.SetPadColor(ROOT.kWhite);
  gStyle.SetPadGridX(ROOT.kFALSE);
  gStyle.SetPadGridY(ROOT.kFALSE);
  gStyle.SetGridColor(0);
  gStyle.SetGridStyle(3);
  gStyle.SetGridWidth(1);

  # For the frame:
  gStyle.SetFrameBorderMode(0);
  gStyle.SetFrameBorderSize(1);
  gStyle.SetFrameFillColor(0);
  gStyle.SetFrameFillStyle(0);
  gStyle.SetFrameLineColor(1);
  gStyle.SetFrameLineStyle(1);
  gStyle.SetFrameLineWidth(1);

  gStyle.SetAxisColor(1, "XYZ");
  gStyle.SetStripDecimals(ROOT.kTRUE);
  gStyle.SetTickLength(0.03, "XYZ");
  gStyle.SetNdivisions(505, "XYZ");
  gStyle.SetPadTickX(1);  # To get tick marks on the opposite side of the frame
  gStyle.SetPadTickY(1);
  gStyle.SetGridColor(0);
  gStyle.SetGridStyle(3);
  gStyle.SetGridWidth(1);

  gStyle.SetTitleColor(1, "XYZ");
  gStyle.SetTitleFont(42, "XYZ");
  gStyle.SetTitleSize(0.05, "XYZ");
  # gStyle.SetTitleXSize(Float_t size = 0.02); # Another way to set the size?
  # gStyle.SetTitleYSize(Float_t size = 0.02);
  gStyle.SetTitleXOffset(1.15);#0.9);
  gStyle.SetTitleYOffset(1.3); # => 1.15 if exponents
  gStyle.SetLabelColor(1, "XYZ");
  gStyle.SetLabelFont(42, "XYZ");
  gStyle.SetLabelOffset(0.007, "XYZ");
  gStyle.SetLabelSize(0.045, "XYZ");

  gStyle.SetPadBorderMode(0);
  gStyle.SetFrameBorderMode(0);
  gStyle.SetTitleTextColor(1);
  gStyle.SetTitleFillColor(10);
  gStyle.SetTitleFontSize(0.05);


##################################################
### Get Limit Value from Combine -M Asymptotic ###
##################################################
def getAsymLimits(file):
    
    
    f = ROOT.TFile(file);
    t = f.Get("limit");
    entries = t.GetEntries();
    
    lims = [0,0,0,0,0,0];
    
    for i in range(entries):
        
        t.GetEntry(i);
        t_quantileExpected = t.quantileExpected;
        t_limit = t.limit;
        
        #print "limit: ", t_limit, ", quantileExpected: ",t_quantileExpected;
        
        if t_quantileExpected == -1.: lims[0] = t_limit;
        elif t_quantileExpected >= 0.024 and t_quantileExpected <= 0.026: lims[1] = t_limit;
        elif t_quantileExpected >= 0.15  and t_quantileExpected <= 0.17:  lims[2] = t_limit;
        elif t_quantileExpected == 0.5: lims[3] = t_limit;
        elif t_quantileExpected >= 0.83  and t_quantileExpected <= 0.85:  lims[4] = t_limit;
        elif t_quantileExpected >= 0.974 and t_quantileExpected <= 0.976: lims[5] = t_limit;
        else: print "Unknown quantile!"
        print "entries: ", entries;
        print "obs: ", lims[0], ", 2s: ", lims[1], lims[1], ", 1s: ", lims[2], lims[4], ", exp: ", lims[3];
    
    return lims;

##########################################
### Make Limit Plot --> Brazilian Plot ###
##########################################
def doULPlot( suffix ):
    
    xbins     = array('d', [])
    xbins_env = array('d', [])
    ybins_exp = array('d', [])
    ybins_obs = array('d', [])
    ybins_1s  = array('d', [])
    ybins_2s  = array('d', [])
    ybins_th = array('d', [])
    ybins_th_up = array('d', [])
    ybins_th_down = array('d', [])
    ybins_th_1s = array('d', [])
 
    for i in range(len(mass)):
        curFile = "higgsCombine_lim_%s%03d%s.AsymptoticLimits.mH%03d.root"%( options.signalmodel, mass[i], suffix, mass[i]);
        print "curFile: %s"%curFile;
        if options.lvqqBR:
            sf = table_signalscale[mass[i]]*xsDict_lvj[mass[i]]; #*0.1057*0.577; # BR(W->munu)*BR(H->bb)
        else:
            sf = table_signalscale[mass[i]]*xsDict[mass[i]];

        curAsymLimits = getAsymLimits(curFile);
        #print mass[i]
        #print curAsymLimits
        #raw_input("zixu")
        xbins.append( mass[i]/1000. );#GeV->TeV
        xbins_env.append( mass[i]/1000. );
        ybins_exp.append( curAsymLimits[3]*sf );
        ybins_obs.append( curAsymLimits[0]*sf );
        ybins_2s.append( curAsymLimits[1]*sf );
        ybins_1s.append( curAsymLimits[2]*sf );
        #ybins_th.append(sf);#/20.); #*0.25);
        xsDict_PDF_mass = xsDict_PDF[mass[i]];
        xsDict_scale_mass = xsDict_scale[mass[i]];
        Xsec_un = (xsDict_PDF_mass**2+xsDict_scale_mass**2)**0.5;
        if options.lvqqBR:
            ybins_th.append(xsDict_lvj[mass[i]]);#/20.); #*0.25);
            ybins_th_up.append(xsDict_lvj[mass[i]]*(1.0+Xsec_un));
            ybins_th_down.append(xsDict_lvj[mass[i]]/(1.0+Xsec_un));
            ybins_th_1s.append(xsDict_lvj[mass[i]]*(1.0+Xsec_un));
        else:
            ybins_th.append(xsDict[mass[i]]);#/20.); #*0.25);
            ybins_th_up.append(xsDict[mass[i]]*(1.0+Xsec_un));
            ybins_th_down.append(xsDict[mass[i]]/(1.0+Xsec_un));
            ybins_th_1s.append(xsDict[mass[i]]*(1.0+Xsec_un));
    
    for i in range( len(mass)-1, -1, -1 ):
        curFile = "higgsCombine_lim_%s%03d%s.AsymptoticLimits.mH%03d.root"%( options.signalmodel, mass[i], suffix, mass[i]);
        print "curFile: %s"%curFile;
        if options.lvqqBR:
          sf = table_signalscale[mass[i]]*xsDict_lvj[mass[i]]; #*0.1057*0.577; # BR(W->munu)*BR(H->bb)

        else:
          sf = table_signalscale[mass[i]]*xsDict[mass[i]];


        curAsymLimits = getAsymLimits(curFile);
        xbins_env.append( mass[i]/1000. );
        ybins_2s.append( curAsymLimits[5]*sf );
        ybins_1s.append( curAsymLimits[4]*sf );
        xsDict_PDF_mass = xsDict_PDF[mass[i]];
        xsDict_scale_mass = xsDict_scale[mass[i]];
        Xsec_un = (xsDict_PDF_mass**2+xsDict_scale_mass**2)**0.5;

        if options.lvqqBR:
          ybins_th_1s.append(xsDict_lvj[mass[i]]/(1.0+Xsec_un));

        else:
          ybins_th_1s.append(xsDict[mass[i]]/(1.0+Xsec_un));


    nPoints = len(mass);
    curGraph_exp = ROOT.TGraphAsymmErrors(nPoints,xbins,ybins_exp);
    curGraph_obs = ROOT.TGraphAsymmErrors(nPoints,xbins,ybins_obs);
    curGraph_th = ROOT.TGraph(nPoints,xbins,ybins_th);
    curGraph_th_up = ROOT.TGraph(nPoints,xbins,ybins_th_up);
    curGraph_th_down = ROOT.TGraph(nPoints,xbins,ybins_th_down);
    curGraph_1s = ROOT.TGraphAsymmErrors(nPoints*2,xbins_env,ybins_1s);
    curGraph_2s = ROOT.TGraphAsymmErrors(nPoints*2,xbins_env,ybins_2s);
    curGraph_th_1s = ROOT.TGraphAsymmErrors(nPoints*2,xbins_env,ybins_th_1s);
    
    curGraph_obs.SetMarkerStyle(20);
    curGraph_obs.SetLineWidth(3);
    curGraph_obs.SetLineStyle(1);
    curGraph_obs.SetMarkerSize(1.6);
    curGraph_exp.SetMarkerSize(1.3);
    curGraph_exp.SetMarkerColor(ROOT.kBlack);

    curGraph_exp.SetLineStyle(2);
    curGraph_exp.SetLineWidth(3);
    curGraph_exp.SetMarkerSize(2);
    curGraph_exp.SetMarkerStyle(24);
    curGraph_exp.SetMarkerColor(ROOT.kBlack);

    #curGraph_th.SetLineStyle(ROOT.kDashed);
    curGraph_th.SetFillStyle(3344);
    curGraph_th.SetLineWidth(2);
    curGraph_th.SetMarkerSize(2);
    curGraph_th.SetLineColor(ROOT.kRed);
    curGraph_th_up.SetFillStyle(3344);
    curGraph_th_up.SetLineWidth(2);
    curGraph_th_up.SetMarkerSize(2);
    curGraph_th_up.SetLineColor(ROOT.kRed);
    curGraph_th_down.SetFillStyle(3344);
    curGraph_th_down.SetLineWidth(2);
    curGraph_th_down.SetMarkerSize(2);
    curGraph_th_down.SetLineColor(ROOT.kRed);


    curGraph_1s.SetFillColor(ROOT.kGreen);
    curGraph_1s.SetFillStyle(1001);
    curGraph_1s.SetLineStyle(ROOT.kDashed);
    curGraph_1s.SetLineWidth(3);

    curGraph_2s.SetFillColor(ROOT.kYellow);
    curGraph_2s.SetFillStyle(1001);
    curGraph_2s.SetLineStyle(ROOT.kDashed);
    curGraph_2s.SetLineWidth(3);
    
    curGraph_th_1s.SetFillColor(ROOT.kRed);
    curGraph_th_1s.SetFillStyle(3013);
    curGraph_th_1s.SetLineStyle(1);
    curGraph_th_1s.SetLineColor(ROOT.kRed);
    curGraph_th_1s.SetLineWidth(2);
        
    oneLine = ROOT.TF1("oneLine","1",799,1001);
    oneLine.SetLineColor(ROOT.kRed);
    oneLine.SetLineWidth(3);

    setStyle();

    can_SM = ROOT.TCanvas("can_SM","can_SM",630,600);
    
    hrl_SM = can_SM.DrawFrame(mass[0]/1000.-0.01,1e-5, mass[nPoints-1]/1000.+0.01, 1e1);

    if options.signalmodel=="BulkGravWW":
        if options.lvqqBR:
            hrl_SM.GetYaxis().SetTitle("#sigma_{95%} (pp #rightarrow G_{Bulk} #rightarrow WW #rightarrow l#nuqq') (pb)");
        else:
            hrl_SM.GetYaxis().SetTitle("#sigma_{95%} (pp #rightarrow G_{Bulk} #rightarrow WW) (pb)");
    elif options.signalmodel=="WprimeWZ":
        if options.lvqqBR:
            hrl_SM.GetYaxis().SetTitle("#sigma_{95%} (pp #rightarrow W' #rightarrow WZ #rightarrow l#nuqq') (pb)");
        else:
            hrl_SM.GetYaxis().SetTitle("#sigma_{95%} (pp #rightarrow W' #rightarrow WZ) (pb)");
    elif options.signalmodel=="WprimeWZ-HVT-A":
        if options.lvqqBR:
            hrl_SM.GetYaxis().SetTitle("#sigma_{95%} (pp #rightarrow W' #rightarrow WZ #rightarrow l#nuqq') (pb)");
        else:
            hrl_SM.GetYaxis().SetTitle("#sigma_{95%} (pp #rightarrow W' #rightarrow WZ) (pb)");

    hrl_SM.GetYaxis().SetTitleOffset(1.35);
    hrl_SM.GetYaxis().SetTitleSize(0.045);
    hrl_SM.GetYaxis().SetTitleFont(42);

    if options.signalmodel=="BulkGravWW":
        hrl_SM.GetXaxis().SetTitle("M_{G_{Bulk}} (TeV)");
    elif options.signalmodel=="WprimeWZ":
        hrl_SM.GetXaxis().SetTitle("M_{W'} (TeV)");
    elif options.signalmodel=="WprimeWZ-HVT-A":
        hrl_SM.GetXaxis().SetTitle("M_{W'} (TeV)");


    hrl_SM.GetXaxis().SetTitleSize(0.045);
    hrl_SM.GetXaxis().SetTitleFont(42);

    hrl_SM.GetXaxis().SetNdivisions(510);
    hrl_SM.GetYaxis().SetNdivisions(505);
    can_SM.SetGridx(1);
    can_SM.SetGridy(1);

    curGraph_2s.Draw("F");
    curGraph_1s.Draw("Fsame");
    curGraph_th_1s.Draw("Fsame");
    if options.keepblind==0:
        curGraph_obs.Draw("PLsame");
    curGraph_exp.Draw("Lsame");
    curGraph_th.Draw("Csame");
#    curGraph_th_up.Draw("Csame");
#    curGraph_th_down.Draw("Csame");
       
    leg2 = ROOT.TLegend(0.32,0.72,0.9,0.92);

    leg2.SetFillColor(0);
    leg2.SetFillStyle(0);
    leg2.SetBorderSize(0);
    leg2.SetShadowColor(0);
    leg2.SetTextFont(42);
    leg2.SetTextSize(0.035);

    leg2.AddEntry(curGraph_1s,"Asympt. CL_{S}  Expected #pm 1 s.d.","LF")
    leg2.AddEntry(curGraph_2s,"Asympt. CL_{S}  Expected #pm 2 s.d.","LF")
    if options.signalmodel=="BulkGravWW":
        if options.lvqqBR:
            leg2.AddEntry(curGraph_th_1s,"#sigma_{TH} #times BR(G_{Bulk}#rightarrow WW#rightarrow l#nuqq'), #tilde{k}=0.5","LF");
        else:
            leg2.AddEntry(curGraph_th_1s,"#sigma_{TH} #times BR(G_{Bulk}#rightarrow WW), #tilde{k}=0.5","LF");
    elif options.signalmodel=="WprimeWZ":
        if options.lvqqBR:
            leg2.AddEntry(curGraph_th,"#sigma_{TH} #times BR(W'_{HVT B}#rightarrow WZ#rightarrow l#nuqq')","L");
        else:
            leg2.AddEntry(curGraph_th,"#sigma_{TH} #times BR(W'_{HVT B}#rightarrow WZ)","L");
    elif options.signalmodel=="WprimeWZ-HVT-A":
        if options.lvqqBR:
            leg2.AddEntry(curGraph_th,"#sigma_{TH} #times BR(W'_{HVT A}#rightarrow WZ#rightarrow l#nuqq')","L");
        else:
            leg2.AddEntry(curGraph_th,"#sigma_{TH} #times BR(W'_{HVT A}#rightarrow WZ)","L");
    leg2.AddEntry(curGraph_obs,"Asympt. CL_{S} Observed","LP")




    #ROOT.gPad.SetLogx();
    #hrl_SM.GetXaxis().SetMoreLogLabels()
    #hrl_SM.GetXaxis().SetNoExponent()
    ROOT.gPad.SetLogy();

    can_SM.Update();
    can_SM.RedrawAxis();
    can_SM.RedrawAxis("g");
    can_SM.Update();

    leg2.Draw();
#    line = TLine( 1.1, 1e-4, 1.1, 1e0)
#    line.SetLineWidth(2)
#    line.SetLineColor(kBlack)
#    line.SetLineStyle(9)
#    line.Draw();


    banner = TLatex(0.95, 0.96, "%2.1f fb^{-1} (13 TeV)"%(Lumi));
    banner.SetNDC(); banner.SetTextSize(0.038); banner.SetTextFont(42); banner.SetTextAlign(31); banner.SetLineWidth(2); banner.Draw();
    CMStext = TLatex(0.15,0.96,"CMS");
    CMStext.SetNDC(); CMStext.SetTextSize(0.041); CMStext.SetTextFont(61); CMStext.SetTextAlign(11); CMStext.SetLineWidth(2); CMStext.Draw();
#    if suffix =="_el_HP_W" or suffix =="_el_HP_Z" or suffix =="_el_HP_WZ":
    if options.channel == "el":
        Extratext = TLatex(0.241, 0.96, "Preliminary W#rightarrow e#nu");
        Extratext.SetNDC(); Extratext.SetTextSize(0.032); Extratext.SetTextFont(52); Extratext.SetTextAlign(11); Extratext.SetLineWidth(2); Extratext.Draw();
#    elif suffix =="_mu_HP_W" or suffix =="_mu_HP_Z" or suffix =="_mu_HP_WZ":
    elif options.channel == "mu":
        Extratext = TLatex(0.241, 0.96, "Preliminary W#rightarrow #mu#nu");
        Extratext.SetNDC(); Extratext.SetTextSize(0.032); Extratext.SetTextFont(52); Extratext.SetTextAlign(11); Extratext.SetLineWidth(2); Extratext.Draw();
#    elif suffix =="_em_HP_W" or suffix =="_em_HP_Z" or suffix =="_em_HP_WZ":
    elif options.channel == "em":
        Extratext = TLatex(0.241, 0.96, "Preliminary W#rightarrow l#nu");
        Extratext.SetNDC(); Extratext.SetTextSize(0.032); Extratext.SetTextFont(52); Extratext.SetTextAlign(11); Extratext.SetLineWidth(2); Extratext.Draw();

    #CMS_lumi.lumi_13TeV = "%s fb^{-1}"%(Lumi)
    #CMS_lumi.writeExtraText = 1
    #CMS_lumi.extraText = "Preliminary"

    #iPos = 11
    #if(iPos == 0):
    #    CMS_lumi.relPosX = 0.15

    #CMS_lumi.CMS_lumi(can_SM, 4, 11)
        
    os.system("mkdir -p %s/LimitResult/"%(os.getcwd()));
    os.system("mkdir -p %s/LimitResult/Limit_%s_sys%s/"%(os.getcwd(), options.signalmodel, options.Sys));

    curGraph_exp.SaveAs("./LimitResult/Limit_%s_sys%s/Lim%s.root"%(options.signalmodel, options.Sys, suffix));
    can_SM.SaveAs("./LimitResult/Limit_%s_sys%s/Lim%s.png"%(options.signalmodel, options.Sys, suffix));
    can_SM.SaveAs("./LimitResult/Limit_%s_sys%s/Lim%s.pdf"%(options.signalmodel, options.Sys, suffix));
    #can_SM.SaveAs("./LimitResult/Limit_sys%s/Lim%s.root"%(options.Sys, suffix));
    can_SM.SaveAs("./LimitResult/Limit_%s_sys%s/Lim%s.C"%(options.signalmodel, options.Sys, suffix));




    ROOT.gPad.SetLogx();
    hrl_SM.GetXaxis().SetMoreLogLabels()
    hrl_SM.GetXaxis().SetNoExponent()

    can_SM.Update();
    can_SM.RedrawAxis();
    can_SM.RedrawAxis("g");
    leg2.Draw();
    can_SM.Update();

    can_SM.SaveAs("./LimitResult/Limit_%s_sys%s/Lim%s_Logx.png"%(options.signalmodel, options.Sys, suffix));
    can_SM.SaveAs("./LimitResult/Limit_%s_sys%s/Lim%s_Logx.pdf"%(options.signalmodel, options.Sys, suffix));
    can_SM.SaveAs("./LimitResult/Limit_%s_sys%s/Lim%s_Logx.C"%(options.signalmodel, options.Sys, suffix));





#################
### Main Code ###    
#################
    
if __name__ == '__main__':

    
    CHAN = options.channel;
     
    moreCombineOpts = "";

    ### Set the working directory
    if options.computeLimits or options.plotLimits or options.closurechecks or options.diffNuisances or options.text2workspace or options.drawpostfit:
        #os.chdir("cards_B2GWW_closuretest0_HP_"+shape[0]);    
        os.chdir("cards_B2GWW");    
#        os.chdir("cards_B2GWW");

    ### put in functionality to test just one mass point or just one cprime

    nMasses = len(mass);
    mLo = 0;
    mHi = nMasses;

    if options.massPoint > 0:
        curIndex = mass.index(options.massPoint);
        mLo = curIndex;
        mHi = curIndex+1;

    cpLo = 1;
    cpHi = 2;

    ### Make cards option analysis
    if options.makeCards:
        for i in range(mLo,mHi):
            print "##################################################";
            print "##################################################";
            print "############# R U N N I N G F I T S ##############";
            print "mass = ",mass[i];
            print "###################################################";
            print "###################################################";
                
            time.sleep(0.3);
            command_makeCards = "python newstyle_B2GWW_doFit_class.py %s %s%03d %02d %02d %02d %02d %02d %02d %s %s -b -m %01d --inPath %s --category %s --masswindow %s --closuretest %01d  --realdata 1  --keepblind %01d -w %01d "%(CHAN,options.signalmodel, mass[i], ccmlo[i], ccmhi[i], mjlo[i], mjhi[i], mlo[i], mhi[i], shape[i], shapeAlt[i], 1, os.getcwd(), options.category,options.masswindow,options.closuretest, options.keepblind,  binwidth[i]);
            print command_makeCards ;

            if options.batchMode :
                fn = "fitScript_%s_%s_%03d_%s_%s"%(options.signalmodel, options.channel, mass[i], options.category, shape[i])
                submitBatchJob( command_makeCards, fn );
            if not options.batchMode: 
                print command_makeCards ;
                os.system(command_makeCards);
                 
    ### Compute Limits
    if options.computeLimits:

        for i in range(mLo,mHi):
            print "##################"+str(mass[i])+"#####################";
            time.sleep(0.3);
            ### Asymptotic Limit + profileLikelihood to have an hint of the r value
            if options.limitMode==0 and options.onlyCombine:
                if options.masswindow=="WZ" and options.channel!="em" and options.category!="HL":
                    cmd_comb= 'combineCards.py '
                    cmd_comb += 'wwlvj_%s%s_%s_%s_Z_unbin.txt ' %(options.signalmodel,mass[i],options.channel,options.category)
                    cmd_comb += 'wwlvj_%s%s_%s_%s_W_unbin.txt ' %(options.signalmodel,mass[i],options.channel,options.category)
                    cmd_comb += '> wwlvj_%s%s_%s_%s_WZ_unbin.txt'%(options.signalmodel,mass[i],options.channel,options.category)
                    print cmd_comb
                    os.system(cmd_comb)

                if options.channel=="em" and options.category!="HL":
                    cmd_comb= 'combineCards.py '
                    cmd_comb += 'wwlvj_%s%s_mu_%s_%s_unbin.txt ' %(options.signalmodel,mass[i],options.category,options.masswindow) 
                    cmd_comb += 'wwlvj_%s%s_el_%s_%s_unbin.txt ' %(options.signalmodel,mass[i],options.category,options.masswindow)
                    cmd_comb += '> wwlvj_%s%s_em_%s_%s_unbin.txt'%(options.signalmodel,mass[i],options.category,options.masswindow)
                    print cmd_comb
                    os.system(cmd_comb)

                if options.category=="HL":
                    cmd_comb= 'combineCards.py '
                    cmd_comb += 'wwlvj_%s%s_%s_HP_%s_unbin.txt ' %(options.signalmodel,mass[i],options.channel,options.masswindow)
                    cmd_comb += 'wwlvj_%s%s_%s_LP_%s_unbin.txt ' %(options.signalmodel,mass[i],options.channel,options.masswindow)
                    cmd_comb += '> wwlvj_%s%s_%s_HL_%s_unbin.txt'%(options.signalmodel,mass[i],options.channel,options.masswindow)
                    print cmd_comb
                    os.system(cmd_comb)

                #runCmmd2 = "combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -H ProfileLikelihood -m %03d -n _lim_%03d_%s_HP -d wwlvj_BulkGravWW%03d_%s_HP_unbin.txt -v 2 -S %d --run expected --rMax rMaxs[i]"%(mass[i],mass[i],options.channel ,mass[i],options.channel, options.Sys);
                #runCmmd2 = "combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -H ProfileLikelihood -m %03d -n _lim_%s%03d_%s_HP -d wwlvj_%s%03d_%s_HP_unbin.txt -v 2 -S %d --run expected "%(mass[i] ,options.signalmodel,mass[i],options.channel ,options.signalmodel ,mass[i],options.channel, options.Sys);
                #runCmmd2 = "combine -M Asymptotic --minimizerAlgo Minuit2 --minosAlgo stepping -H ProfileLikelihood -m %03d -n _lim_%s%03d_%s_HP_%s -d wwlvj_%s%03d_%s_HP_%s_unbin.txt -v 2 -S %d "%(mass[i] ,options.signalmodel,mass[i],options.channel,options.masswindow,options.signalmodel ,mass[i],options.channel, options.masswindow, options.Sys);###only for HP
            if options.limitMode==0 and not options.onlyCombine:
                runCmmd2 = "combine -M AsymptoticLimits --cminDefaultMinimizerType Minuit2 --minosAlgo stepping -m %03d -n _lim_%s%03d_%s_%s_%s -d wwlvj_%s%03d_%s_%s_%s_unbin.txt -v 2 -S %d "%(mass[i] ,options.signalmodel,mass[i],options.channel,options.category,options.masswindow,options.signalmodel ,mass[i],options.channel, options.category,options.masswindow, options.Sys);
#-H ProfileLikelihood
                print runCmmd2;
#                os.system(runCmmd2);
                if options.batchMode :
                    fn = "calScript_%s_%s_%03d_%s_%s"%(options.signalmodel, options.channel, mass[i], options.category, shape[i])
                    submitBatchJob( runCmmd2, fn );
                if not options.batchMode:
                    print runCmmd2;
                    os.system(runCmmd2);

                time.sleep(0.1);


            #elif options.limitMode==1:
            #  runCmmd2 = "combine -M ProfileLikelihood --significance --pvalue -m %03d -n _pval_obs_%03d_bb_%s_HP wwlvj_MWp_%03d_bb_%s_HP_unbin.txt\n"%(mass[i],mass[i],"mu",mass[i],"mu");
            #  runCmmd2 += "combine -M ProfileLikelihood --significance --pvalue -m %03d -n _pval_exp_%03d_bb_%s_HP wwlvj_MWp_%03d_bb_%s_HP_unbin.txt --expectSignal=1 --toysFreq -t -1"%(mass[i],mass[i],"mu",mass[i],"mu");

    ### make the plots    
    if options.plotLimits:
        doULPlot("_%s_%s_%s"%(options.channel,options.category,options.masswindow));

    if options.closurechecks:
        for i in range(mLo,mHi):
            print "##################"+str(mass[i])+"#####################";
            time.sleep(0.3);

            runCmmd3 = "combine -M MaxLikelihoodFit -t -1 --expectSignal %d -m %03d -n _closurechecks_%s%03d_%s_%s_%s_%d -d wwlvj_%s%03d_%s_%s_%s_unbin.txt -v 10"%(options.Bonly, mass[i] ,options.signalmodel,mass[i],options.channel,options.category,options.masswindow,options.Bonly,options.signalmodel ,mass[i],options.channel, options.category, options.masswindow);

            print runCmmd3;
            os.system(runCmmd3);
            time.sleep(0.1);

    if options.diffNuisances:
        for i in range(mLo,mHi):
            print "##################"+str(mass[i])+"#####################";
            time.sleep(0.3);

            runCmmd4 = "python diffNuisances_draw.py -a mlfit_closurechecks_%s%03d_%s_%s_%s_%d.root -g plots_closurechecks_%s%03d_%s_%s_%s_%d.root > plots_closurechecks_%s%03d_%s_%s_%s_%d.log"%(options.signalmodel,mass[i],options.channel,options.category,options.masswindow,options.Bonly,options.signalmodel ,mass[i],options.channel, options.category, options.masswindow,options.Bonly,options.signalmodel ,mass[i],options.channel, options.category, options.masswindow,options.Bonly);


            print runCmmd4;
            os.system(runCmmd4);
            time.sleep(0.1);

    if options.text2workspace:
        for i in range(mLo,mHi):
            print "##################"+str(mass[i])+"#####################";
            time.sleep(0.3);

            runCmmd5 = "text2workspace.py wwlvj_%s%03d_%s_%s_%s_unbin.txt -m %03d"%(options.signalmodel,mass[i],options.channel,options.category,options.masswindow,mass[i]);


            print runCmmd5;
            os.system(runCmmd5);
            time.sleep(0.1);

    if options.drawpostfit:
#        for i in range(mLo,mHi):
#            print "##################"+str(mass[i])+"#####################";
#            time.sleep(0.3);

            runCmmd6 = "combine -M MaxLikelihoodFit --expectSignal %d -m %03d -n _postfit_%s%03d_%s_%s_%s_%d -d wwlvj_%s%03d_%s_%s_%s_unbin.txt --plots --saveShapes --saveWithUncertainties -v 10"%(options.Bonly, 2000 ,options.signalmodel,2000,options.channel,options.category,options.masswindow,options.Bonly,options.signalmodel ,2000,options.channel, options.category, options.masswindow);

            print runCmmd6;
            os.system(runCmmd6);
            time.sleep(0.1);



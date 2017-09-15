#!/bin/bash
# cms software setup
export SCRAM_ARCH=slc6_amd64_gcc491
echo "working directory"
tar xvf loot.tar
cd CMSSW_7_1_25_patch1/src
eval `scramv1 runtime -sh`
cd ../../
cmsDriver.py LLP_SIGID_cff.py --fileout file:SIGID_step0_GENSIM_n0.root --mc --eventcontent RAWSIM --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring,SimG4Core/CustomPhysics/Exotica_HSCP_SIM_cfi,DisappTrks/SignalMC/genParticlePlusGeant.customizeProduce,DisappTrks/SignalMC/genParticlePlusGeant.customizeKeep --datatier GEN-SIM --conditions MCRUN2_71_V1::All --beamspot Realistic50ns13TeVCollision --step GEN,SIM --magField 38T_PostLS1 --python_filename SIGID_GENSIM.py --no_exec -n NUMEVENTS
python ShortTrackSusy/python/edit_config.py SIGID_GENSIM.py
bash ShortTrackSusy/python/replace_storage.sh SIGID_GENSIM.py SIGID_GENSIMb.py
mv SIGID_GENSIMb.py SIGID_GENSIM.py
cmsRun SIGID_GENSIM.py

cd CMSSW_8_0_21/src
eval `scramv1 runtime -sh`
cd ../../
cmsDriver.py step2 --filein file:SIGID_step0_GENSIM_10of10.root --fileout file:SIGID_step1_GSR_n0.root --mc --eventcontent RECOSIM --datatier GEN-SIM-RECO --conditions 80X_mcRun2_asymptotic_2016_v3 --step DIGI,L1,DIGI2RAW,HLT:@relval25ns,RAW2DIGI,L1Reco,RECO,EI --era Run2_25ns --python_filename SIGID_step2.py --customise Configuration/DataProcessing/Utils.addMonitoring,DisappTrks/SignalMC/genParticlePlusGeant.customizeProduce,DisappTrks/SignalMC/genParticlePlusGeant.customizeKeep -n NUMEVENTS

xrdcp SIGID_step1_GSR_n0.root root://cmseos.fnal.gov//store/user/sbein/FastSimDev/Full/gensimreco/

rm *.root

#try going back to scratch area before running code

## SUSY-centric disappearing tracks production

####  Instructions: the following commands entered in order should produce EDM files corresponding to an example signal benchmark defined by an slha file named pMSSM12_MCMC1_27_200970.slha, which is installed by default. To install another slha file for a different signal model and generate events, instructions are given at the bottom of the page. 

Initial setup
```
git clone https://github.com/ShortTrackSusy/ShortTrackSusy.git
mkdir jobs
mkdir jobs/logs
cp -r ShortTrackSusy/python .
cp ShortTrackSusy/template.* .
```

Needed for GENSIM:
```
cmsrel CMSSW_7_1_25_patch1
cd CMSSW_7_1_25_patch1/src
cmsenv
git-cms-addpkg SimG4Core/CustomPhysics
git-cms-addpkg Configuration/Generator
git-cms-addpkg SimG4Core/Application
cp ../../ShortTrackSusy/stuff/* Configuration/Generator/python
cp ../../ShortTrackSusy/stuff/Exotica_HSCP_SIM_cfi.py SimG4Core/CustomPhysics/python/Exotica_HSCP_SIM_cfi.py
cp ../../ShortTrackSusy/stuff/g4SimHits_cfi.py SimG4Core/Application/python/
cp -r ../../ShortTrackSusy/DisappTrks .
cp -r ../../ShortTrackSusy/Customise .
cp -r ../../ShortTrackSusy/SigPoints .
scram b
cd ../../
```

Produce a GENSIM file from existing SLHA file
```
cd CMSSW_7_1_25_patch1/src
cmsenv
cd ../..
cmsDriver.py LLP_pMSSM12_MCMC1_27_200970_cff.py --fileout file:pMSSM12_MCMC1_27_200970_step1_GENSIM.root --mc --eventcontent RAWSIM --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring,SimG4Core/CustomPhysics/Exotica_HSCP_SIM_cfi,DisappTrks/SignalMC/genParticlePlusGeant.customizeProduce,DisappTrks/SignalMC/genParticlePlusGeant.customizeKeep --datatier GEN-SIM --conditions MCRUN2_71_V1::All --beamspot Realistic50ns13TeVCollision --step GEN,SIM --magField 38T_PostLS1 --python_filename pMSSM12_MCMC1_27_200970_GENSIM.py --no_exec -n 10 
python python/edit_config.py pMSSM12_MCMC1_27_200970_GENSIM.py
cmsRun pMSSM12_MCMC1_27_200970_GENSIM.py
```

Setup to generate GENSIMRAW, AODSIM and miniAODSIM
```
cmsrel CMSSW_8_0_21
cd CMSSW_8_0_21/src
cmsenv
cp -r ../../ShortTrackSusy/DisappTrks .
scram b
cd ../../
```

Produce a GEN-SIM-RAW file from the previous output
```
cd CMSSW_8_0_21/src
cmsenv
cd ../../
voms-proxy-init -voms cms
cmsDriver.py step1 --filein file:pMSSM12_MCMC1_27_200970_step1_GENSIM.root --fileout file:pMSSM12_MCMC1_27_200970_GENSIMRAW.root --pileup_input dbs:/MinBias_TuneCUETP8M1_13TeV-pythia8/RunIISummer15GS-MCRUN2_71_V1-v2/GEN-SIM --mc --eventcontent RAWSIM --pileup 2015_25ns_FallMC_matchData_PoissonOOTPU --datatier GEN-SIM-RAW --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step DIGI,L1,DIGI2RAW,HLT:@frozen2016 --era Run2_2016 --python_filename pMSSM12_MCMC1_27_200970_GENSIMRAW.py --customise Configuration/DataProcessing/Utils.addMonitoring,DisappTrks/SignalMC/genParticlePlusGeant.customizeKeep,DisappTrks/SignalMC/genParticlePlusGeant.customizeProduce -n 10
```

Produce an AODSIM file from the previous output 
```
cd CMSSW_8_0_21/src
cmsenv
cd ../../
cmsDriver.py step2 --filein file:pMSSM12_MCMC1_27_200970_GENSIMRAW.root --fileout file:pMSSM12_MCMC1_27_200970_step2_AODSIM.root --mc --eventcontent AODSIM --runUnscheduled --datatier AODSIM --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step RAW2DIGI,RECO,EI --nThreads 4 --era Run2_2016 --python_filename AOD_cfg.py --customise Configuration/DataProcessing/Utils.addMonitoring,DisappTrks/SignalMC/genParticlePlusGeant.customizeProduce,DisappTrks/SignalMC/genParticlePlusGeant.customizeKeep -n 10
```

Produce a miniAODSIM file from the previous output 
```
cd CMSSW_8_0_21/src
cmsenv
cd ../../
cmsDriver.py step3 --conditions auto:run2_mc --fast --eventcontent MINIAODSIM --runUnscheduled --filein file:pMSSM12_MCMC1_27_200970_step2_AODSIM.root --fileout file:pMSSM12_MCMC1_27_200970_step3_miniAODSIM.root -s PAT --datatier MINIAODSIM --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --customise Configuration/DataProcessing/Utils.addMonitoring,DisappTrks/SignalMC/genParticlePlusGeant.customizeProduce,DisappTrks/SignalMC/genParticlePlusGeant.customizeKeep --mc -n 10
```


To test this procedure on another signal point for which there is an slha file with full path \<path to slha file\>, the following command can be run to install the slha file.
```
python python/installfrags.py <path to slha file>
cd CMSSW_7_1_25_patch1/src
cmsenv
scram b -j12
cmsenv
cd ../../
```
Then, the production commands given above can be run after replacing all instances of "pMSSM12_MCMC1_27_200970_step2_AODSIM" with the stem of the new slha file.

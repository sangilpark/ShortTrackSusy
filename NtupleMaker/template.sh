#!/bin/bash
# cms software setup
export SCRAM_ARCH=slc6_amd64_gcc491
echo "working directory"
cd NTUPLEDIR
eval `scramv1 runtime -sh`
cd ${_CONDOR_SCRATCH_DIR}

cmsRun runMakeTreeFromMiniAOD_cfg.py scenario=Summer16 dataset=root://cmsxrootd.fnal.gov//store/user/lpcsusyhad/sbein/LongLiveTheChi/miniaodsim/smallchunks/SIGID_step3_miniAODSIM_71of100.root outfile=SIGID_ntuple

xrdcp SIGID_ntuple_RA2AnalysisTree.root root://cmseos.fnal.gov//store/user/lpcsusyhad/sbein/LongLiveTheChi/ntuple/smallchunks/OUTFILENAME

rm *.py 
rm SIGID*.root

#try going back to scratch area before running code

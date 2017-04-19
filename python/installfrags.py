import os, sys

def main():
    #argument is the slha file to define the signal parameters
    try: slhaname = sys.argv[1]
    except: slhaname = 'DisTrack/SigPoints/benchmarks/pMSSM12_MCMC1_44_855871.slha'

    if slhaname == 'all': 
        from glob import glob
        slhas = glob('DisTrack/SigPoints/benchmarks/*.slha')
    else: slhas = [slhaname]

    print 'installing slha files', slhas
    #use working slha files as a template/basis
    templatekey = 'pMSSM12_MCMC1_27_200970'
    templateGen = 'CMSSW_7_1_25_patch1/src/Configuration/Generator/python/LLP_'+templatekey+'_cff.py'
    f = open(templateGen)
    fraglines = f.readlines()
    f.close()



    for slha in slhas:
        
        #grab templates for files to be edited
        frawslha = open(slha)
        slhalines = frawslha.readlines()
        frawslha.close()
        frawdecay = open('CMSSW_7_1_25_patch1/src/Customise/data/geant4_'+templatekey+'.slha')
        decaylines = frawdecay.readlines()
        frawdecay.close()        

        #copy and fix slha file for GEN step
        slhakey = slha[slha.rfind('/')+1:slha.rfind('.slha')]
        print 'slhakey=',slhakey
        fslha = open('CMSSW_7_1_25_patch1/src/SigPoints/'+slhakey+'.slha','w')
        armed2comment = False
        width = -1.0
        for slhaline in slhalines:
            if 'DECAY   1000024' in slhaline:
                armed2comment = True
                width = slhaline.split()[2]
            if armed2comment and '#         PDG' in slhaline: armed2comment = False
            if armed2comment: fslha.write('#'+slhaline)
            else: fslha.write(slhaline)
        print 'determined width =',width
        fslha.close()

        #copy and fix slha fragment file for SIM step
        fdecay = open('CMSSW_7_1_25_patch1/src/Customise/data/geant4_'+slhakey+'.slha','w')
        for decayline in decaylines:
            if ('DECAY  -1000024' in decayline) or ('DECAY  1000024' in decayline):
                undesirable = decayline.split()[2]
                fdecay.write(decayline.replace(undesirable,width))
            else: fdecay.write(decayline)
        fdecay.close()

        #create the new frag itself
        ffrag = open(templateGen.replace(templatekey,slhakey),'w')
        for fragline in fraglines:
            ffrag.write(fragline.replace(templatekey,slhakey))
        print 'check created frag:', 'CMSSW_7_1_25_patch1/src/Configuration/Generator/python/LLP_'+slhakey+'_cff.py'
        print ''
        print 'to test full production interactively, do'
        print what2donext.replace(templatekey,slhakey)



what2donext = '''
echo Now producing GEN-SIM for pMSSM12_MCMC1_27_200970
cd CMSSW_7_1_25_patch1/src
cmsenv
cd ../../
cmsDriver.py LLP_pMSSM12_MCMC1_27_200970_cff.py --fileout file:pMSSM12_MCMC1_27_200970_step1_GENSIM.root --mc --eventcontent RAWSIM --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring,SimG4Core/CustomPhysics/Exotica_HSCP_SIM_cfi,DisappTrks/SignalMC/genParticlePlusGeant.customizeProduce,DisappTrks/SignalMC/genParticlePlusGeant.customizeKeep --datatier GEN-SIM --conditions MCRUN2_71_V1::All --beamspot Realistic50ns13TeVCollision --step GEN,SIM --magField 38T_PostLS1 --python_filename pMSSM12_MCMC1_27_200970_GENSIM.py -n 10

echo Now producing GEN-SIM-RAW for pMSSM12_MCMC1_27_200970
cd CMSSW_8_0_21/src
cmsenv
cd ../../
cmsDriver.py step1 --filein file:pMSSM12_MCMC1_27_200970_step1_GENSIM.root --fileout file:pMSSM12_MCMC1_27_200970_GENSIMRAW.root --pileup_input dbs:/MinBias_TuneCUETP8M1_13TeV-pythia8/RunIISummer15GS-MCRUN2_71_V1-v2/GEN-SIM --mc --eventcontent RAWSIM --pileup 2015_25ns_FallMC_matchData_PoissonOOTPU --datatier GEN-SIM-RAW --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step DIGI,L1,DIGI2RAW,HLT:@frozen2016 --era Run2_2016 --python_filename pMSSM12_MCMC1_27_200970_GENSIMRAW.py --customise Configuration/DataProcessing/Utils.addMonitoring,DisappTrks/SignalMC/genParticlePlusGeant.customizeKeep,DisappTrks/SignalMC/genParticlePlusGeant.customizeProduce -n 10

echo Now producing AODSIM for pMSSM12_MCMC1_27_200970
cmsDriver.py step2 --filein file:pMSSM12_MCMC1_27_200970_GENSIMRAW.root --fileout file:pMSSM12_MCMC1_27_200970_step2_AODSIM.root --mc --eventcontent AODSIM --runUnscheduled --datatier AODSIM --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step RAW2DIGI,RECO,EI --nThreads 4 --era Run2_2016 --python_filename AOD_cfg.py --customise Configuration/DataProcessing/Utils.addMonitoring,DisappTrks/SignalMC/genParticlePlusGeant.customizeProduce,DisappTrks/SignalMC/genParticlePlusGeant.customizeKeep -n 10

echo Now producing MINIAODSIM for pMSSM12_MCMC1_27_200970
cmsDriver.py step3 --conditions auto:run2_mc --fast --eventcontent MINIAODSIM --runUnscheduled --filein file:pMSSM12_MCMC1_27_200970_step2_AODSIM.root --fileout file:pMSSM12_MCMC1_27_200970_step3_miniAODSIM.root -s PAT --datatier MINIAODSIM --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --customise Configuration/DataProcessing/Utils.addMonitoring,DisappTrks/SignalMC/genParticlePlusGeant.customizeProduce,DisappTrks/SignalMC/genParticlePlusGeant.customizeKeep --mc -n 10
'''

main()

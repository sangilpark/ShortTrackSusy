import os, sys
from glob import glob

dirStem=os.getcwd()
print 'DIRSTEM=',dirStem

ntuplizerdir='/uscms_data/d3/sbein/LongLiveTheChi/19Apr2017/NtupleMaker/CMSSW_8_0_25/src/TreeMaker/Production/test'
if not os.path.exists(ntuplizerdir):
    print 'no such directory :(', ntuplizerdir
    exit(0)

try: minisourcedir = sys.argv[1]
except: minisourcedir = '/eos/uscms/store/user/lpcsusyhad/sbein//LongLiveTheChi/miniaodsim/smallchunks/'

filelist = glob(minisourcedir+'/*.root')

JDLtemplate = open(dirStem+'/template.jdl')
JDLtemplines = JDLtemplate.readlines()
JDLtemplate.close()

SHtemplate = open(dirStem+'/template.sh')
SHtemplines = SHtemplate.readlines()
SHtemplate.close()

for filename in filelist[:999999]:
    outname = filename.replace('step3_miniAODSIM','ntuple_RA2AnalysisTree').replace('miniaodsim','ntuple')
    if os.path.exists(outname):continue
    else:  
        print 'nothing to delete here yet!', outname    
    if filename[-1]=='/': filename = filename[:-2]
    print 'filename', filename
    partialname = filename[filename.rfind('/')+1:]
    print 'partialname', partialname
    sigid, jobposition = partialname.split('_step3_miniAODSIM_')
    jobposition=jobposition.replace('.root','')
    print 'determined sigid, jobpostion =', sigid, jobposition
    job = 'job_'+partialname.replace('.root','')
    print 'creating jobs:',job

    outname = outname[outname.rfind('/')+1:]
    newjdl = open('jobs/'+job+'.jdl','w')
    for jdlline in JDLtemplines:
        if 'template' in jdlline:
            jdlline = jdlline.replace('template', job)
        newjdl.write(jdlline)
    newjdl.close()
    newsh = open('jobs/'+job+'.sh','w')
    for shline in SHtemplines:
        if 'template' in shline:
            shline=shline.replace('template',job)
        if 'WORKINGDIR' in shline:
            shline=shline.replace('WORKINGDIR',dirStem)            
        if 'SIGID' in shline:
            shline=shline.replace('SIGID',sigid)
        if 'OUTFILENAME' in shline:
            shline=shline.replace('OUTFILENAME',outname)
        if 'NUMEVENTS' in shline:
            shline=shline.replace('NUMEVENTS',str(numevents))
        if 'NTUPLEDIR' in shline:
            shline=shline.replace('NTUPLEDIR',ntuplizerdir)
        if 'JOBPOSITION' in shline:
            shline=shline.replace('JOBPOSITION',jobposition)
        newsh.write(shline)
    newsh.close()

    cmd =  'condor_submit jobs/'+job+'.jdl'
    print cmd
    os.system(cmd)

print 'done'

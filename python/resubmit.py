from glob import glob
import os, sys

try: slhaid = sys.argv[1]
except: slhaid = 'pMSSM12_MCMC1_8_373637'

errlist = glob('jobs/logs/*.err')
nresub = 0
for err in errlist:
    f = open(err)
    lines = f.readlines()
    f.close()
    needsresubmitting = False
    for line in lines:
        if 'Begin Fatal Exception' in line: 
            needsresubmitting = True
            break
    if needsresubmitting:
        command = 'condor_submit '+err.replace('/logs','').replace('.err','.jdl')
        print command
        os.system(command)
        nresub+=1
        
print 'n(resub) =',nresub
        


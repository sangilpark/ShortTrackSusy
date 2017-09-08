import os, sys
from glob import glob

TestMode = False

errlist = glob('jobs/logs/*.err')
nresub = 0
f2del = []
for err in errlist:
    f = open(err)
    lines = f.readlines()
    f.close()
    needsresubmitting = False
    for line in lines:
        if 'Begin Fatal Exception' in line: 
            needsresubmitting = True
            break
        if '[ERROR] Server responded with an error:' in line: 
            needsresubmitting=True
            if '[3006]' in line:
                f2d = line.split('Unable to create file')[1].split(';')[0].strip()
                dcommand = 'rm '+f2d
                print dcommand
                if not TestMode: 
                    print 'deleting'
                    os.system(dcommand)
            else: print 'other issue', line
            #
            break
    if needsresubmitting:
        command = 'condor_submit '+err.replace('/logs','').replace('.err','.jdl')
        print command
        if not TestMode:
            os.system(command)
        nresub+=1

print 'n(resub) first =',nresub
loglist = glob('jobs/logs/*.log')
nresub=0
for log in loglist:
    f = open(log)
    lines = f.readlines()
    f.close()
    needsresubmitting = False
    for line in lines:
        if 'aborted' in line: 
            needsresubmitting = True
            break
    if needsresubmitting:
        command = 'condor_submit '+log.replace('/logs','').replace('.log','.jdl')
        print command
        if not TestMode:
            os.system('rm '+log)
            os.system(command)
        nresub+=1		

print 'n(resub) abort =',nresub




import os, sys

FredBlurb = '''
from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper
randSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)
randSvc.populate()
#process.source.firstLiminosityBlock = cms.untracked.uint32(1 + seed)
'''


try: cname = sys.argv[1]
except: cname = 'nonexistent.py'

f = open(cname)
lines = f.readlines()
f.close()

fnew = open('2'+cname,'w')
armed = False
for line in lines:
    if 'process = cms.Process(' in line: armed = True
    fnew.write(line)
    if armed:
        fnew.write(FredBlurb)
        armed = False
    

os.system('mv 2'+cname+' '+cname)

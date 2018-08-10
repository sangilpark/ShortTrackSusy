import os, sys
import time

dirStem=os.getcwd()
print 'DIRSTEM=',dirStem

try: sigid = sys.argv[1].replace('.slha','')
except: sigid = 'pMSSM12_MCMC1_27_200970'
try: numevents = int(sys.argv[3])
except: numevents = 8
try: numjobs = int(sys.argv[2])
except: numjobs = 1

if not os.path.exists('CMSSW_7_1_25_patch1/src/Configuration/Generator/python/LLP_'+sigid+'_cff.py'):
	print 'no frag called CMSSW_7_1_25_patch1/src/Configuration/Generator/python/LLP_'+sigid+'_cff.py'
	print 'please run python/installfrags.py <slha file name> to install fragments'
	exit(0)

if not os.path.exists('jobs/'+sigid):
    print 'creating a new jobs directory'
    os.system('mkdir -p jobs/'+sigid+'/logs jobs/outputs')

if not os.path.exists('loot.tar'):
    print 'creating a new tar file'
    os.system('tar -cvf loot.tar CMSSW_7_1_25_patch1 CMSSW_8_0_21')
else: print 'using existing tar file'

#JDLtemplate = open(dirStem+'/template.jdl')
#JDLtemplines = JDLtemplate.readlines()
#JDLtemplate.close()

SHtemplate = open(dirStem+'/template_PBS.sh')
SHtemplines = SHtemplate.readlines()
SHtemplate.close()

for nj in range(1,numjobs+1):
	job = 'job_'+sigid+'_'+str(nj)+'of'+str(numjobs)
	print 'creating jobs:',job

	#newjdl = open('jobs/'+job+'.jdl','w')
	#for jdlline in JDLtemplines:
	#	if 'template' in jdlline:
	#		jdlline = jdlline.replace('template', job)
	#	newjdl.write(jdlline)
	#newjdl.close()
	newsh = open('jobs/'+sigid+'/'+job+'.sh','w')
	for shline in SHtemplines:
		if 'template' in shline:
			shline=shline.replace('template',job)
		if 'WORKINGDIR' in shline:
			shline=shline.replace('WORKINGDIR',dirStem)            
		if 'SIGID' in shline:
			shline=shline.replace('SIGID',sigid)
		if '_n0' in shline:
			shline=shline.replace('_n0','_'+str(nj)+'of'+str(numjobs))
		if 'NUMEVENTS' in shline:
			shline=shline.replace('NUMEVENTS',str(numevents))
		newsh.write(shline)
	newsh.close()

	cmd_chmod =  'chmod u+x jobs/'+sigid+'/'+job+'.sh'
	os.system(cmd_chmod)
	cmd_submit =  'qsub -q cms jobs/'+sigid+'/'+job+'.sh'
	print cmd_submit
	#os.system(cmd_submit)
	#time.sleep(0.5)
    
print 'done'

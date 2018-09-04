#!/usr/bin/env
import logging

#my own watchdog program
#read config file

def sysType():
	"""
	selects between the two main systems this would run on, either a pi with user pi or another machine
	with user chadg
	"""
	global G_SYSTEM
	if os.path.isdir("/home/pi"):
		G_SYSTEM="pi"
		setSetting("system","pi")
	else:
		G_SYSTEM="chadg"

sysType()
FORMAT='%(levelname)s %(asctime)s %(threadName)s : %(message)s'
LOGFILE='/home/'+G_SYSTEM+'/logs/wd.log'
log=logging.getLogger(__name__)
logging.basicConfig(format=FORMAT,datefmt='%m-%d-%y %H:%M:%S',filename=LOGFILE,level=logging.DEBUG)
log.info('Logging Started')

try:
	f=open("wd.conf","r")
except:
	log.error("Could not open wd.conf")
	exit()

pidFiles=[]
programFiles=[]
data=f.read().split("\n")
for line in data:
	if line.strip()=="":
		continue
	if "pidfile" in line:
		pidFiles.append(line.split("=")[1]
	if "programfile" in line:
		programFiles.append(line.split("=")[1]
f.close()
if len(pidFiles)!=len(programFiles):
	log.error("Error Parsing config file")

for index in range(len(pidfiles)):
	try:
		f=open(pid[index],"w")
		f.close()
		#we were able to open it, so it must not be running
		pid=os.spawnl(os.P_NOWAIT,programFiles[index])
		log.info("Started "+programFiles[index]+" with pid: "+str(pid))
	except:
		log.info(pid+" file is locked....
"""
Config file example data

[Name]
pidfile:/path/to/pid/file
programfile:/path/to/program/file
"""

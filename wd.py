#!/usr/bin/env python
import logging as log
import os
import sys
import subprocess
import filelock


#my own watchdog program
#read config file

G_SYSTEM=""
if os.path.isdir("/home/pi"):
	G_SYSTEM="pi"
else:
	G_SYSTEM="chadg"
FORMAT='%(levelname)s %(asctime)s %(threadName)s : %(message)s'
LOGFILE='/home/'+G_SYSTEM+'/logs/wd.log'
log.basicConfig(format=FORMAT,datefmt='%m-%d-%y %H:%M:%S',filename=LOGFILE,level=log.INFO)
log.info('Logging Started')

try:
	f=open("/home/"+G_SYSTEM+"/WD/wd.conf","r")
	log.info("wd.conf open")
	log.info("\n\n\n")
except:
	log.error("Could not open wd.conf")
	exit()

pidFiles=[]
programFiles=[]
logFiles=[]
data=f.read().split("\n")
f.close()
for line in data:
	try:
		line=line.strip()
		if line=="":
			continue
		if line[0]=='#':
			continue
		if "pidfile" in line:
			pidFiles.append(line.split("==")[1])
		if "programfile" in line:
			programFiles.append(line.split("==")[1])
		if "logfile" in line:
			logFiles.append(line.split("==")[1])
	except:
		log.error("Failed to parse wd.conf")
		log.error(sys.exc_info())
		exit()
if len(pidFiles)!=len(programFiles) or len(pidFiles)!=len(logFiles):
	log.error("Error Parsing config file")
	exit()
	
log.info("Found "+str(len(pidFiles))+ " programs to check from wd.conf")
for index in range(len(pidFiles)):
	try:
		lock=filelock.FileLock(pidFiles[index])
		lock.timeout=1
		#will throw an exception if lock is not acquired
		lock.acquire()
		lock.release()
		log.warning("Starting "+ programFiles[index])
		#we were able to open it, so it must not be running
		try:
			cur_env=os.environ.copy()
			cur_env["DISPLAY"]=":0"
			subprocess.Popen(programFiles[index].split(" "),env=cur_env)
		except:
			log.error("Failed to start program")
			log.error(programFiles[index].split(" "))
			log.error(sys.exc_info())
	except:
		log.info(pidFiles[index]+" already running")
		
"""
Config file example data

[Name]
pidfile:/path/to/pid/file
logfile:/path/to/log/file
programfile:/path/to/program/file
"""

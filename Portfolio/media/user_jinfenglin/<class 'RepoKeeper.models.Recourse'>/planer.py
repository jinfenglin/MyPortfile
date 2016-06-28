import threading
import sys,getopt
import re,time
from paramiko import SSHClient,AutoAddPolicy
class Planer:
	''' this version use 1 thread to listen on server, and 1 thread to submit command. 
	Another easier  way to do it is loop {'check server: wait for connection'->'submit'}''' 
	def __init__(self,argv):
		self.shareLock = threading.Lock()
		self.oath = True

		try:
			opts,args = getopt.getopt(argv,"hl:s:",["list=","server="]) #maybe passwd, username as well
		except getopt.GetoptError:
			print "planer.py -l <listfile> -s <server>"
			sys.exit(2)
		for opt,arg in opts:
			if opt == '-h':
				print "planer helps to run a test on local server when you are off"
			elif opt in ("-l","--list"):
				#read the file
				self.suiteDict = self.readSuiteList(arg)
			elif opt in ("-s","--server"):
				self.cluster= arg
		self.ssh = SSHClient()
		self.ssh.load_system_host_keys()
		self.ssh.connect(self.cluster,username='root')

	def readSuiteList(self,path):
		suiteDict={}
		with open (path) as infile:
			for line in infile:
				line = line.strip('\t\n\r')
				parts = re.split('[:,]',line) 
				parts = filter(lambda x: len(x)>0,parts)
				suiteDict[parts[0]]=parts[1:]
		return suiteDict
	def run(self):
		print "Suite testcase num"
		for key in self.suiteDict:
			ls = self.suiteDict[key]
			print key,ls,len(ls)
		#one thread listening from server 
		#another one submit work
		print "My watch starts"
		self.shareLock.acquire()

		submitter = threading.Thread(target=self.commandSubmitter );
		submitter.start()
		while(self.oath):
			stdin, stdout, stderr=self.ssh.exec_command('service grinder-atf status')
			feedback = stdout.readline()
			#print "feedback:",feedback
			if 'now waiting for client connection' in feedback:
				if self.shareLock.locked():
					print "lock realease"
					self.shareLock.release()
			else:
				if not self.shareLock.locked():
					self.shareLock.acquire()
					print "lock acquire"
		self.ssh.close()
	
		print "My watch is ended"

	def commandMaker(self,script,testname = None):
		cmd = ["/home/grinder/bin/gclient.py", "--product=ANYWHERE",'-s',script,'--branch=draper_tweener','--test_branch==draper_tweener','--uselocal','--noinstall']
		if testname is not None:
			cmd.append('--singletest='+testname)
		return cmd

	def commandSubmitter(self):
		work=0
		for key in self.suiteDict:
			tests = self.suiteDict[key]
			if len(tests) == 0:
				cmd = ' '.join(self.commandMaker(key))
				with self.shareLock:
					print "Submitting:",cmd
					stdin,stdout,stderr = self.ssh.exec_command(cmd)
					print "print err:",stderr.read()
				print "lock release"
				time.sleep(5)
			else:
				for test in tests:
					cmd = ' '.join(self.commandMaker(key,test))
					with self.shareLock:
						print "Submitting:",cmd
						self.ssh.exec_command(cmd)
					print "lock release"
					time.sleep(5)

		self.oath = False


if __name__=="__main__":
	planer= Planer(sys.argv[1:])
	planer.run()

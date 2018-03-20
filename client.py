import sys, os, socket, package, subprocess, _thread, time, requests
from functools import cmp_to_key

class Client:

	def getAddressList(self):
		l = subprocess.check_output(['ifconfig']).decode(encoding='ascii', errors='ignore').split('\n\n')
		ret = []
		for interface in l:
			if(len(interface.split('HWaddr'))==2):
				try:
					ret.append(interface.split('Bcast:')[1].split()[0])
				except:
					pass

		return ret

	def cmp(self, a, b):
		a = a[1].split('.')
		b = b[1].split('.')
		aLength = len(a)
		bLength = len(b)
		i = 0
		while i < aLength and i < bLength:
			if int(a[i]) < int(b[i]):
				return -1
			elif int(a[i]) > int(b[i]):
				return 1
			i += 1
		return 0

	def __init__(self, message):
		
		if len(message) == 0:
			print('Compulsory argument <package name> missing')
			exit(1)

		try:
			for i in range(len(message)):
				self.CWD = os.getcwd()
				self.versionList = []
				self.downloadingList = []
				self._main(message[i])
		except Exception as e:
			print(e)
			exit()
		os.chdir('/var/cache/apt/archives')
		print("Updating your packages list for distribution.")
		FNULL = open(os.devnull, 'w')
		subprocess.call("dpkg-scanpackages . /dev/null | gzip -9c > Packages.gz", stdout=FNULL, stderr=FNULL, shell=True)
		package.packageListGenerator(self.CWD)
		print("Completed.")

	def broadcast(self, broadcast_addr, message):

		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

		server_address = (broadcast_addr, 10000)

		print('Broadcasted to <'+broadcast_addr+'>: ', message)

		sent = sock.sendto(message.encode(), server_address)

		sock.close()

		self.threadCount -= 1

	def replyHandler(self, conn, address):
		data = conn.recv(1000000)
		data = data.decode()
		print("Received: ",end="")
		print(data,end=" ")
		print("From: ", end="")
		print(address[0])
		if(data[0]=='H'):
			self.versionList.append((address[0], data[2:]))
		else:
			self.downloadingList.append((address[0], data[2:]))

	def listen(self):
		sock = socket.socket()
		sock.settimeout(5)
		sock.bind(('', 22653))
		sock.listen(100)
		print("Listening for replies..")
		try:
			while True:
				conn, address = sock.accept()     
				_thread.start_new_thread(self.replyHandler,(conn, address))

		except Exception as e:
			print(e)
			print("Network successfully checked for the package.")

		sock.close()
		self.threadCount -= 1

	def _main(self, message):

		message = '?' + message
		baddr_list = self.getAddressList()

		print('Searching in Local Network...')

		# latestVersion = '0.0.0'
		# localRepo = ''
		self.versionList = []
		self.downloadingList = []
		
		_thread.start_new_thread(self.listen, ())
		time.sleep(1)
		self.threadCount = 1
		for i in baddr_list:
			self.threadCount += 1 #Warning. Keep this line before anything else
			_thread.start_new_thread(self.broadcast, (i, message))

		while self.threadCount!=0:
			pass
		
		self.versionList.sort(key = cmp_to_key(self.cmp), reverse = True)

		apt_preperation_complete = False

		lines_modified = 0

		if len(self.downloadingList) != 0:
			print("Someone is already downloading the latest packages..")
			wait = 1
			download_complete = False
			while wait<=10:
				time.sleep(wait)
				res = dict()
				try:
					res = requests.get("http://"+str(self.downloadingList[0][0])+":35622/current_downloads.conf")
				except Exception as e:
					print(e)
					pass

				print(res.text)
				
				if res.status_code!=200 or res.text!=message[1:]:
					download_complete = True
					break

				wait *= 2

			if download_complete:
				print("Latest downloaded version:", self.downloadingList[0][1])
				sourcesFile = open('/etc/apt/sources.list', 'r+')
				sourcesLine = sourcesFile.readlines()
				newRepoString = ''
				for version in self.downloadingList:
					newRepoString += ('deb http://%s:35622/ ./\n' % version[0])
					lines_modified += 1
				print("Adding repo(s) : ", newRepoString)
				newRepo = [newRepoString]
				finalSourcesLines = newRepo + sourcesLine
				sourcesFile.seek(0)
				sourcesFile.writelines(finalSourcesLines)
				sourcesFile.truncate()
				sourcesFile.close()
				print("Running APT repositories list update.")
				FNULL = open(os.devnull, 'w')
				subprocess.call("apt-get update", stdout=FNULL, stderr=FNULL, shell=True)
				print("APT repository list update complete.")
				apt_preperation_complete = True


		if len(self.versionList) != 0 and apt_preperation_complete==False:
			print("Latest available version:", self.versionList[0][1])
			sourcesFile = open('/etc/apt/sources.list', 'r+')
			sourcesLine = sourcesFile.readlines()
			newRepoString = ''
			for version in self.versionList:
				newRepoString += ('deb http://%s:35622/ ./\n' % version[0])
				lines_modified += 1
			print("Adding repo(s) : ", newRepoString)
			newRepo = [newRepoString]
			finalSourcesLines = newRepo + sourcesLine
			sourcesFile.seek(0)
			sourcesFile.writelines(finalSourcesLines)
			sourcesFile.truncate()
			sourcesFile.close()
			print("Running APT repositories list update.")
			FNULL = open(os.devnull, 'w')
			subprocess.call("apt-get update", stdout=FNULL, stderr=FNULL, shell=True)
			print("APT repository list update complete.")
			apt_preperation_complete = True

		if apt_preperation_complete==False:
			print('File not found locally...\nDownloading from the Internet')
			f = open('/var/cache/apt/archives/current_downloads.conf','w')
			f.write(message[1:])
			f.close()



		os.system('apt-get install %s --allow-unauthenticated' % message[1:])
		#f = open('/var/cache/apt/archives/current_downloads.conf','w')
		#f.write("")
		#f.close()

		if len(self.versionList) != 0:
			sourcesFile = open('/etc/apt/sources.list', 'r+')
			sourcesLine = sourcesFile.readlines()
			for i in range(0, lines_modified):
				del sourcesLine[0]
			sourcesFile.seek(0)
			sourcesFile.writelines(sourcesLine)
			sourcesFile.truncate()
			sourcesFile.close()

if __name__ == '__main__':
	try:
		if sys.argv[1] == 'install':
			Client(sys.argv[2:])
		elif sys.argv[1] == 'remove':
			for i in range(2, len(sys.argv)):
				os.system('apt-get remove %s' % sys.argv[i])
		else:
			print('Invalid command')
	except:
		print('Required command missing')
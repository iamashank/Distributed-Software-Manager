import sys, os, socket, package
from functools import cmp_to_key

class Client:

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
			exit()

		try:
			for i in range(len(message)):
				self._main(message[i])
		except Exception as e:
			print(e)
			exit()
		self.CWD = os.getcwd()
		os.chdir('/var/cache/apt/archives')
		os.system('dpkg-scanpackages . /dev/null | gzip -9c > Packages.gz') 
		package.packageListGenerator(self.CWD)


	def _main(self, message):

		message = '?' + message

		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		server_address = ('192.168.43.255', 10000)

		print('Broadcast: ', message)

		sent = sock.sendto(message.encode(), server_address)

		sock.close()

		# latestVersion = '0.0.0'
		# localRepo = ''
		versionList = []

		print('Searching in Local Network...')

		sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock1.settimeout(5)

		server_address = ('', 22653)

		sock1.bind(server_address)

		try:
			while True:
				data, address = sock1.recvfrom(1000000)
				data = data.decode()
				print("Received:",data)
				versionList.append((address[0], data))

		except Exception as e:
			print(e)
		versionList.sort(key = cmp_to_key(self.cmp), reverse = True)

		if len(versionList) != 0:
			print("Latest available version:", versionList[-1][1])
			sourcesFile = open('/etc/apt/sources.list', 'r+')
			sourcesLine = sourcesFile.readlines()
			newRepoString = ''
			for version in versionList:
				newRepoString += ('deb http://%s:35622/ ./\n' % version[0])
			print ("Adding repo(s) : ", newRepoString)
			newRepo = [newRepoString]
			# newRepo = [ 'deb http://%s:35622/ ./\n' % localRepo ]
			finalSourcesLines = newRepo + sourcesLine
			sourcesFile.seek(0)
			sourcesFile.writelines(finalSourcesLines)
			sourcesFile.truncate()
			sourcesFile.close()
			os.system('apt-get update')
		else:
			 print('File not found locally...\nDownloading from the Internet')

		os.system('apt-get install %s --allow-unauthenticated' % message[1:])

		if len(versionList) != 0:
			sourcesFile = open('/etc/apt/sources.list', 'r+')
			sourcesLine = sourcesFile.readlines()
			for i in range(0, len(versionList)):
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
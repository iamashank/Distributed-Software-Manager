import socket, sys, os, pickle, _thread, subprocess, time, gzip, package, http.server, socketserver
from client import Client

class Server:

	def __init__(self):
		self.repo_server_failure = False
		self.CWD = os.getcwd()
		os.chdir("/var/cache/apt/archives")
		self._main()


	def repoServer(self):

		PORT = 35622

		try:
			Handler = http.server.SimpleHTTPRequestHandler
			httpd = socketserver.TCPServer(("", PORT), Handler)
			httpd.serve_forever()
			# print("Serving repo at port", PORT)
		except:
			self.repo_server_failure = True
			print('Port is already in use. Cannot start Repository Server.')


	def setupRepo(self):
		# print(os.getcwd())
		FNULL = open(os.devnull, 'w')
		subprocess.call("apt-get install net-tools", stdout=FNULL, stderr=FNULL, shell=True)
		Client(['dpkg-dev'])
		# os.system("apt-get install dpkg-dev")
		os.system("dpkg-scanpackages . /dev/null | gzip -9c > Packages.gz")
		os.system("apt-get update")
		package.packageListGenerator(self.CWD)



	def handle_requests(self, data, addr, sock):

		# global CWD
		sock = socket.socket()
		data = data.decode(encoding='ascii', errors='ignore')
		if(data[0]!='?'):
			sock.connect((addr[0], 22653))
			sock.send("Incorrect message format".encode())
			sock.close()
		else:
			data = data[1:]
			res = "" 
			try:
				l = open(self.CWD+'/packages.conf','r').readlines()
				found = False
				for i in l:
					try:
						name, version = i.split()
						if(name == data):
							print("Sent version :", version)
							sock.connect((addr[0], 22653))
							sock.send(("H:"+version).encode())
							sock.close()
							found = True
							break
					except Exception as e:
						pass
				if not found:
					try:
						print("fdvsdvf")
						f = open('/var/cache/apt/archives/current_downloads.conf','r')
						if(f.read()==data):
							print("Currently downloading that file..")
							print("Sent version :", version)
							sock.connect((addr[0], 22653))
							sock.send(("D:"+version).encode())
							sock.close()
						f.close()
					except Exception as e:
						pass
			except Exception as e:
				package.packageListGenerator(self.CWD)
				pass

	def _main(self):
		d = dict()

		try:
			f = open(self.CWD+'/server.conf','rb')
			d = pickle.load(f)
			if(('dpkg' not in d) or ( d['dpkg']==False)):
				self.setupRepo()
				f = open(self.CWD+'/server.conf','wb+')
				d = {'dpkg': True}
				pickle.dump(d, f)
				f.close()
		except:
			self.setupRepo()
			f = open(self.CWD+'/server.conf','wb+')
			d = {'dpkg': True}
			pickle.dump(d, f)
			f.close()

		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		server_address = ('', 10000)

		try:
			sock.bind(server_address)
		except:
			print('Port 10000 is already in use')
			exit()


		_thread.start_new_thread(self.repoServer,())

		time.sleep(1)

		if(self.repo_server_failure==True):
			exit()

		while True:
			print('Listening at port 10000..')
			data, addr = sock.recvfrom(409600)
			print('Received request for : ', data)
			_thread.start_new_thread(self.handle_requests,(data, addr, sock))

	

if __name__ == '__main__':
	Server()

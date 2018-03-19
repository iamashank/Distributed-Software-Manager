import socket, sys, os, pickle, _thread, subprocess, time, gzip, package, http.server, socketserver

repo_server_failure = False
CWD = os.getcwd()
os.chdir("/var/cache/apt/archives")

def repoServer():

	global repo_server_failure

	PORT = 35622

	try:
		Handler = http.server.SimpleHTTPRequestHandler
		httpd = socketserver.TCPServer(("", PORT), Handler)
		httpd.serve_forever()
		print("Serving repo at port", PORT)
	except:
		print('Port is already in use. Cannot start Repository Server.')
		repo_server_failure = True


def setupRepo():
	print(os.getcwd())
	os.system("apt-get install dpkg-dev")
	os.system("dpkg-scanpackages . /dev/null | gzip -9c > Packages.gz")
	os.system("apt-get update")
	package.packageListGenerator(CWD)



def handle_requests(data, addr, sock):

	global CWD

	data = data.decode(encoding='ascii', errors='ignore')
	if(data[0]!='?'):
		sock.sendto("Incorrect message format".encode(), addr)
	else:
		data = data[1:]
		addr = (addr[0], 22653)
		res = ""
		try:
			l = open(CWD+'/packages.conf','r').read().split('\n')
			for i in l:
				name, version = i.split()
				if(name == data):
					sock.sendto(version.encode(), addr)
					break
		except Exception as e:
			package.packageListGenerator()
			print(e)
			pass

d = dict()

try:
	f = open(CWD+'/server.conf','rb')
	d = pickle.load(f)
	if(('dpkg' not in d) or ( d['dpkg']==False)):
		setupRepo()
		f = open(CWD+'/server.conf','wb+')
		d = {'dpkg': True}
		pickle.dump(d, f)
		f.close()
except:
	setupRepo()
	f = open(CWD+'/server.conf','wb+')
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


_thread.start_new_thread(repoServer,())

time.sleep(1)

if(repo_server_failure==True):
	exit()

while True:
	print('Listening at port 10000..')
	data, addr = sock.recvfrom(409600)
	_thread.start_new_thread(handle_requests,(data, addr, sock))

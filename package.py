import gzip, shutil, tempfile, sys

def packageListGenerator(CWD):

	packages = []

	with gzip.open('/var/cache/apt/archives/Packages.gz', 'rb') as f_in:
		fp = tempfile.TemporaryFile()
		shutil.copyfileobj(f_in, fp)
		fp.seek(0)
		packages = fp.read().decode().split('Package: ')
		fp.close()

	f = open(CWD+'/packages.conf','w')
	for i in packages[1:]:
		try:
			name = i.split('\n')[0]
			version = i.split('Version: ')[1].split('\n')[0].split('-')[0].split('+')[0].replace(':','.').split()
			for j in range(len(version)):
				if((version[j]<'0' or version[j]>'9') and version[j]!='.'):
					del version[j]
			version = ''.join(version)
			if(version==""):
				version = "0.0.0.1"
			f.write(name+" "+version+"\n")
		except:
			pass

	f.close()
import sys, os, socket, package

CWD = os.getcwd()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
server_address = ('192.168.43.255', 10000)

message = '?'+sys.argv[1]

print('Broadcast: ', message)

sent = sock.sendto(message.encode(), server_address)

sock.close()

latestVersion = '0.0.0'
localRepo = ''

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
        latestVersionList = latestVersion.split('.')
        dataVersionList = data.split('.')
        if int(dataVersionList[0]) > int(latestVersionList[0]):
            latestVersion = data
            localRepo = address[0]
        elif int(dataVersionList[0]) == int(latestVersionList[0]) and int(dataVersionList[1]) > int(latestVersionList[1]):
            latestVersion = data
            localRepo = address[0]
        elif int(dataVersionList[0]) == int(latestVersionList[0]) and int(dataVersionList[1]) == int(latestVersionList[1]) and int(dataVersionList[2]) > int(latestVersionList[2]):
            latestVersion = data
            localRepo = address[0]

except Exception as e:
    print(e)

print("Latest available version:",latestVersion)

if latestVersion != '0.0.0':
    sourcesFile = open('/etc/apt/sources.list', 'r+')
    sourcesLine = sourcesFile.readlines()
    newRepo = [ 'deb http://%s:35622/ ./\n' % localRepo ]
    finalSourcesLines = newRepo + sourcesLine
    sourcesFile.seek(0)
    sourcesFile.writelines(finalSourcesLines)
    sourcesFile.truncate()
    sourcesFile.close()
    os.system('apt-get update')
else:
     print('File not found locally...\nDownloading from the Internet')

os.system('apt-get install %s --allow-unauthenticated' % sys.argv[1])
os.chdir('/var/cache/apt/archives')
os.system("dpkg-scanpackages . /dev/null | gzip -9c > Packages.gz") 
package.packageListGenerator(CWD)

if latestVersion != '0.0.0':
    sourcesFile = open('/etc/apt/sources.list', 'r+')
    sourcesLine = sourcesFile.readlines()
    del sourcesLine[0]
    sourcesFile.seek(0)
    sourcesFile.writelines(sourcesLine)
    sourcesFile.truncate()
    sourcesFile.close()

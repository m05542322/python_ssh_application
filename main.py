'''
2015/08/06 Tim.H.Huang

This program is design to get the disk usage information of all the machines on aws which based on an ssh connection library named paramiko

There are two files must be setted before start: config/config.ini and server_list.txt

        config.ini: information of the login user name and password

        server_list.txt: information of all machines, the format of server_list is [name]=[host] without any whitespace


'''
import ConfigParser
import paramiko
import operator
from functions import GetServerList
import os

serverListFilePath = os.path.join(os.path.dirname(__file__), 'server_list.txt')
configFilePath = os.path.join(os.path.dirname(__file__), 'config/config.ini')

serverList = GetServerList(serverListFilePath)

# Linux Disk Usage Command
cmd = 'df -h'

# Set config
config = ConfigParser.ConfigParser()

config.read(configFilePath)
loginSection = 'ini'

loginName = config.get(loginSection, 'loginName')
loginPass = config.get(loginSection, 'loginPass')

# Set thresholds
threshold = 50

diskUsage = dict()

for item in serverList:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    stdin = None
    stdout = None
    stderr = None
    try:
        #make ssh connection
        ssh.connect(hostname=serverList[item], username=loginName, password=loginPass)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        host = item + ' (' + serverList[item] + ')'
        usage = stdout.readlines()[1].split('\n')[0].split()[4].split("%")[0]
        diskUsage[host] = int(usage)
    except Exception as e:
        print "Exception!!"
        print e
        if stderr != None:
            print stderr
    finally:
        ssh.close()


sorted_result = sorted(diskUsage.items(), key=operator.itemgetter(1), reverse=True)

sendmail = 0
with open('mail_content.txt', 'wb') as output:
    for item in sorted_result:
        if item[1] > threshold:
            sendmail = 1
            output.write(item[0] + ': ' + str(item[1]) + '%\n')
    output.close()

if sendmail:
    os.system("mail -s 'Production Enviroment Disk Alert' -c tim.h.huang@newegg.com tim.h.huang@newegg.com < mail_content.txt")


for item in sorted_result:
    print item[0] + ': ' + str(item[1]) + '%'

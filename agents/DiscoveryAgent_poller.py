#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import socket
import sys
import nmap
import time
import commands
import threading
import re
from Crypto.Cipher import AES



# For debug only, 0:log // 1:console
LOG_FILE = "@AGENT_DIR@" + "/log/"+time.strftime('%Y%m',time.localtime())  +"_Poller_DiscoveryAgent.log"
#LOG_FILE = "log/"+time.strftime('%Y%m',time.localtime())  +"_Poller_DiscoveryAgent.log"
MODE_DEBUG = 0

KEY = "@KEY@"
#KEY = ""

# Encryption/Decryption function using key
def enc_dec(msg, encrypt):
	obj_crypt = AES.new(KEY, AES.MODE_CFB)
	if encrypt == 1:
		return obj_crypt.encrypt(msg)
	else:
		return obj_crypt.decrypt(msg)

def connectToCentral():
	# Check the debug mode (O:log // 1:console)
	if MODE_DEBUG ==  0:
		saveout = sys.stdout
		saveerr = sys.stderr
		flog = open(LOG_FILE, 'a')
		sys.stdout = flog	
		sys.stderr = flog
		print "##############################################"
		print "### Poller log : " + time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()) + "###"
		flog.flush()
	try:
		HOST = ''                 	      # Symbolic name meaning all available interfaces
		PORT = 1080             	      # Arbitrary non-privileged port
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((HOST, PORT))
		s.listen(1)
		while 1:
			conn, addr = s.accept()
			print 'Connected by', addr
		    	data = conn.recv(256)
			if KEY != "":
				data = enc_dec(data, 0)
			if data.startswith("#echo#"):
				print 'DiscoveryAgent_poller.py : STATUS_POLLER'
				data="#reply#"
				if KEY != "":
					data = enc_dec(data, 1)
				conn.send(data)
			elif data.startswith("#scanip#"):
				strSplit = data.lstrip().split("#")
				plage = strSplit[2]
				args = [strSplit[3], strSplit[4], strSplit[5], strSplit[6], strSplit[7], strSplit[8], strSplit[9], strSplit[10], strSplit[11], strSplit[12], strSplit[13]]
				print 'DiscoveryAgent_poller.py : SCAN_RANGEIP for ' + plage
				scanRangeIP(plage, conn, s, args)
				data = "#scanip#done"		
				if KEY != "":
					data = enc_dec(data, 1)
				conn.send(data)			
			if MODE_DEBUG==0:
				flog.flush()
	except KeyboardInterrupt:
		print "Connection aborted"
		conn.close()
		s.close()
	finally:
		# Exit properly
		if MODE_DEBUG ==  0:
			print "\n"
			sys.stdout = saveout
			sys.stderr = saveerr
			flog.close()	


def scanRangeIP(rangeIP, conn, s, args):
	try:
		nm = nmap.PortScanner()         # instantiate nmap.PortScanner object
	except nmap.PortScannerError:
		print('Nmap not found or Nmap version < 5.00', sys.exc_info()[0])
		return
	except:
		print("Unexpected error:", sys.exc_info()[0])
		return

	# Scan NMAP en ARP sur un réseau spécifié
#	nm.scan(hosts=rangeIP, arguments='-n -sP -PR ') # ARP
	try:
		rc = re.compile('T[0-5]')
		nmap_args = "-n -sU -p%s -%s --max_retries=%s --host_timeout=%s --max_rtt_timeout=%s" % (args[7], rc.findall(args[0])[0], args[1], args[2], args[3])
		#nmap_args = "-n -sU -p%s -%s --max_retries=%s --max_rtt_timeout=%s" % (args[7], rc.findall(args[0])[0], args[1],args[3])
		nm.scan(hosts=rangeIP, arguments=nmap_args)

		hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
		thread_host_list = []
		for host, status in hosts_list:
			if status=='up' :
				thread_host = threading.Thread(None, getHostOS, None, (host,args,status,conn,))
				thread_host.start()
				thread_host_list.append(thread_host)
		for thread in thread_host_list:
			thread.join()
		print "#scanip#done"		
	except nmap.PortScannerError:
		print "Error using connection. Scan stopped"
		return

def getHostOS(host,args,status,conn):
	req_snmp = "snmpget -c %s -v %s -t %s -r %s -O nq %s:%s %s 2>&1 | grep %s" % (args[8], args[6], args[9], args[10], host, args[7], args[4], args[4])
	hostname = commands.getoutput(req_snmp)
	if hostname == "":
		hostname = "* TimeOut SNMP *"
		os_name = "* TimeOut SNMP *"
	else:
		hostname = hostname.split(' ',1)[1]
		#hostname = hostname.replace(hostname, hostname[hostname.find("STRING")+len("STRING: "):])
		req_snmp = "snmpget -c %s -v %s -t %s -r %s -O nq %s:%s %s 2>&1 | grep %s" % (args[8], args[6], args[9], args[10], host, args[7], args[5], args[5])
		os_name = commands.getoutput(req_snmp)
		os_name = os_name.split(' ',1)[1]
	state = "#state#%s#%s#%s#%s"%(host,status,hostname,os_name)
	state = "%475s"%state
	print "Send : ",state.lstrip()
	if KEY != "":
		state = enc_dec(state, 1)
	conn.send(state)


if __name__ == '__main__':
	# Connection to central	
	connectToCentral();

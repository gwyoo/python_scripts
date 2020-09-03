#!/usr/bin/python

import sys
import os
import netsnmp
import pyping


def ping_test(ipaddr):
	ping_res = pyping.ping(ipaddr, count=1, timeout=500)

	if ping_res.ret_code == 0:
		return True
	else:
		return False


def snmp_get_test(ipaddr):
	var = netsnmp.Varbind('sysDescr.0')
	res = netsnmp.snmpget(var, Version = 2,  DestHost = ipaddr,  Community='storm_tros', Timeout=500000) 

	if res[0] is None:
		return False
	else:
		return True 


def check_ip(ipaddr):
	print "%-16s" % ipaddr , ":",  
	sys.stdout.flush()

	response = ping_test(ipaddr)

	if response:
		print "PING OK   :",
		sys.stdout.flush()
		response2 = snmp_get_test(ipaddr)
		if response2:
			print "SNMP_GET OK"
			#os.system("head -1 /tmp/3")
		else:
			print "SNMP_GET ERROR"
			#os.system("head -1 /tmp/4")
	else:
		print "PING ERROR"

#################################################################

if len(sys.argv) != 2:
	print "Please, Input filename(ipaddr list)!!"
	raise SystemExit(1)

fd = open(sys.argv[1])
lines = fd.readlines()
totalcount=len(lines)
print "IP List Count is ", totalcount

i = 1
for line in lines:
	print "%5d" % i, "/", "%5d" % totalcount," : ", 
	line = line.strip()
	check_ip(line)	
	i = i + 1
fd.close()

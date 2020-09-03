#!/usr/bin/python

import sys
import os


def ping_test(ipaddr):
	ping_res = os.system("ping -c 1 " + ipaddr + " 1> /tmp/1 2> /tmp/2")

	if ping_res == 0:
		#print "==> ", ipaddr, " is up!"
		return True
	else:
		#print "==> ", ipaddr, " is down!"
		return False


def snmp_get_test(ipaddr):
	snmp_res = os.system("snmpwalk -v 2c -c storm_tros " + ipaddr + " 1> /tmp/3 2> /tmp/4")

	if snmp_res == 0:
		return True
	else:
		return False 


def check_ip(ipaddr):
	print "%-16s" % ipaddr , ":",  

	response = ping_test(ipaddr)

	if response:
		print "PING OK   :",
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

i = 1
for line in lines:
	print "%5d" % i, "/", "%5d" % totalcount," : ", 
	line = line.strip()
	check_ip(line)	
	i = i + 1
fd.close()

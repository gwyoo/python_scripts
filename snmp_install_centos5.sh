#!/bin/bash
#
# snmp install script for CentOS-5
# version 0.9
#
# scripted by gwyoo
# 2016. 8. 11 
#


echo "SNMP INSTALL SCRIPT============================================"
########################################################################################################
echo 
echo 
echo "---------------------------------------------" 
echo "------dmidecode installation by yum"
echo "---------------------------------------------" 

yum -y install dmidecode
echo
echo -n "IF dmidecode does not exist, then press Q + [Enter]. Otherwise [Enter] "

read answer
if [[ $answer = "Q" ]]; then
	echo "Because dmidecode does not exit, install process QUITs" 
	exit
fi


########################################################################################################
echo 
echo 
echo "---------------------------------------------" 
echo "------snmp daemon installation by yum"
echo "---------------------------------------------" 

yum -y install net-snmp*
echo
echo -n "IF net-snmp does not exist, then press Q + [Enter]. Otherwise [Enter] "

read answer
if [[ $answer = "Q" ]]; then
	echo "Because snmp daemon does not exit, install process QUITs" 
	exit
fi


########################################################################################################
echo 
echo 
echo "---------------------------------------------" 
echo "------system & process info filing" 
echo "---------------------------------------------" 

/usr/sbin/dmidecode -t 1 > /etc/snmp/dmidecode_t_1.log
/usr/sbin/dmidecode -t 4 > /etc/snmp/dmidecode_t_4.log

grep "dmidecode -t 1" /var/spool/cron/root > /dev/null
ret=$?
if [[ $ret = 1 ]]; then
	echo "0 2 * * * /usr/sbin/dmidecode -t 1 > /etc/snmp/dmidecode_t_1.log" >> /var/spool/cron/root
elif [[ $ret = 2 ]]; then
	echo "0 2 * * * /usr/sbin/dmidecode -t 1 > /etc/snmp/dmidecode_t_1.log" >> /var/spool/cron/root
fi

grep "dmidecode -t 4" /var/spool/cron/root > /dev/null
ret=$?
if [[ $ret = 1 ]]; then
	echo "0 2 * * * /usr/sbin/dmidecode -t 4 > /etc/snmp/dmidecode_t_4.log" >> /var/spool/cron/root
elif [[ $ret = 2 ]]; then
	echo "0 2 * * * /usr/sbin/dmidecode -t 4 > /etc/snmp/dmidecode_t_4.log" >> /var/spool/cron/root
fi


/bin/ls -al /etc/snmp/dmi*
echo
echo -n "IF dmidecode_t_[1|4].log files do not exist, then press Q + [Enter]. Otherwise [Enter] "

read answer
if [[ $answer = "Q" ]]; then
	echo "Because dmidecode log files do not exit, install process QUITs" 
	exit
fi

echo
crontab -l | grep dmidecode
echo
echo -n "crontab jobs do not exist, then press Q + [Enter]. Otherwise [Enter] "

read answer
if [[ $answer = "Q" ]]; then
	echo "Because dmidecode log files do not exit, install process QUITs" 
	exit
fi


########################################################################################################
echo 
echo 
echo "---------------------------------------------" 
echo "------snmpd.conf backup $ change"
echo "---------------------------------------------" 

/bin/mv /etc/snmp/snmpd.conf /etc/snmp/snmpd.conf.backup

echo "com2sec notConfigUser  default       public                                       " > /etc/snmp/snmpd.conf
echo "group   notConfigGroup v1           notConfigUser                                 " >> /etc/snmp/snmpd.conf
echo "group   notConfigGroup v2c           notConfigUser                                " >> /etc/snmp/snmpd.conf
echo "view    systemview    included   .1.3.6.1.2.1                                     " >> /etc/snmp/snmpd.conf
echo "view    systemview    included   .1.3.6.1.4.1                                     " >> /etc/snmp/snmpd.conf
echo "access  notConfigGroup \"\"      any       noauth    exact  systemview none none    " >> /etc/snmp/snmpd.conf
echo "syslocation Unknown (edit /etc/snmp/snmpd.conf)                                   " >> /etc/snmp/snmpd.conf
echo "syscontact Root <root@localhost> (configure /etc/snmp/snmp.local.conf)            " >> /etc/snmp/snmpd.conf
echo "dontLogTCPWrappersConnects yes                                                    " >> /etc/snmp/snmpd.conf
echo "includeAllDisks  10%                                                              " >> /etc/snmp/snmpd.conf
##############
############## cat executable file's PATH CHECK is VERY IMPORTANT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
############## cat executable file's PATH CHECK is VERY IMPORTANT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
############## cat executable file's PATH CHECK is VERY IMPORTANT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
##############
echo "extend     system        /bin/cat  /etc/snmp/dmidecode_t_1.log                    " >> /etc/snmp/snmpd.conf
echo "extend     processor     /bin/cat  /etc/snmp/dmidecode_t_4.log                    " >> /etc/snmp/snmpd.conf
/bin/ls -al /etc/snmp/snmpd.conf*
echo
echo -n "IF snmpd.conf snmpd.conf.backup files do not exist, then press Q + [Enter]. Otherwise [Enter] "

read answer
if [[ $answer = "Q" ]]; then
	echo "Because snmpd.conf snmpd.conf.backup files do not exit, install process QUITs" 
	exit
fi


########################################################################################################
echo 
echo 
echo "---------------------------------------------" 
echo "------snmpd daemon start"
echo "---------------------------------------------" 

service snmpd restart
service snmpd status

echo
echo -n "IF snmpd daemon does not start, then press Q + [Enter]. Otherwise [Enter] "

read answer
if [[ $answer = "Q" ]]; then
	echo "Because snmpd daemon does not start, install process QUITs" 
	exit
fi



########################################################################################################
echo 
echo 
echo "---------------------------------------------" 
echo "------snmpd service registration"
echo "---------------------------------------------" 

chkconfig snmpd on
chkconfig --list snmpd

echo
echo -n "IF \"snmpd           0:off   1:off   2:on    3:on    4:on    5:on    6:off\" is not, then press Q + [Enter]. Otherwise [Enter] "

read answer
if [[ $answer = "Q" ]]; then
	echo "Because snmpd service is not registered, install process QUITs" 
	exit
fi


########################################################################################################
echo 
echo 
echo "---------------------------------------------" 
echo "------filewall config change"
echo "---------------------------------------------" 

iptables -L | grep "udp dpt:snmp" > /dev/null
if [[ $? = 1 ]]; then  
	################################### Match string does not exit
	iptables -I INPUT -p udp -m udp --dport 161 -j ACCEPT
	service iptables save
	service iptables restart
fi
/sbin/iptables -L

echo
echo -n "IF \"ACCEPT     udp  --  anywhere             anywhere            udp dpt:snmp\" is not, then press Q + [Enter]. Otherwise [Enter] "

read answer
if [[ $answer = "Q" ]]; then
	echo "Because firewall config fails, install process QUITs" 
	exit
fi


########################################################################################################
echo 
echo 
echo "---------------------------------------------" 
echo "------snmpwalk check phase I"
echo "---------------------------------------------" 

snmpwalk -v 2c -c public localhost | head -10


########################################################################################################
echo 
echo 
echo "---------------------------------------------" 
echo "------snmpwalk check phase II"
echo "---------------------------------------------" 

snmpwalk -v 2c -c public localhost .exte | head -40

echo "SUCCESS !!!"


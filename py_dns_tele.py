import telepot
import socket
import time
import string
from datetime import datetime

# telegram info
token='1601309060:AAGx282hUb_Qe8S-xECQRZE6pY7B0HeAjwo'
chat_id = 1635025695

db0_ip = ''
db1_ip = ''

# file info
fname = "/home/azureuser/pysrc/iplist.conf"

def query_dns(addr):
    return socket.getaddrinfo(addr, 80)[0][4][0]


# get ip info from FILE
def getdata(fname):
    global db0_ip, db1_ip

    f = open(fname, "r")
    line = f.readlines()
    db0_ip = string.strip(line[0])
    db1_ip = string.strip(line[1])
    f.close()

# put ip info to FILE
def putdata(fname):
    global db0_ip, db1_ip

    f = open(fname, "w")
    f.write(db0_ip + "\n")
    f.write(db1_ip + "\n")
    f.close()

bot = telepot.Bot(token)

getdata(fname)

# check liveness
if datetime.now().strftime("%H%M") == "0705":    # 16:05 check
    bot.sendMessage(chat_id, text="I am still ALIVE... py_dns_tele.py 07:05 UTC")
    print  "I am still ALIVE - dns check"

# check ip addr change - master db
db0_azure_ip = query_dns('pcc-prd-rdb.mysql.database.azure.com')
if db0_azure_ip != db0_ip:
    print  datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Master ip diff", db0_ip, db0_azure_ip
    bot.sendMessage(chat_id, text="Master DB IP Diff ==> "+ datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + db0_ip + "|" + db0_azure_ip)
    db0_ip = db0_azure_ip

# check ip addr change - replica db
db1_azure_ip = query_dns('pcc-prd-rdb-01.mysql.database.azure.com')
if db1_azure_ip != db1_ip:
    print  datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Replica ip diff", db1_ip, db1_azure_ip
    bot.sendMessage(chat_id, text="Replica DB IP Diff ==> "+ datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + db1_ip + "|" + db1_azure_ip)
    bot.sendMessage(chat_id, text="Replica DB IP Diff "+db1_ip+"|"+db1_azure_ip)
    db1_ip = db1_azure_ip

putdata(fname)

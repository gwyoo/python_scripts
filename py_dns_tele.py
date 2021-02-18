# 기존에 저장한 IP와 doname name query한 것과 비교해서 다를 경우, telegram으로 메시지 전송함
#

import telepot
import socket

# telegram 관련 정보
token='1601309060:AAGx282hUb_Qe8S-xECQRZE6pY7B0HeAjwo'
chat_id = 1635025695

# 비교할 IP정보
db0_ip = '52.231.200.86'
db1_ip = '52.231.32.42'

# master db의 IP정보 비교
if socket.getaddrinfo('pcc-prd-rdb.mysql.database.azure.com', 80)[0][4][0] != db0_ip:
    DB0_diff = True
    print "master diff checked"
else:
    DB0_diff = False

# replica db의 IP정보 비교
if socket.getaddrinfo('pcc-prd-rdb-01.mysql.database.azure.com', 80)[0][4][0] != db1_ip:
    DB1_diff = True
    print "replica diff checked"
else:
    DB1_diff = False

if DB0_diff or DB1_diff: bot = telepot.Bot(token)
if DB0_diff: bot.sendMessage(chat_id, text="Master DB Diff")
if DB1_diff: bot.sendMessage(chat_id, text="Replica DB Diff")

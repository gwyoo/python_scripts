#!/usr/bin/python3
import mysql.connector
from mysql.connector import errorcode

from datetime import datetime
import time



import telegram
import asyncio

async def send_telegram(msg):
    bot = telegram.Bot(token='6446717981:AAGhj1qvT_47MY4zX1a9X-ckIQOmn9mkJEU')
    chat_id = 5614379509

    await bot.send_message(chat_id, text = msg)


config = {
    'host':'pcc-prd-rdb-mhub-01.mysql.database.azure.com',
    'user':'apppcc@pcc-prd-rdb-mhub-01',
    'password':'pcc2020pwd!',
    'database':'mhub'
}


def get_cnt():

    # DB connect
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # DB Query
    cursor.execute("select count(*) from sms.tb_bulk tb, sms.tb_message tm where tb.smsSeq = tm.smsSeq and status = 0 and lockStatus = 'A' and psid is null and reserveDateTime between '2024-03-29 00:00:00' and '2024-06-30 23:59:59'")
    row = cursor.fetchone()

    cnt = row[0]

    # DB close
    cursor.close()
    conn.close()

    return cnt


now1 = datetime.now()
cnt1 = get_cnt()

time.sleep(30)

now2 = datetime.now()
cnt2 = get_cnt()

if cnt1 == 0:
    str_msg = "OK !! \n"
else:
    str_msg = "=== CHECK ===> \n"

str_msg = str_msg + "     " + now1.strftime('%Y-%m-%d %H:%M:%S') + " : " + str(cnt1) + "\n     " + now2.strftime('%Y-%m-%d %H:%M:%S') + " : " + str(cnt2)

#print (str_msg)

asyncio.run(send_telegram(str_msg))

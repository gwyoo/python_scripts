import mysql.connector
from mysql.connector import errorcode

from datetime import datetime

MAX_QUERY_CNT = 30

config = {
    'host':'pcc-prd-rdb.mysql.database.azure.com',
    'user':'sktpcc@pcc-prd-rdb',
    'password':'pcc2018pwd!',
    'database':'sktpcc'
}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()
cursor.execute("select * from information_schema.processlist p where p.info is not null order by time desc")
rows = cursor.fetchall()
#print ("read", cursor.rowcount, "row of data")
if cursor.rowcount > MAX_QUERY_CNT:
    now = datetime.now()
    print ("==============================", now.strftime('%Y-%m-%d %H:%M:%S'), "Rows", cursor.rowcount)
    for row in rows:
        print(row)

cursor.close()
conn.close()

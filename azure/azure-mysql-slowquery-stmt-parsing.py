import sys

# Usage : 
# python src1.py mysql-slow-pcc-prd-rdb-2023080804.log > 0808.csv
#

if len(sys.argv) != 2:
    print("Insufficient arguments")
#    file_path = "d:\slow1.txt"
    sys.exit()
else:
    file_path = sys.argv[1]

f = open(file_path, "r", encoding='UTF8')
lines = f.readlines()
f.close()

linelen = len(lines)

stmt = stmt_tag = ""
status = 0

def print_record():
    print (item_date, ",", item_time, ",", item_ip, ",", item_id, ",", item_qu_time, ",", item_lk_time, ",", end='')
    print (item_rw_sent, ",", item_rw_exam, ",", '"'+stmt_tag+'"', "," '"'+stmt[:200]+'"')

print ("date, time, ip, id, query_time, lock_time, rows_sent, rows_exam, tag, sql")

for line in lines[3:]:
    if status == 0:       # TIME
        status = 1
        
        item_date = line[8:18]
        item_time = line[19:35]
  
    elif status == 1:     # User@Host
        status = 2
        
        item_ip = line[line.rfind('[') + 1 : line.rfind(']')]
        item_id = line[line.rfind('Id: ') + 4 : line.rfind('\n')]
        
    elif status == 2:     # Query Time
        status = 3
        
        loc1 = line.find('Query_time: ')
        loc2 = line.find('Lock_time: ')
        loc3 = line.find('Rows_sent: ')
        loc4 = line.find('Rows_examined: ')
        loc5 = len(line)-1

        item_qu_time = line[loc1 + len('Query_time: ')   : loc2 ].strip()
        item_lk_time = line[loc2 + len('Lock_time: ')    : loc2 + 19]
        item_rw_sent = line[loc3 + len('Rows_sent: ')    : loc4 - 2]
        item_rw_exam = line[loc4 + len('Rows_examined: '): loc5]
        
        
    else:                 # Query Stmt
        if line[0] == '#':
            stmt_tag = stmt[stmt.find('/*') : stmt.find('*/') + 2]
            stmt = stmt[0:200]
            
            #print ("tag --> ", stmt_tag)
            #print ("stmt -->", stmt)
            print_record()
            
            status = 1
            stmt = ""
            stmt_tag = ""
            item_date = line[8:18]
            item_time = line[19:35]

        else:
            #print('before stmt     #####', stmt)
            #print('     line strip #####', line.strip())
            stmt = stmt + line.strip()
            #print('after  stmt     #####', stmt)


#stmt_tag = stmt[loc1, loc2]
stmt_tag = stmt[stmt.find('/*') : stmt.find('*/') + 2]

#print ("tag --> ", stmt_tag)
#print ("stmt -->", stmt[0:200])
print_record()           

#print (line[0])
#print (line[1])

#stmt = "use sktpcc;\nSET timestamp=1691294706;\nCALL /* schedul.api.parking.common.sqlmap.xml - processSchedulMaster */ SCH_MASTER_PROC (\n		'DTA040'               /* in_스케즐 코드 */\n		,'20230806130500'                /* in_수행 시간 */\n		);"
#new_stmt = re.sub("\n", "", query_stmt)

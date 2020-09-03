# 무제한 요금제 사용자 일한도 초과 전문(H9)
# MSISDN번호별 수신일자 계산 script 

rfd=open("d:\\H9.txt")
lines = rfd.readlines()
totalcount = len(lines)
rfd.close()

i=0
dic = {}
for line in lines:
	num=line[4:12]
	recv=line[23:25]
	
	# filtering or sampling
	if num[6:8] <> '87': continue
	
	# dictionary value init : null list
	if not num in dic: dic[num] = []
	dic[num].append(recv)

	i = i + 1

MSISDNs = dic.keys()

print 'total count', i
print 'get value from dic (value exists)', dic.get('20212137', -1)
print 'msisdn count', len(MSISDNs)

for MSISDN in MSISDNs:
	print MSISDN, len(dic[MSISDN]), dic[MSISDN]
	
MSISDN_list = dic.items()
	
## 821093152022 ^ 2017/02/01 00:14:29:639490
## 821044720980 ^ 2017/02/01 00:15:07:584136
## 821093152022 ^ 2017/02/03 00:14:29:639490

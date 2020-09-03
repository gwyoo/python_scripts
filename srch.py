#!/usr/bin/python

import os, sys, string, time
import getopt

dia_codes = (
  [  263, "UTFSTRING   "    , "Session-Id"               , " "  ],
  [  264, "DIA_IDENTITY"    , "Origin-Host"              , " "  ],
  [  296, "DIA_IDENTITY"    , "Origin-Realm"             , " "  ],
  [  283, "DIA_IDENTITY"    , "Destination-Realm"        , " "  ],
  [  480, "ENUMERATED  "    , "Accounting-Record-Type"   , " "  ],
  [  485, "UNSIGNED32  "    , "Accounting-Record-Number" , " "  ],
  [    1, "UTF8STRING  "    , "User-Name"                , " "  ],
  [   85, "UNSIGNED32  "    , "Acct-Interim-Interval"    , " "  ],
  [   55, "TIME        "    , "Event-Timestamp"          , " "  ],
  [10000, "GROUPED     "    , "Event-Type"               , " "  ],
  [10001, "UTF8STRING  "    , "SIP-Method"               , " "  ],
  [10002, "UTF8STRING  "    , "Event"                    , " "  ],
  [10003, "UTF8STRING  "    , "Global-Session-Id"        , " "  ],
  [10004, "GROUPED     "    , "Address"                  , " "  ],
  [10005, "UTF8STRING  "    , "Calling-Party-Address"    , " "  ],
  [10006, "UTF8STRING  "    , "Called-Party-Address"     , " "  ],
  [10007, "UTF8STRING  "    , "Charging-Party-Address"   , " "  ],
  [10008, "UTF8STRING  "    , "Call-Forward-Address"     , " "  ],
  [10009, "INTEGER32   "    , "Origination_flag"         , " "  ],
  [10010, "UTF8STRING  "    , "IMS-Charging-Identifier"  , " "  ],
  [10011, "TIME        "    , "Start-Time"               , " "  ],
  [10012, "TIME        "    , "End-Time"                 , " "  ],
  [10013, "INTEGER32   "    , "Charging-Duration"        , " "  ],
  [10014, "INTEGER32   "    , "Sip-body-size-uplink"     , " "  ],
  [10015, "INTEGER32   "    , "Sip-body-size-downlink"   , " "  ],
  [10016, "INTEGER32   "    , "Content-size-uplink"      , " "  ],
  [10017, "INTEGER32   "    , "Content-size-downlink"    , " "  ],
  [10019, "INTEGER32   "    , "RTP-size-uplink"          , " "  ],
  [10020, "INTEGER32   "    , "RTP-size-downlink"        , " "  ],
  [10021, "INTEGER32   "    , "Receiver-count"           , " "  ],
  [10022, "INTEGER32   "    , "Service-type"             , " "  ],
  [10023, "INTEGER32   "    , "SubService-Type"          , " "  ],
  [10024, "UTF8STRING  "    , "Charge-Indicator"         , " "  ],
  [10026, "GROUPED     "    , "Cause"                    , " "  ],
  [10027, "INTEGER32   "    , "SIP-Code"                 , " "  ],
  [10028, "INTEGER32   "    , "Detail-Code"              , " "  ],
  [10029, "UTF8STRING  "    , "Terminal-Type"            , " "  ],
  [10030, "UTF8STRING  "    , "Terminal-Model"           , " "  ],
  [10031, "INTEGER32   "    , "Connection-Type"          , " "  ],
  [10032, "UTF8STRING  "    , "PPS-Type"                 , " "  ],
  [10033, "UTF8STRING  "    , "Terminal-Ip-Address"      , " "  ],
  [10034, "GROUPED     "    , "NIBS-Item"                , " "  ],
  [10035, "UTF8STRING  "    , "NIBS-URL1"                , " "  ],
  [10036, "UTF8STRING  "    , "NIBS-Service ID"          , " "  ],
  [10037, "UTF8STRING  "    , "NIBS-TID"                 , " "  ],
  [10038, "UTF8STRING  "    , "NIBS-Data Size"           , " "  ],
  [10039, "UTF8STRING  "    , "NIBS-Size Indicator"      , " "  ],
  [10040, "UTF8STRING  "    , "NIBS-UA Flag"             , " "  ],
  [10041, "UTF8STRING  "    , "NIBS-Calling ID"          , " "  ],
  [10042, "UTF8STRING  "    , "NIBS-Charging ID"         , " "  ],
  [10043, "UTF8STRING  "    , "NIBS-Called ID"           , " "  ],
  [10044, "INTEGER32   "    , "P2P-Message-Count"        , " "  ],
  [10045, "INTEGER32   "    , "P2W-Message-Count"        , " "  ],
  [10046, "INTEGER32   "    , "W2P-Message-Count"        , " "  ],
  [10047, "INTEGER32   "    , "W2W-Message-Count"        , " "  ]
)

dia_val = []
isFound = False
srch_type = ''
srch_str  = ''
DIAMESSAGE_HEADER_SIZE = 20

def conv_num(s):
    if len(s) == 1:
        num = ord(s[0])
    elif len(s) == 2:
        num = ord(s[0]) * (2**8)  + ord(s[1])
    elif len(s) == 3:
        num = ord(s[0]) * (2**16) + ord(s[1]) * (2**8) + ord(s[2])
    elif len(s) == 4:
        num = ord(s[0]) * (2**24) + ord(s[1]) * (2**16) + ord(s[2]) * (2**8) + ord(s[3])
    else: num = -1
    return num

def is_vendor(s):
    ch = s[4]
    if ord(ch) >= 128: return 12
    else: return 8

def srch_dia_code(dia_codes, code):
    for i in range(len(dia_codes)):
        if code == dia_codes[i][0]: return i
    return -1    

def get_dia_data(dia_codes, s, idx, data_offset, data_leng, group_flag):
    if group_flag: indent_str = "    "
    else: indent_str = ""
    
    if   dia_codes[idx][1] in   ["DIA_IDENTITY", "UTFSTRING   ", "UTF8STRING  "]:
        dia_val[idx] = indent_str + s[data_offset:data_leng]
        if dia_codes[idx][0] == 1:
            if s[data_offset:data_leng] == 'sip:'+srch_str+'@sktimt.net':
                isFound == True
            else: print "%s %s %d"%(s[data_offset:data_leng], srch_str, isFound)
        
    elif dia_codes[idx][1] in ["GROUPED     "]:
        dia_val[idx] = indent_str + "GROUPED AVP"
    elif dia_codes[idx][1] in ["TIME        "]:
        tm = conv_num(s[data_offset:data_offset+4])
        usec = ".%s"%conv_num(s[data_offset+4:data_offset+8])
        dia_val[idx] = indent_str + time.strftime("%Y.%m.%d %H:%M:%S", time.localtime(tm))+usec
    elif dia_codes[idx][1] in ["ENUMERATED  ", "UNSIGNED32  ", "INTEGER32   "]:
        dia_val[idx] = indent_str + "%s"%(conv_num(s[data_offset:data_leng]))
    else:
        print "Cannot find such type: %d %d %s"%(idx, dia_codes[idx][0], dia_codes[idx][2])
        return -1
#    print "%-40s: %s"%(dia_codes[idx][2], dia_val[idx])
    return True    
        
def conv_dia_message_body(dia_codes, s, group_flag):
    if not group_flag:
        for i in range(len(dia_codes)):
            dia_codes[i][3] = " "
        aaa = []
        
    left_size = len(s)
    while left_size >= 4:
        code = conv_num(s[:4]) 
        data_leng = conv_num(s[5:8])
        data_offset = is_vendor(s)
        
#        print "total leng: %d, leng: %d, offset: %d"%(left_size, data_leng, data_offset),
        
        idx = srch_dia_code(dia_codes, code)        
        dia_codes[idx][3] = get_dia_data(dia_codes, s, idx, data_offset, data_leng, group_flag)
        if dia_codes[idx][1] == "GROUPED     ":
            conv_dia_message_body(dia_codes, s[is_vendor(s):data_leng], True)
        if (data_leng % 4):  
            data_leng += (4 - (data_leng % 4))
        left_size = left_size - data_leng
        s = s[data_leng:]
    return True
    
def usage():
    print "srch OPTION files..."
    print "OPTION : -m MDN     "
    print "         -i IP      "    
    
def main():

    srch_type = 'ALL'
    opts, args = getopt.getopt(sys.argv[1:], 'hm:i:')
    for o, a in opts:
        if o == '-m':
            srch_type = 'MDN'
            srch_str = a
        if o == '-i':
            srch_type = 'IP'
            srch_str = a
        if o == '-h':
            usage()
            sys.exit(1)
            
    print "%s %s %s"%(srch_type, srch_str, args)            
    for file_nm in args:    
        if srch_type == 'ALL':  isFound = True
        else:   isFound = False
        
        arcfile = file(file_nm, 'rb')
        readstr = arcfile.read(DIAMESSAGE_HEADER_SIZE)
        foffset = 0
        for i in range(len(dia_codes)): dia_val.append('')
    
        while (len(readstr)):
            msgleng = conv_num(readstr[1:4])
            
            if msgleng < DIAMESSAGE_HEADER_SIZE: 
                print "Invalid Message Length: %d" % msgleng
                return
                           
            readstr = arcfile.read(msgleng - DIAMESSAGE_HEADER_SIZE)
            if conv_dia_message_body(dia_codes, readstr, False):
                if isFound:
                    for i in range(len(dia_codes)):
                        print "%s;" % (dia_val[i]),
                        dia_val[i] = ''
                    print 
                        
    #           print "----------------------------"
    #       print dia_val
    #       print "=============================="
            readstr = arcfile.read(DIAMESSAGE_HEADER_SIZE)
        arcfile.close()
            
if __name__ == "__main__":
    main()

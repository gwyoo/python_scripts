#!/usr/bin/python

import os, sys, string
import curses.ascii

def main():
   
    rfile = file(sys.argv[1], "r")    
    rstr = rfile.read(8)
    foffset = 0
    
    while (len(rstr)):
        print "0x%04x: "%foffset,
        
        for i in range(len(rstr)): 
            print "0x%02x "%ord(rstr[i]),
        for i in range(len(rstr)): 
            if curses.ascii.isprint(rstr[i]):
                ch = rstr[i]
            else:
                ch = '.'
            print "%c"%(ch),
        print
                
        rstr = rfile.read(8)
        foffset = foffset + len(rstr)
            
    rfile.close()
            
if __name__ == "__main__":
    main()

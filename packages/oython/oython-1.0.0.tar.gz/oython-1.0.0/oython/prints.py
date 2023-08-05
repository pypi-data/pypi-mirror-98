#oython 1.0.0 
#prints 0.0.1

import time
import sys

def cleansc(nwq):#清屏
    if nwq:
        time.sleep(nwq)
        sys.stdout.write("\033[2J\033[00H")
        
def oyprint(nwz,t):#逐字输出
    for nwprint in nwz:
        time.sleep(t)
        if len(nwz) != 0:
            print(nwprint,end = '')
        else:
            print(nwprint)
    print()
    
def error(err):
    raise Exception(err)

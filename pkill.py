# file:    pkill.py
# author:  Colin Woodbury
# contact: colingw AT gmail
# about:   Kills a given program name, if it can.
#          Accepts '-f' as a flag to send a -9 KILL signal instead of the  
#          safer -15 TERM signal.

import subprocess
import sys
import os
import re

def get_args():
    '''Parses the args looking for flags and the process name.'''
    if not 1 < len(sys.argv) < 4:
        print('Bad args ->', sys.argv)
        return
    signal = '-15'  # Send the software termination signal by default.
    process = sys.argv[1]  # The first given arg must be a process name.
    if len(sys.argv) > 2 and '-f' in sys.argv: # Possible flag given.
        pos = sys.argv.index('-f')
        signal = '-9'  # Kill the fucker.
        process = sys.argv[-pos]
    return (process, signal)

args = get_args()    
if args:
    process = args[0]
    signal = args[1]
    pid = None
    pidList = subprocess.getoutput('ps -A | grep {0}'.format(process))
    for line in pidList.split('\n'):
        if re.search('/{0}'.format(process), line):
            pid = line.split()[0]
            break
    if pid:
        # os.kill() didn't work...
        os.system('kill {0} {1}'.format(signal, pid))
    else:
        print('{0} -> No such process active.'.format(process))

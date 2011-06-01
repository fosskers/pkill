# file:    pkill.py
# author:  Colin Woodbury
# contact: colingw AT gmail
# about:   Kills a given program name, if it can.
#
# options:
#  -1  Hang up the program.
#  -2  Interrupt the program.
#  -3  Quit.
#  -6  Abort.
#  -9  Kill (non-catchable, non-ignorable kill)
#  -14 Alarm clock.
#  -15 Software termination signal. The 'safe' kill.  

# BUGS: Make pkill non-case-sensative.

import subprocess
import sys
import os
import re

def get_args():
    '''Parses the args looking for flags and the process name.'''
    if not 1 < len(sys.argv) < 4:
        print('Bad args ->', sys.argv)
        return
    signals = ('-1', '-2', '-3', '-6', '-9', '-14', '-15')
    signal  = '-15'  # Send the software termination signal by default.
    process = sys.argv[1]  # By default, there is no signal given.
    if len(sys.argv) > 2:
        process = sys.argv[2]
        if sys.argv[1] in signals:
            signal  = sys.argv[1]
        else:
            print('{} is not a valid signal. Using -15.'.format(sys.argv[1]))
    return (process, signal)

args = get_args()    
if args:
    process = args[0]
    signal  = args[1]
    pid     = None
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

#!/usr/bin/python3
import datetime
import time
import traceback
from subprocess import PIPE, Popen

def cmdline(command):
    process = Popen(
            args=command,
            stdout=PIPE,
            shell=True,
            universal_newlines=True
    )
    return process.communicate()[0]

debug = True
while True:
    try:
        print("Reading logs...")
        the_time = datetime.datetime.now()
        fast_log = cmdline('cat /var/log/suricata/fast.log')# or just read the file in
        fast_log = fast_log.split('\n')# so each entry in fast.log is its own line 
        for i in fast_log: # iterate over each entry in fast.log
            if "CUSTOM" in i:
                # only IPs I want to block have "CUSTOM" in the alert,
                # so it is a reliable way to determine if want to block IP
                ip = i.split('-> ')[1].split(':')[0]
                check_ip = cmdline('iptables -nL -t raw')#see if IP already blocked
                # this is here to avoid redundant firewall rules
                if ip not in check_ip:
                    # command to block IP
                    cmdline(f'iptables -t raw -A PREROUTING -s {ip} -j DROP')
                    log_entry = str(the_time) + f' BLOCKED {ip}\n'
                    print(log_entry)
                    f = open('/var/log/blocks.log', 'w') # add to blocked IP log
                    f.write(log_entry)
                    f.close()
        print("sleeping... ")
        time.sleep(60) # pauses for 60 seconds before next loop
    except:
        # this makes reading errors easier, gets rid of some noise from stderr
        if debug:
            print(traceback.format_exc())
        error_time = datetime.datetime.now()
        g  = open('/var/log/python_daemon_error.log','a')
        g.write('----------------------\n')
        g.write(str(error_time)+'\n')
        g.write(traceback.format_exc()+'\n')
        g.close()
        time.sleep(60)

#!/usr/bin/python3
import sys
from subprocess import PIPE, Popen
"""
This script takes in a pcap file as a command line argument and writes
all of the TCP streams together to one text file in a 
cleaned up and human readable format.
"""
def cmdline(command):
    """
    The following function takes in a bash command and returns the stdout.
    I use it here to repeat individual TCP stream output commands 
    and add it all the streams together in one file for easy analysis.
    """
   process = Popen(
            args=command,
            stdout=PIPE,
            shell=True,
            universal_newlines=True,
    )
    return process.communicate()[0]

pcap_file = sys.argv[1] # name of the pcap file (filename.pcap)

# Dynamically name the text output file.
# Split at the period of filename.pcap
# (.pcap will be taken off and _streams.txt added...filename.txt)
output_file_name = pcap_file.split('.')[0]+'_streams.txt'

# now open in write mode to add the output
output_file = open(output_file_name, 'w')

# While loop iterates over each tcp stream, stripping it of any noise,
# and writing the output to a new text file. Use '-----------------' as a
# search term to move quickly between each streams.
count = 0
while True:
    cmd = f'tshark -r {pcap_file} -z follow,tcp,ascii,{count}'
    stream = cmdline(cmd)
    stream = stream.split('================================================\n')[1]
    stream += '\n-------------------\n'
    if 'Node 0: :0' not in stream:
        output_file.write(stream)
    else:
        break
    count += 1
output_file.close()


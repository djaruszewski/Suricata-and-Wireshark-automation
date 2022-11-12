#!/usr/bin/python3
from subprocess import PIPE, Popen
"""
This function takes in a bash command and returns it's output,
can be very useful if need to iterate over multiple commands or
when a GUI for another program is not available.
"""


def cmdline(command):
    process = Popen(
            args=command,
            stdout=PIPE,
            shell=True,
            universal_newlines=True
    )
    return process.communicate()[0]

cmd_output = cmdline('ls /home/kali/Desktop').rstrip()

print(cmd_output)

files = cmd_output.split('\n')

print(files)

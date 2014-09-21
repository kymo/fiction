import os
import copy
import subprocess

def read_file(file_path):
    with open(file_path, 'r') as f:
        data = f.read()
        return data

def cmd_output(cmd):
    with os.popen(cmd) as buff:
        return buff.read()

def process_stat(pid):
    fmt = 'ps -p %s u'
    return cmd_output(fmt % pid)

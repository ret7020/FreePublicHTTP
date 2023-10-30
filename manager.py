#!/usr/bin/env python

import subprocess
import sys

def get_keeper_pid():
    tunnel_keeper_pid = None
    process = subprocess.Popen("ps -eo pid,command | grep 'python3 public_ip_handler'", shell=True, stdout=subprocess.PIPE)
    processes = process.communicate()[0].decode("utf-8").split("\n")
    for pr in processes:
        if "python3 public_ip_handler.py" in pr:
            tunnel_keeper_pid = int(pr.strip().split()[0])

    return tunnel_keeper_pid

tunnel_keeper_pid = get_keeper_pid()

if len(sys.argv) > 1:
    if sys.argv[1] == "check":
        if tunnel_keeper_pid:
            print("Alive with pid:", tunnel_keeper_pid)
        else:
            print("Not working now")

    elif sys.argv[1] == "stop":
        if tunnel_keeper_pid:
            subprocess.Popen(f"kill -14 {tunnel_keeper_pid}", shell=True, stdout=subprocess.PIPE)
            print("Stopped!")
        else:
            print("Nothing to do!")

    elif sys.argv[1] == "start":
        subprocess.Popen(["python3", "public_ip_handler.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

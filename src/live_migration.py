from cProfile import run
from email.mime import base
from re import sub
import subprocess
import pexpect
import tempfile
import time
import os
import signal
import rpyc

def get_pid(name):
    return subprocess.check_output(["pidof", name]).decode("utf-8").strip("\n")

def run_checkpoint(pid, ):
    p = subprocess.call(["./extract", pid], shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

def update_checkpoint(pid,):
    p = subprocess.call(["mv", "spirity.binary", "old.binary"], shell=False, stderr=subprocess.STDOUT)
    p = subprocess.call(["mv", "spirity.header", "old.header"], shell=False, stderr=subprocess.STDOUT)
    run_checkpoint(pid)
    p = subprocess.call(["./jdiff081/linux/jdiff", "old.binary", "spirity.binary", "binary_diff"], shell=False, stderr=subprocess.STDOUT)
    p = subprocess.call(["./jdiff081/linux/jdiff", "old.header", "spirity.header", "header_diff"], shell=False, stderr=subprocess.STDOUT)

def transfer_file(filename):
    proc = subprocess.Popen(["scp", filename,  "danny@192.168.100.2:/home/danny/linux-tools/drivers/mremap/"], stdin=subprocess.PIPE)
    print("transfering {}!".format(filename))
    proc.wait()
    print("done file transfer")

conn_m2 = rpyc.connect("192.168.100.2", 5000)
conn_m2._config["sync_request_timeout"] = None
m2 = conn_m2.root
print("m2 connected")


base_time = time.time()

#---------------------------
current_time = time.time()
print("current time ", 0)
#---------------------------
dumper_pid = get_pid("./napp")
print("napp pid is ", dumper_pid)
print("start first-time checkpoint")
run_checkpoint(dumper_pid)
print("done first-time checkpoint")
#---------------------------
current_time = time.time()
print("current time ", current_time - base_time)
#---------------------------


print("transfer the base checkpoint file")
transfer_file("spirity.binary")
transfer_file("spirity.header")
#---------------------------
current_time = time.time()
print("current time ", current_time - base_time)
#---------------------------


for i in range(3):
    print("============================================================")
    print("round {}".format(i))
    print("I will wait 5 seconds to for you to modify the app")
    time.sleep(5)

    print("start updating checkpoint")
    #---------------------------
    current_time = time.time()
    print("current time ", current_time - base_time)
    #---------------------------
    update_checkpoint(dumper_pid)
    print("done updating checkpoint")
    #---------------------------
    current_time = time.time()
    print("current time ", current_time - base_time)
    #---------------------------


    print("transfer the checkpoint diff")
    transfer_file("binary_diff")
    transfer_file("header_diff")
    #---------------------------
    current_time = time.time()
    print("current time ", current_time - base_time)
    #---------------------------
    
    m2.apply_checkpoint_patch_on_m2()
    print("applied patch on m2")
    #---------------------------
    current_time = time.time()
    print("current time ", current_time - base_time)
    #---------------------------

# finally stop the process and start migration/restoration
os.kill(int(dumper_pid), signal.SIGTERM)
m2.inject_on_m2()
print("done injection on m2")
#---------------------------
current_time = time.time()
print("current time ", current_time - base_time)
#---------------------------




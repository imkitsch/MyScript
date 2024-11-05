import subprocess
import time
import signal
import re
import sys
import random

path="/root/ajiasu"
change_time=120

def login():
    cmd="login"
    proc_login=subprocess.Popen([path,cmd], stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    proc_login.wait()

def get_list():
    cmd_list="list"
    proc_list=subprocess.Popen([path,cmd_list], stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    stdoutdata, stderrdata=proc_list.communicate()
    # print(stdoutdata.decode('iso-8859-1'))
    proxy_out=stdoutdata.decode('iso-8859-1')
    proxy_list=re.findall(r"\n(.+?) ok",proxy_out)
    return proxy_list

if __name__ =='__main__':
    login()
    print("[+]登陆成功")
    proxy_list=get_list()
    print("[+]获取代理列表")
    proxy_length=len(proxy_list)-1
    print("[+]开始代理咯")
    while(True):
        cmd_conn="connect"
        randproxy=proxy_list[random.randint(0,proxy_length)]
        print("[+]目前代理为:"+randproxy)
        proc_conn=subprocess.Popen([path,cmd_conn,randproxy], stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        proc_conn.stdin.write(b"proxy\n")
        proc_conn.stdin.flush()
        time.sleep(change_time)
        proc_conn.send_signal(signal.SIGINT)

    

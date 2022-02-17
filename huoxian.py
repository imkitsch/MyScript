import requests
import json

def GetDomain():
    proxies = {"http":None,"https":None}
    page=154 # page数
    outfile="gd.txt" # 输出文件名
    # kw的值抓包看一下
    url="https://www.huoxian.cn/fireapi/user/search/subdomain?kw=%E7%A8%BF%E5%AE%9A%E5%AE%89%E5%85%A8%E5%BA%94%E6%80%A5%E5%93%8D%E5%BA%94%E4%B8%AD%E5%BF%83&sort=update_time_desc"
    header = {
        "Cookie": "", # 抓包全部扔进去
        "Csrf-Token": "", # # 抓包全部扔进去
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Sec-Ch-Ua": '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        "X-Token": "", # 抓包全部扔进去
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Origin": "https://www.huoxian.cn",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",

    }
    if page < 100:
        con = page
    else:
        con = 100
    for i in range(1,con+1):
        postData='{"query":[],"size":100,"pageIndex":'+str(i)+'}'
        req=requests.post(url,data=postData,headers=header,proxies=proxies, verify=False)
        for k in json.loads(req.text)['data']['items']:
            with open(outfile, "a+") as f1:
                f1.write(k['source']['subdomain']+ "\n")
            print(k['source']['subdomain'])

    if page > 100:
        postData='{"query":[],"size":100,"pageIndex":100}'
        req=requests.post(url,data=postData,headers=header,proxies=proxies, verify=False)
        tmp=json.loads(req.text)['data']['sortList'][0]['101']
        for i in range(101,page+1):
            postData='{"query":[],"size":100,"pageIndex":'+str(i)+',"searchAfter":["'+str(tmp[0])+'",'+str(tmp[1])+']}'
            req=requests.post(url,data=postData,headers=header,proxies=proxies, verify=False)
            for k in json.loads(req.text)['data']['items']:
                with open(outfile, "a+") as f1:
                    f1.write(k['source']['subdomain']+ "\n")
                print(k['source']['subdomain'])
            tmp=json.loads(req.text)['data']['sortList'][0][str(i+1)]

if __name__ == '__main__':
    GetDomain()


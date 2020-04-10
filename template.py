from urllib import request
from urllib import error
from urllib import parse
from urllib import robotparser
import string
import time
import datetime
import re
import lxml.html
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import random

fu = open('user_agent.txt','r',encoding='utf-8')
UA = fu.readlines()
fu.close()
for i,data in enumerate(UA):
    UA[i] = data.replace('\n','')

def download(url,try_times=10,user_agent=UA,proxies=None):
    global UA
    UA_len = len(UA)
    # print('Downloading:',url)
    head={'User-Agent':UA[random.randint(0,UA_len-1)]}#写入UA信息
    req=request.Request(url,headers=head)#创建Request对象
    opener=request.build_opener()#挂载opener
    try:
        html=request.urlopen(req).read()#使用自定义UA去下载
    except error.HTTPError as e:
        print('Download error:',e.reason)
        if 'Forbidden' in e.reason:
            UA.remove(head['User-Agent'])
            print('被ban了一个UA了，当前还有'+str(len(UA))+'个UA')
        if try_times>0:
            time.sleep(2)
            return download(url,try_times-1)
    return html

def crawl_page(url):
    html=download(url)
    soup = BeautifulSoup(html,'lxml')

    for k in soup.find_all('div',attrs={'class':'','id':''}):
        for i in k.find_all('p'):
            if i.string!=None:
                print(i.string)
            else:
                comp = re.compile('>(.*?)<')
                rrr = comp.findall(str(i))
                print(rrr)
        for i in k.find_all('a'):
            print(i.string)
            print(i['href'])

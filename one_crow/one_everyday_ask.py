#!/usr/bin/python
#-*-coding:utf-8-*-
'''
Created on 2016年4月27日
todo:抓取one-一个的问答数据
@author: aaksjd
'''
import argparse
import re
from multiprocessing import Pool
import bs4
import time
import urllib
from dbtest import DataSaveToDB

root_url = 'http://wufazhuce.com'
startpage=8#开始的页面
pagenum=1326#总共抓取的页面个数
curpage=startpage
dbManager=DataSaveToDB.DataSave()
def get_url(num):
    return root_url + '/question/' + str(num)
 
def get_urls(num):
    urls = map(get_url, range(startpage,startpage+num))
    return urls
 
def get_data(url):
    dataList = {}
    print "url==>",url
    pagenumstr=url.split('/')
    curpage=pagenumstr[-1]
    print "curpage==>",curpage
    response = urllib.urlopen(url)
    soup = bs4.BeautifulSoup(response,"html.parser")
    title=soup.find("title").string
    ask_info = soup.findAll(attrs={"class":"cuestion-contenido"})
    if len(ask_info)==0:
        return
    askcontent=ask_info[0].string
    asktext=""
    if isinstance(askcontent, str):
        asktext=askcontent
    else:
        for index in ask_info[0].contents:
            if isinstance(index, bs4.element.Tag):
                asktext=asktext+index.get_text().encode('utf-8')
            elif isinstance(index, bs4.element.NavigableString):
                asktext=asktext+index.string.encode('utf-8')
    coontent=ask_info[1].contents
    contentstring=""
    for index in coontent:
        if isinstance(index, bs4.element.Tag):
            contentstring=contentstring+index.get_text().encode('utf-8')
        elif isinstance(index, bs4.element.NavigableString):
            contentstring=contentstring+index.string.encode('utf-8')
    dataList["pageindex"] = curpage.encode("utf-8")
    dataList["title"] = title.encode("utf-8")
    dataList["ask_info"] =asktext
    dataList["content"] = contentstring
    print "==标题=",title.encode("utf-8")
    dbManager.insertData(dataList)
    return dataList
    
def saveDataToDB(dataList):
    dbManager=DataSaveToDB.DataSave()
    dbManager.insertData(dataList)
    dbManager.querryAllData()
    dbManager.closedDB()
    
if __name__=='__main__':
    dataList = []
    dbManager.initDB()
    urls = get_urls(pagenum)
    start = time.time()
    dataList = map(get_data, urls)
    end = time.time()
    dbManager.querryAllData()
    dbManager.closedDB()
    print '用时use: %.2f s' % (end - start)
#     saveDataToDB(dataList)
#     for i in range(len(dataList)):
#         print i,dataList[i]
#         for (k,v) in  dataList[i].items():
#             if k=="content":
#                 print "%s" %v[5:-2]
#             elif k=="imgUrl":
#                 print "%s" %v
#     jsonData = json.dumps({'data':dataList})
#     with open('data.txt', 'w') as outfile:
#         json.dump(jsonData, outfile)
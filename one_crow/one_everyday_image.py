#!/usr/bin/python
#-*-coding:utf-8-*-
'''
Created on 2016年4月27日
todo:抓取one-一个的每日一图
@author: aaksjd
'''
import argparse
import re
from multiprocessing import Pool
import bs4
import time
import json
import io
import os
import urllib 
root_url = 'http://wufazhuce.com'
startpage=14#开始的页面
pagenum=1000#总共抓取的页面个数 
def get_url(num):
    return root_url + '/one/' + str(num)
 
def get_urls(num):
    urls = map(get_url, range(startpage,startpage+num))
    return urls
 
def get_data(url):
    dataList = {}
    print "url==>",url
    response = urllib.urlopen(url)
    soup = bs4.BeautifulSoup(response,"html.parser")
#     dataList["index"] = soup.title.string[4:7]
    for meta in soup.select('meta'):
        if meta.get('name') == 'description':
            dataList["content"] = meta.get('content')
    dataList["imgUrl"] = soup.find_all('img')[1]['src']
    downloadImage(dataList["imgUrl"])
    return dataList
 #根绝imageUrl下载图片到本地     
def downloadImage(imageUrl):  
    dir = "./one_image"  
    try:  
        if not os.path.exists(dir):  
            os.mkdir(dir)  
    except:  
        print "Failed to create directory in %s"%dir  
        exit()  
    image = imageUrl.split('/')[-1]  
    path = dir+"/"+image  
    print "图片保存路径--》",path
    data = urllib.urlopen(imageUrl).read()  
    f = file(path+".jpg","wb")  
    f.write(data)  
    f.close() 
    print "图片保存完成"
    
    
    
if __name__=='__main__':
    pool = Pool(processes=4)
    dataList = []
    urls = get_urls(pagenum)
    start = time.time()
    dataList = map(get_data, urls)
    end = time.time()
    print '用时use: %.2f s' % (end - start)
#     for i in range(len(dataList)):
# #         print i,dataList[i]
#         for (k,v) in  dataList[i].items():
#             if k=="content":
#                 print "%s" %v[5:-2]
#             elif k=="imgUrl":
#                 print "%s" %v
# #     jsonData = json.dumps({'data':dataList})
# #     with open('data.txt', 'w') as outfile:
# #         json.dump(jsonData, outfile)
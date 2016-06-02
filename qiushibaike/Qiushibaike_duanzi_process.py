# coding:utf-8
# author： ou
import urllib2,os
from multiprocessing import Process,Queue,Pool
import re
import time
import sys

#糗事百科段子多进程版

reload(sys)
sys.setdefaultencoding('utf8')
def pTitle():
    return re.compile('<title.*?>(.*?)</', re.S)
def pContent():
    return re.compile('<div class="author.*?>.*?<a.*?<img.*?/>(.*?)</a>.*?</div>.*?<div.*?class="content.*?>(.*?)</div>.*?class="number.*?>(.*?)</.*?', re.S)

def getPageContent(pageNum):
    baseUrl = "http://www.qiushibaike.com/hot/page/"
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    url = baseUrl + str(pageNum)
    print u'地址：',url
    try:
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        content = response.read().decode('utf-8', 'ignore')
        content = content.encode('utf-8', 'ignore')
        return content
    except urllib2.URLError, e:
        if hasattr(e,"reason"):
            print u"error: ", e.reason
            return None

def getPageDetail(c):
    items = re.findall(pContent(), c)
    result = []
    for item in items:
        p = {}
        p['发布人'] = item[0].strip()
        p['id'] = item[2].strip()
        p['内容'] = item[1].strip()
        result.append(p)
    return result

def spider(pageList):
    dir = "./qiushibaike"
    try:
        if not os.path.exists( dir):
            os.mkdir(dir)
    except:
        print "Failed to create directory in %s"%dir
    for page in pageList:
        c = getPageContent(page)
        if c == None:
            print u"URL已失效，请重试"
            page+=1
            continue

        print u"---- 正在抓取第" + str(page) + "页 ---- "
        title = getTitle(c)
        title=title.encode('gbk', 'ignore')
        f = open(dir+'/'+title + ' - Page_' + str(page) + '.txt', 'w')
        result = getPageDetail(c)
        cutLine = u'-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.\n'
        for item in result:
            f.write(cutLine)
            for K, V in item.items():
                f.write(str(K) + ' : ' + str(V) + '\n')
        print u"---- 第" + str(page) + "页抓取完毕 ----\n"
        page+=1
        f.close()
        del result
        del f
        del cutLine
        del c
    print u"---- " + time.ctime() + " ----"
def getTitle(c):
    result = re.findall(pTitle(), c)
    return result[0].strip()

def splist(oldlist,num):
    if len(oldlist)==0 or num==0:
        return oldlist
    mainList=[]
    yu=int(len(oldlist)%num)
    chu=int(len(oldlist)/num)
    for i in range(num):
        if i==num-1:
            mainList.append(oldlist[i*chu:(i+1)*chu+yu])
        else:
            mainList.append(oldlist[i*chu:(i+1)*chu])
    return mainList
if __name__ == '__main__':
    startTime=time.time()
    maxPage = 35
    pageList=[]
    for i in range(maxPage):
        pageList.append(i)
    # pw = Process(target=spider, args=(pageList[1:17],))
    # pr = Process(target=spider, args=(pageList[17:],))
    # pw.start()
    # pr.start()
    # pw.join()
    # pr.terminate()
    #进程池抓取

    processNum=4;
    pageList=splist(pageList,processNum)
    print pageList
    p = Pool()
    for i in range(processNum):
        p.apply_async(spider, args=(pageList[i],))
    p.close()
    p.join()
    endTime=time.time()
    print u'用时：%s秒'%(endTime-startTime)
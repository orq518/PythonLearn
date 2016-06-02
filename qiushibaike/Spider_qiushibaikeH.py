# coding:utf-8
# author： ou
import urllib,os
from multiprocessing import Pool
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf8')
#糗事百科H版

debug = True # 设置是否打印log
def log(message):
    if debug:
        print message

def download_image(url, save_path):
    ''' 根据图片url下载图片到save_path '''
    try:
        urllib.urlretrieve(url, save_path)
        log('Downloaded a image: ' + save_path)
    except Exception, e:
        print 'An error catched when download a image:', e

def load_page_html(url):
    ''' 得到页面的HTML文本 '''
    log('Get a html page : ' + url)
    return urllib.urlopen(url).read()

def down_page_images(page, save_dir):
    ''' 下载第page页的图片 '''
    html_context = load_page_html('http://qiubaichengren.com/%d.html' % page)
    soup = BeautifulSoup(html_context)
    for ui_module_div in soup.findAll('div', {'class': 'ui-module'}):
        img_tag = ui_module_div.find('img')
        try:
            if img_tag is not None and img_tag.has_attr('alt') and img_tag.has_attr('src'):
                alt = img_tag.attrs['alt'] # 图片的介绍
                src = img_tag.attrs['src'] # 图片的地址
                filename = '%s%s' % (alt, src[-4:]) # 取后四位（有的图片后缀是'.jpg'而有的是'.gif'）
                download_image(src, save_dir + filename)
        except:
            continue

def download_qbcr(frm=1, page_count=1, save_dir='./'):
    for x in xrange(frm, frm + page_count):
        log('Page : ' + x)
        down_page_images(x, save_dir)

def download_qbcr(pageList, save_dir='./'):
    for x in pageList:
        log('Page %s:'%x)
        down_page_images(x, save_dir)
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

def main():
    base_path = './qiubaiH/'
    if os.path.exists(base_path):
        pass
    else:
        os.makedirs(base_path)
    # download_qbcr(frm=1, page_count=10, save_dir=base_path)

    maxPage = 10
    pageList=[]
    for i in range(maxPage):
        pageList.append(i)
    processNum=4;
    pageList=splist(pageList,processNum)
    p = Pool()
    for i in range(processNum):
        p.apply_async(download_qbcr, args=(pageList[i],base_path,))
    p.close()
    p.join()

if __name__ == '__main__':
    main()
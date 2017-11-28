__author__="ZYK"
# -*- coding:utf-8 -*-
import urllib
from urllib import request
from bs4 import BeautifulSoup
import re
import tool
import ssl
import os
import sys


#-----------------------------------
#煎蛋网爬虫
#-----------------------------------
class Spider:

    def __init__(self,url):
        self.siteURL =  url
        self.headers = {
        	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) '
        	             +'AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4',
            'Accept'	: 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer'   : 'https://jandan.net/ooxx',
            'Upgrade-Insecure-Requests':	'1'

    }
    #--------------------------------
    #通用方法
    #封装常用到的代码减少代码量
    #openUrl(url)
    #mkdir(path)
    #writeToFile(path,name,data)
    #--------------------------------

    #访问网络资源
    def openUrl(self, url):
        req = request.Request(url, headers=self.headers)
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        print ("正在访问" + url)
        resp = request.urlopen(req,context=gcontext)
        print (url + "资源已取得")
        return resp;

    #获取网页标题
    def getTitle(self, page):
        soup = BeautifulSoup(page, "html.parser")
        return soup.title.string.encode("utf-8")

    #创建文件夹
    def mkdir(self, path):
        path = path.strip()

        isExists=os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            print ("创建目录"+path)
            return True
        else:
            print (u'名为'+path+'的文件夹已经存在')
            return False
    #保存数据到本地
    def writeToFile(self, path, name, data):
        f = open(path + "/" + name,'wb')
        f.write(data)
        print ("数据" + name + "已保存到本地" + path)
        f.close()

    #----------------------------------
    #Spider方法
    #
    #----------------------------------
    def getPage(self, pageIndex):
        url = self.siteURL + "/page-"+str(pageIndex)
        print ("正在爬取页面" + url)
        response = self.openUrl(url)
        page = response.read().decode('utf-8')
        #print (page)
        return page

    def downloadFile(self, items, target_path):
        self.mkdir(target_path)
        print("正在下载文件...")
        for i, item in enumerate(items):
            print ("正在下载文件（ %d ）%s " % (i, item))
            image_name= str(i)+item[-4:]
            resp = self.openUrl(item)
            self.writeToFile(target_path, image_name, resp.read())
    def downloadImage(self, items, target_path="./Photo"):
           self.mkdir(target_path)
           print("正在下载图片...")

           for i, item in enumerate(items):
                print ("正在下载图片（ %d ）%s " % (i, item))
                image_name= str(i)+item[-4:]
                resp = self.openUrl("http:" + item)
                self.writeToFile(target_path, image_name, resp.read())


    def getContents(self, page):
        print ("正在匹配...")
        pattern = re.compile('<img src="(//wx4.sinaimg.cn/.*?)"',re.S)
        items = re.findall(pattern,page)

        for i, item in enumerate(items):
            print ("匹配到的内容（ %d ）%s " % (i, item))

        return items
    #----------------------------------
    #爬虫方法
    #实现分步爬虫，降低耦合性
    #----------------------------------
    def crawlPage(self, index):
        print ("正在爬取第" + str(index) + "页")
        page = self.getPage(index)
        contents = self.getContents(page)
        self.downloadImage(contents, "./meizitu" + str(index))
    #----------------------------------------
    #批量爬取页面
    #----------------------------------------
    def crawl(self, start, end):
        for i in range(start, end):
            self.crawlPage(i)
            print ("开始爬取下一个页面")

    def getLatestPage(self):
        response = self.openUrl(self.siteURL)
        page = response.read().decode('utf-8')
        soup = BeautifulSoup(page, "html.parser")
        text = soup.find('span', class_='current-comment-page').get_text()
        return text[1:-1]
    def crawlUsingThread(self, start, end):
        pass
    #-----------------------------------------
    #获取最新的n张图片
    #-----------------------------------------
    def crawlLatestPics(self, num):
        curr = self.getLatestPage()
        for i in  range(0, num):
            pass
if __name__ == '__main__':

    '''
    #传入命令行参数
    if(len(sys.argv) != 3):
        print("正确的使用方法：输入一个起始页码，一个终止页码！")
        exit()

    start = int(sys.argv[1])
    end = int(sys.argv[2])

    if(start > end) :
        print("起始页码不能大于终止页码")
        exit()
    '''
    url = 'https://jandan.net/ooxx'
    spider = Spider(url)
    #spider.crawl(100, 110)
    print(spider.getLatestPage())
    spider.crawlLatestPics(10)